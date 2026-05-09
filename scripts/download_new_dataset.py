"""
Download semua kontrak dari docs/metadata.csv ke dataset/ subdirs.
Jalankan: python scripts/download_new_dataset.py
Requires: ETHERSCAN_API_KEY di .env
"""
import csv, json, os, re, time, tempfile
from pathlib import Path
from dotenv import load_dotenv
import requests, solcx
from packaging.version import Version as PkgVersion

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / '.env')
API_KEY = os.getenv('ETHERSCAN_API_KEY', '')
if not API_KEY:
    raise ValueError('ETHERSCAN_API_KEY tidak ditemukan di .env')

SOLC_MAP = {'0.4':'0.4.26','0.5':'0.5.17','0.6':'0.6.12','0.7':'0.7.6','0.8':'0.8.20'}

# ── helpers ──────────────────────────────────────────────────────────────────

def detect_ver(src):
    m = re.search(r'pragma solidity\s*=?\s*(\d+\.\d+\.\d+)\s*;', src)
    if m: return m.group(1)
    m = re.search(r'pragma solidity\s+[>=^<~]*\s*(\d+\.\d+)', src)
    if not m: return '0.8.20'
    mm = '.'.join(m.group(1).split('.')[:2])
    return SOLC_MAP.get(mm, '0.8.20')

def dedup_pragma(src):
    seen, lines = False, []
    for line in src.splitlines():
        if re.match(r'\s*pragma solidity', line):
            if not seen: lines.append(line); seen = True
        else:
            lines.append(line)
    return '\n'.join(lines)

def parse_multifile(src):
    parts = re.split(r'// === File: (.+?) ===', src)
    if len(parts) <= 1: return None
    files = {}
    for i in range(1, len(parts)-1, 2):
        files[parts[i].strip()] = parts[i+1]
    return files or None

def try_compile(src, ver):
    files = parse_multifile(src)
    if PkgVersion(ver) < PkgVersion('0.4.11'): ver = '0.4.26'
    installed = [str(v) for v in solcx.get_installed_solc_versions()]
    if ver not in installed:
        print(f'      installing solc {ver}...')
        solcx.install_solc(ver)
    if files:
        try:
            inp = {"language":"Solidity",
                   "sources":{n:{"content":c} for n,c in files.items()},
                   "settings":{"optimizer":{"enabled":False},
                               "outputSelection":{"*":{"":["ast"]}}}}
            out = solcx.compile_standard(inp, solc_version=ver)
            return True
        except Exception: pass
        try:
            with tempfile.TemporaryDirectory() as td:
                tdp = Path(td)
                for name, content in files.items():
                    fp2 = tdp/name; fp2.parent.mkdir(parents=True,exist_ok=True)
                    fp2.write_text(content,encoding='utf-8')
                out = solcx.compile_files([str(tdp/next(iter(files)))],
                    output_values=['ast'],solc_version=ver,optimize=False,allow_paths=[td])
                return bool(out)
        except Exception: pass
    else:
        try:
            out = solcx.compile_source(dedup_pragma(src),output_values=['ast'],
                                       solc_version=ver,optimize=False)
            return bool(out)
        except Exception: pass
        try:
            stripped = re.sub(r'^\s*import\s+[^;]+;','',src,flags=re.MULTILINE)
            out = solcx.compile_source(dedup_pragma(stripped),output_values=['ast'],
                                       solc_version=ver,optimize=False)
            return bool(out)
        except Exception: pass
    return False

# ── download ─────────────────────────────────────────────────────────────────

def fetch_source(address):
    url = (f'https://api.etherscan.io/v2/api?chainid=1'
           f'&module=contract&action=getsourcecode'
           f'&address={address}&apikey={API_KEY}')
    for attempt in range(3):
        try:
            resp = requests.get(url, timeout=15)
            data = resp.json()
            break
        except Exception as e:
            if attempt == 2: return None, None, str(e)
            time.sleep(2**attempt)
    if data.get('status') != '1': return None, None, data.get('message','API error')
    r = data['result'][0]
    src = r.get('SourceCode','')
    name = r.get('ContractName','')
    if not src: return None, None, 'not verified'
    # flatten {{json}} format
    if src.startswith('{{'):
        try:
            fj = json.loads(src[1:-1])
            parts = []
            for path, content in fj['sources'].items():
                parts.append(f'// === File: {path} ===')
                parts.append(content['content'])
            src = '\n\n'.join(parts)
        except Exception: pass
    return src, name, None

# ── main ─────────────────────────────────────────────────────────────────────

with open(ROOT/'docs/metadata.csv') as f:
    rows = list(csv.DictReader(f))

results = []
failed  = []

print(f'Downloading {len(rows)} contracts from metadata.csv...\n')

for row in rows:
    addr        = row['address']
    domain      = row['domain']
    contract_nm = row['contract_name']
    dest_path   = ROOT / row['source_file']
    is_proxy    = row.get('proxy','0') == '1'
    impl_addr   = row.get('implementation','').strip()
    expected_loc = int(row['loc']) if row['loc'] else 0

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # If already exists, skip download but still validate
    if dest_path.exists():
        src = dest_path.read_text(encoding='utf-8')
        print(f'  [skip] {contract_nm} — already exists')
    else:
        # For proxy contracts: try implementation address first if available
        src = None
        tried = []
        for fetch_addr in ([impl_addr, addr] if (is_proxy and impl_addr) else [addr]):
            if not fetch_addr or fetch_addr in tried: continue
            tried.append(fetch_addr)
            raw_src, fetched_name, err = fetch_source(fetch_addr)
            if raw_src:
                src = raw_src
                if fetched_name and fetch_addr == impl_addr:
                    # Use proxy name but implementation source
                    pass
                break
            time.sleep(0.3)

        if not src:
            print(f'  [FAIL] {contract_nm} ({addr[:10]}...): {err}')
            failed.append({'domain': domain, 'address': addr, 'name': contract_nm, 'error': err})
            time.sleep(0.25)
            continue

        dest_path.write_text(src, encoding='utf-8')
        time.sleep(0.25)

    # Measure actual LOC and complexity
    actual_loc = len(dest_path.read_text(encoding='utf-8').splitlines())
    complexity = 'Simple' if actual_loc < 100 else 'Medium' if actual_loc < 500 else 'Complex'

    # Try compile
    src_content = dest_path.read_text(encoding='utf-8')
    ver = detect_ver(src_content)
    compile_ok = try_compile(src_content, ver)
    status = '✅' if compile_ok else '⚠️ '
    print(f'  {status} [{domain:10s}] {contract_nm:35s} LOC={actual_loc:5d} [{complexity}] solc={ver}')

    results.append({
        'alamat':      addr,
        'domain':      domain,
        'nama':        contract_nm,
        'file':        str(dest_path),
        'loc':         actual_loc,
        'complexity':  complexity,
        'compile_ok':  compile_ok,
        'solc_ver':    ver,
        'is_proxy':    is_proxy,
    })

# Save
out_path = ROOT / 'contracts_metadata_new.json'
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f'\n{"="*60}')
print(f'Downloaded : {len(results)}')
print(f'Failed     : {len(failed)}')
print(f'Compile OK : {sum(1 for r in results if r["compile_ok"])}')
print(f'\nComplexity distribution:')
from collections import Counter
for c, n in Counter(r["complexity"] for r in results).items():
    print(f'  {c:8s}: {n}')
print(f'\nSaved to: {out_path}')
if failed:
    print(f'\nFailed contracts:')
    for f in failed:
        print(f'  {f["domain"]:10s} {f["name"]:30s} {f["error"]}')
