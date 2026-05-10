"""
Generate manual audit checklist for top-20 contracts by estimated gas savings.
Run from project root: conda run -n gas_opt python scripts/generate_audit_checklist.py
"""
import sys, json, re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.ast_parser import generate_ast
from src.detectors import ALL_DETECTORS

GAS_DIFF = {
    'redundant_sload':      186,
    'unoptimized_loop':    1031,
    'string_vs_bytes32':    950,
    'public_vs_external':  2673,
    'unchecked_arithmetic':12045,
    'dead_code':              0,
}

PATTERN_FULL = {
    'redundant_sload':      'Redundant SLOAD',
    'unoptimized_loop':     'Unoptimized Loop',
    'string_vs_bytes32':    'String vs Bytes32',
    'public_vs_external':   'Public vs External',
    'unchecked_arithmetic': 'Unchecked Arithmetic',
    'dead_code':            'Dead Code',
}

PATTERN_QUESTION = {
    'redundant_sload':
        'Buka fungsi yang disebutkan, cari apakah state variable dibaca >1x **tanpa assignment di antara pembacaan**.',
    'public_vs_external':
        'Cari fungsi yang disebutkan, periksa apakah ada pemanggilan `functionName()` (tanpa `this.`) di dalam kontrak yang sama.',
    'string_vs_bytes32':
        'Cari state variable yang disebutkan, periksa apakah nilai string-nya selalu ≤32 karakter.',
    'unoptimized_loop':
        'Cari for-loop yang disebutkan, periksa apakah `array.length` ada di kondisi loop dan array itu adalah state variable.',
    'dead_code':
        'Cari fungsi yang disebutkan, lakukan Ctrl+F nama fungsi tersebut — apakah ada pemanggilan selain deklarasi?',
    'unchecked_arithmetic':
        'Cari for-loop yang disebutkan, periksa apakah increment `i++` sudah dibungkus `unchecked {}`.',
}

# ── Build filename → full path index ──────────────────────────────────────
sol_index = {}
for f in ROOT.rglob('*.sol'):
    if '.git' in str(f) or 'hardhat_project' in str(f):
        continue
    sol_index[f.name] = str(f.resolve())

def resolve_path(file_field):
    name = Path(file_field).name
    if name in sol_index:
        return sol_index[name]
    if Path(file_field).exists():
        return file_field
    return None

# ── Load summary + build top-20 ────────────────────────────────────────────
with open(ROOT / 'results' / 'pekan2_detector_results.json', encoding='utf-8') as f:
    summary_data = json.load(f)

results = []
for r in summary_data:
    if not r.get('compile_ok', True): continue
    savings = sum(r.get(p, 0) * GAS_DIFF[p] for p in GAS_DIFF)
    if savings == 0: continue
    results.append({**r, 'savings': savings})
results.sort(key=lambda x: -x['savings'])

MIN_PER_DOMAIN = 2
TARGET = 20
selected = []
domain_count = defaultdict(int)

for r in list(results):
    if len(selected) >= TARGET: break
    selected.append(r)
    domain_count[r['domain']] += 1

for domain in ['DeFi','NFT','Token','Governance','Utility']:
    if domain_count[domain] < MIN_PER_DOMAIN:
        deficit = MIN_PER_DOMAIN - domain_count[domain]
        candidates = [r for r in results if r['domain'] == domain and r not in selected]
        for c in candidates[:deficit]:
            over = max((d for d in domain_count if domain_count[d] > MIN_PER_DOMAIN),
                       key=lambda d: domain_count[d], default=None)
            if over:
                to_remove = min([s for s in selected if s['domain'] == over], key=lambda x: x['savings'])
                selected.remove(to_remove)
                domain_count[over] -= 1
                selected.append(c)
                domain_count[domain] += 1

selected.sort(key=lambda x: -x['savings'])

# ── Run detectors ──────────────────────────────────────────────────────────
print(f"Running detectors on {len(selected)} contracts...\n")

