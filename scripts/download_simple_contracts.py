"""
Download Simple (<100 SLOC) contracts dan tambahkan ke contracts_metadata_expanded.json.
Jalankan: python scripts/download_simple_contracts.py
"""
import json, os, re, time, sys
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

SIMPLE_CANDIDATES = [
    # DeFi Simple (MakerDAO DSS adapters)
    {'address': '0x3bc3a58b4fc1cbe7e98bb4ab7c99535e8ba9b8f1', 'name': 'GemJoin',  'domain': 'DeFi'},
    {'address': '0x9759A6Ac90977b93B58547b4A71c78317f391A28', 'name': 'DaiJoin',  'domain': 'DeFi'},
    {'address': '0x65C79fcB50Ca1594B025960e539eD7A9a6D434A3', 'name': 'Spotter',  'domain': 'DeFi'},
    {'address': '0x2F0b23f53734252Bda2277357e97e1517d6B042A', 'name': 'ETHJoin',  'domain': 'DeFi'},
    # Utility Simple
    {'address': '0xeefBa1e63905eF1D7ACbA5a8513c70307C1cE441', 'name': 'Multicall', 'domain': 'Utility'},
    # Governance Simple
    {'address': '0x6d903f6003cca6255D85CcA4D3B5E650146C52C', 'name': 'CompoundTimelock', 'domain': 'Governance'},
]

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
    import tempfile
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
            solcx.compile_standard(inp, solc_version=ver)
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
            solcx.compile_source(dedup_pragma(src),output_values=['ast'],
                                 solc_version=ver,optimize=False)
            return True
        except Exception: pass
        try:
            stripped = re.sub(r'^\s*import\s+[^;]+;','',src,flags=re.MULTILINE)
            solcx.compile_source(dedup_pragma(stripped),output_values=['ast'],
                                 solc_version=ver,optimize=False)
            return True
        except Exception: pass
    return False

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

# ── Main ────────────────────────────────────────────────────────────────────

# Load existing metadata
with open(ROOT / 'contracts_metadata_expanded.json') as f:
    existing = json.load(f)
existing_addrs = {c['alamat'].lower() for c in existing}

results = []
failed  = []

print(f'Downloading {len(SIMPLE_CANDIDATES)} Simple candidate contracts...\n')

for cand in SIMPLE_CANDIDATES:
    addr   = cand['address']
    name   = cand['name']
    domain = cand['domain']

    if addr.lower() in existing_addrs:
        print(f'  [skip] {name} — already in metadata')
        continue

    dest_dir = ROOT / 'dataset' / domain.lower()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / f'{name}.sol'

    if dest_path.exists():
        src = dest_path.read_text(encoding='utf-8')
        print(f'  [skip download] {name} — file exists')
    else:
        raw_src, fetched_name, err = fetch_source(addr)
        if not raw_src:
            print(f'  [FAIL] {name} ({addr[:12]}...): {err}')
            failed.append({'name': name, 'address': addr, 'error': err})
            time.sleep(0.25)
            continue
        dest_path.write_text(raw_src, encoding='utf-8')
        src = raw_src
        if fetched_name and fetched_name != name:
            print(f'  [note] Etherscan name: {fetched_name} (using {name})')
        time.sleep(0.25)

    # Compute SLOC and complexity
    lines = dest_path.read_text(encoding='utf-8').splitlines()
    sloc  = sum(1 for l in lines if l.strip())
    complexity = 'Simple' if sloc < 100 else 'Medium' if sloc < 500 else 'Complex'

    # Try compile
    src_content = dest_path.read_text(encoding='utf-8')
    ver = detect_ver(src_content)
    compile_ok = try_compile(src_content, ver)
    status = '✅' if compile_ok else '⚠️ '
    print(f'  {status} [{domain:12s}] {name:25s} SLOC={sloc:4d} [{complexity}] solc={ver}')

    results.append({
        'alamat':     addr,
        'domain':     domain,
        'nama':       name,
        'file':       str(dest_path),
        'loc':        sloc,
        'complexity': complexity,
        'compile_ok': compile_ok,
        'solc_ver':   ver,
        'is_proxy':   False,
        'source':     'simple_added',
    })

print(f'\n{"="*60}')
print(f'Downloaded: {len(results)}  Failed: {len(failed)}')

if not results:
    print('Nothing new to add.')
    sys.exit(0)

# Validate SLOC < 100
non_simple = [r for r in results if r['complexity'] != 'Simple']
if non_simple:
    print(f'\n⚠️  WARNING: These contracts exceed SLOC<100 threshold:')
    for r in non_simple:
        print(f'   {r["nama"]}: SLOC={r["loc"]} ({r["complexity"]})')

# Append to expanded metadata and save backup first
import shutil
backup_path = ROOT / 'contracts_metadata_expanded_presimple_backup.json'
shutil.copy(ROOT / 'contracts_metadata_expanded.json', backup_path)
print(f'\nBacked up existing metadata to {backup_path.name}')

merged = existing + results
out_path = ROOT / 'contracts_metadata_expanded.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

print(f'Saved {len(merged)} contracts to contracts_metadata_expanded.json')
print(f'  (was {len(existing)}, added {len(results)})')