audit_data = []
for idx, meta in enumerate(selected, 1):
    filepath = resolve_path(meta['file'])
    if filepath is None:
        print(f"[{idx:02d}/20] {meta['nama']} — FILE NOT FOUND")
        continue
    print(f"[{idx:02d}/20] {meta['nama']} ({meta['domain']}) ...", end=' ', flush=True)

    ast = generate_ast(filepath)
    if ast is None:
        print("AST FAILED")
        continue

    contract_findings = {}
    for det_name, detect_fn in ALL_DETECTORS:
        try:
            contract_findings[det_name] = detect_fn(ast)
        except Exception:
            contract_findings[det_name] = []

    total = sum(len(v) for v in contract_findings.values())
    print(f"{total} findings")

    audit_data.append({
        'rank': idx,
        'nama': meta['nama'],
        'domain': meta['domain'],
        'complexity': meta['complexity'],
        'loc': meta['loc'],
        'file': filepath,
        'estimated_savings': meta['savings'],
        'findings_by_pattern': contract_findings,
    })

# ── Save raw JSON ──────────────────────────────────────────────────────────
out_dir = ROOT / 'docs' / 'manual_audit'
out_dir.mkdir(parents=True, exist_ok=True)
with open(out_dir / 'audit_findings_raw.json', 'w', encoding='utf-8') as f:
    json.dump(audit_data, f, indent=2, ensure_ascii=False)

# ── Helper: extract subject from description ──────────────────────────────
def extract_subject(desc, pattern):
    """Pull variable/function name from description string."""
    if pattern == 'redundant_sload':
        m = re.search(r"'(\w+)' dibaca.*fungsi '(\w+)'", desc)
        if m: return f"`{m.group(1)}` in `{m.group(2)}()`"
    elif pattern == 'public_vs_external':
        m = re.search(r"fungsi '(\w+)'", desc)
        if m: return f"`{m.group(1)}()`"
    elif pattern == 'string_vs_bytes32':
        m = re.search(r"'(\w+)'", desc)
        if m: return f"`{m.group(1)}`"
    elif pattern == 'unoptimized_loop':
        m = re.search(r"'(\w+)'", desc)
        if m: return f"`{m.group(1)}.length`"
    elif pattern == 'dead_code':
        m = re.search(r"fungsi '(\w+)'", desc)
        if m: return f"`{m.group(1)}()`"
    elif pattern == 'unchecked_arithmetic':
        m = re.search(r"loop.*'(\w+)'", desc)
        if m: return f"loop var `{m.group(1)}`"
    return desc[:50]

# ── Generate Markdown checklist ────────────────────────────────────────────
lines = []
lines += [
    "# Manual Audit Checklist — 20 Kontrak Top Gas Savings",
    "",
    "**Tujuan**: Verifikasi setiap temuan detektor — apakah anti-pattern gas benar-benar ada di kode.",
    "",
    "## Cara Mengisi",
    "",
    "Untuk setiap baris temuan, buka file `.sol` yang tercantum, cari nama fungsi/variabel,",
    "lalu tandai kolom `Audit`:",
    "",
    "| Kode | Arti |",
    "|---|---|",
    "| `TP` | True Positive — anti-pattern memang ada, temuan valid |",
    "| `FP` | False Positive — bukan anti-pattern, detektor salah flag |",
    "| `?`  | Ambiguous — tidak yakin, butuh diskusi |",
    "",
    "Isi kolom `Catatan` jika FP atau ?: jelaskan singkat kenapa.",
    "",
    "---",
    "",
    "## Ringkasan 20 Kontrak",
    "",
    "| # | Kontrak | Domain | LOC | Savings (gas) | rs | ul | sb | pe | dc | Total |",
    "|---|---|---|---|---|---|---|---|---|---|---|",
]

for c in audit_data:
    fp = c['findings_by_pattern']
    lines.append(
        f"| {c['rank']} | **{c['nama']}** | {c['domain']} | {c['loc']} | "
        f"{c['estimated_savings']:,} | "
        f"{len(fp.get('redundant_sload',[]))} | "
        f"{len(fp.get('unoptimized_loop',[]))} | "
        f"{len(fp.get('string_vs_bytes32',[]))} | "
        f"{len(fp.get('public_vs_external',[]))} | "
        f"{len(fp.get('dead_code',[]))} | "
        f"{sum(len(v) for v in fp.values())} |"
    )

total_savings = sum(c['estimated_savings'] for c in audit_data)
total_findings = sum(sum(len(v) for v in c['findings_by_pattern'].values()) for c in audit_data)
lines += [
    "",
    f"**Total estimated savings**: {total_savings:,} gas  ",
    f"**Total findings to audit**: {total_findings}",
    "",
    "---",
    "",
]

# ── Per-contract sections ──────────────────────────────────────────────────
for c in audit_data:
    fp = c['findings_by_pattern']
    total_f = sum(len(v) for v in fp.values())
    fname = Path(c['file']).name

    lines += [
        f"## [{c['rank']:02d}] {c['nama']}",
        "",
        f"| Field | Value |",
        f"|---|---|",
        f"| Domain | {c['domain']} |",
        f"| Complexity | {c['complexity']} |",
        f"| LOC | {c['loc']} |",
        f"| File | `{fname}` |",
        f"| Estimated Savings | **{c['estimated_savings']:,} gas** |",
        f"| Total Findings | {total_f} |",
        "",
    ]

    for det_name, findings in fp.items():
        if not findings:
            continue

        gas_each = GAS_DIFF[det_name]
        total_gas = gas_each * len(findings)
        lines += [
            f"### {PATTERN_FULL[det_name]} — {len(findings)} temuan ({total_gas:,} gas potensial)",
            "",
            f"> **Cara audit**: {PATTERN_QUESTION[det_name]}",
            "",
            "| # | Yang Di-flag | Audit | Catatan |",
            "|---|---|---|---|",
        ]

        for i, f in enumerate(findings, 1):
            subject = extract_subject(f.get('description',''), det_name)
            lines.append(f"| {i} | {subject} | `[ ]` | |")

        lines += [
            "",
            f"**Hasil**: {len(findings)} flagged → TP: ___ / FP: ___ / ?: ___  "
            f"→ Precision = ___% ",
            "",
        ]

    lines += [
        "**Ringkasan kontrak**:",
        "",
        "| Pattern | Flagged | TP | FP | Precision |",
        "|---|---|---|---|---|",
    ]
    for det_name, findings in fp.items():
        if findings:
            lines.append(f"| {PATTERN_FULL[det_name]} | {len(findings)} | | | |")
    lines += ["", "---", ""]

# ── Precision summary template ─────────────────────────────────────────────
lines += [
    "## Rekap Akhir — Precision per Pattern",
    "",
    "Isi setelah semua kontrak selesai diaudit.",
    "",
    "| Pattern | Total Flagged | Total TP | Total FP | Precision (%) |",
    "|---|---|---|---|---|",
]
pattern_totals = {}
for c in audit_data:
    for det_name, findings in c['findings_by_pattern'].items():
        pattern_totals[det_name] = pattern_totals.get(det_name, 0) + len(findings)

for det_name, total in sorted(pattern_totals.items(), key=lambda x: -x[1]):
    if total > 0:
        lines.append(f"| {PATTERN_FULL[det_name]} | {total} | | | |")

lines += [
    "",
    "**Catatan**: Precision yang diharapkan berdasarkan karakteristik detektor:",
    "- `public_vs_external`: ~90% (deterministik, FP hanya jika dipanggil via `this.fn()`)",
    "- `redundant_sload`: ~70–80% (FP jika state var dimodifikasi antar pembacaan)",
    "- `string_vs_bytes32`: ~85% (FP jika string memang butuh dinamis)",
    "- `dead_code`: ~65–75% (FP tinggi karena tidak bisa track cross-contract calls)",
    "- `unoptimized_loop`: ~95% (sangat deterministik, FP sangat jarang)",
]

out_md = out_dir / 'AUDIT_CHECKLIST.md'
with open(out_md, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"\nSaved raw findings : docs/manual_audit/audit_findings_raw.json")
print(f"Generated checklist: docs/manual_audit/AUDIT_CHECKLIST.md")
print(f"\nTotal findings to audit: {total_findings} across 20 contracts")
print(f"Breakdown by pattern:")
for det_name, total in sorted(pattern_totals.items(), key=lambda x: -x[1]):
    if total > 0:
        print(f"  {PATTERN_FULL[det_name]:<25}: {total}")
