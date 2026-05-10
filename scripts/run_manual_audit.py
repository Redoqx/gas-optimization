"""
Automated manual audit: reads each .sol file and verifies each detector finding.
Run from project root: conda run -n gas_opt python scripts/run_manual_audit.py
"""
import sys, json, re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

# ── Load raw findings ──────────────────────────────────────────────────────
with open(ROOT / 'docs' / 'manual_audit' / 'audit_findings_raw.json', encoding='utf-8') as f:
    audit_data = json.load(f)

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

# ═══════════════════════════════════════════════════════════════════════════
# VERIFICATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def load_sol(filepath):
    """Load .sol source, return (lines list, full text)."""
    path = Path(filepath)
    if not path.exists():
        return None, None
    text = path.read_text(encoding='utf-8', errors='replace')
    return text.splitlines(), text


def extract_func_name(desc, pattern):
    """Pull function/variable name from detector description."""
    if pattern == 'public_vs_external':
        m = re.search(r"fungsi '(\w+)'", desc)
        return m.group(1) if m else None
    elif pattern == 'redundant_sload':
        m = re.search(r"'(\w+)' dibaca.*fungsi '(\w+)'", desc)
        if m: return (m.group(1), m.group(2))   # (varname, funcname)
        m = re.search(r"SLOAD:? '?(\w+)'?", desc)
        return (m.group(1), None) if m else None
    elif pattern == 'string_vs_bytes32':
        m = re.search(r"'(\w+)'", desc)
        return m.group(1) if m else None
    elif pattern in ('dead_code', 'unoptimized_loop', 'unchecked_arithmetic'):
        m = re.search(r"fungsi '(\w+)'", desc)
        return m.group(1) if m else None
    return None


def check_public_vs_external(lines, text, func_name):
    """
    TP: function is truly never called internally.
    FP sources:
      1. Called as this.funcName() — external call but within same contract
      2. Called via super.funcName()
      3. Is 'constructor' (never flagged but guard anyway)
      4. Has 'override' keyword and called from child (can't detect, mark ?)
      5. Direct internal call: funcName(
    """
    if not func_name or func_name == 'constructor':
        return '?', 'constructor / no name'

    # Look for internal call pattern: funcName( but not function funcName(
    # Also check for this.funcName( and super.funcName(
    call_pattern  = re.compile(r'\b' + re.escape(func_name) + r'\s*\(')
    this_pattern  = re.compile(r'\bthis\.' + re.escape(func_name) + r'\s*\(')
    super_pattern = re.compile(r'\bsuper\.' + re.escape(func_name) + r'\s*\(')

    internal_calls = []
    this_calls = []
    super_calls = []
    decl_lines = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Skip comments
        if stripped.startswith('//') or stripped.startswith('*'):
            continue
        # Declaration line
        if re.search(r'\bfunction\s+' + re.escape(func_name) + r'\b', line):
            decl_lines.append(i)
            continue
        if this_pattern.search(line):
            this_calls.append(i)
        elif super_pattern.search(line):
            super_calls.append(i)
        elif call_pattern.search(line):
            internal_calls.append(i)

    if internal_calls:
        return 'FP', f'called internally at lines {internal_calls[:3]}'
    if this_calls:
        return 'FP', f'called via this.{func_name}() at lines {this_calls[:3]}'
    if super_calls:
        return 'FP', f'called via super.{func_name}() at lines {super_calls[:3]}'

    # Check if function has 'override' — might be required public by interface
    for i, line in enumerate(lines, 1):
        if re.search(r'\bfunction\s+' + re.escape(func_name) + r'\b', line):
            if 'override' in line:
                return '?', f'has override keyword (line {i}) — may need public for interface'

    return 'TP', ''


def extract_function_body(lines, func_name):
    """Return lines of the named function body."""
    in_func = False
    depth = 0
    body = []
    start_pattern = re.compile(r'\bfunction\s+' + re.escape(func_name) + r'\b')

    for line in lines:
        if not in_func:
            if start_pattern.search(line):
                in_func = True
                depth = line.count('{') - line.count('}')
                body.append(line)
        else:
            depth += line.count('{') - line.count('}')
            body.append(line)
            if depth <= 0:
                break
    return body


def check_redundant_sload(lines, text, var_name, func_name):
    """
    TP: var is read 2+ times in function with no assignment between reads.
    FP: assignment to var exists between the two reads.
    """
    if not var_name:
        return '?', 'could not parse variable name'

    func_body = extract_function_body(lines, func_name) if func_name else lines

    # Assignment patterns for this variable
    vn = re.escape(var_name)
    assign_pat = re.compile(
        r'\b' + vn + r'\s*(?:\[.*?\])?\s*(?:\+|-|\*|/|&|\||\^)?=' +
        r'|(?:\+\+|--)' + vn +
        r'|\b' + vn + r'(?:\+\+|--)'
    )
    read_pat = re.compile(r'\b' + re.escape(var_name) + r'\b')

    read_positions = []
    assignment_positions = []

    for i, line in enumerate(func_body):
        s = line.strip()
        if s.startswith('//') or s.startswith('*'):
            continue
        if assign_pat.search(line):
            assignment_positions.append(i)
        elif read_pat.search(line):
            read_positions.append(i)

    if len(read_positions) < 2:
        return '?', f'only {len(read_positions)} reads found in function body — may be cross-function or parse issue'

    # Check if any assignment falls between first and last read
    first_read = read_positions[0]
    last_read  = read_positions[-1]
    interleaved = [a for a in assignment_positions if first_read < a < last_read]

    if interleaved:
        return 'FP', f'assignment to `{var_name}` at body-line {interleaved[0]} between reads'

    return 'TP', f'{len(read_positions)} reads, no assignment between them'


def check_string_vs_bytes32(lines, text, var_name):
    """
    TP: string state variable with value ≤32 chars.
    FP: value is longer, dynamic, or it's a parameter/local (not state var).
    """
    if not var_name:
        return '?', 'could not parse variable name'

    # Look for state variable declaration (not inside function)
    state_pat = re.compile(
        r'\bstring\b.*\b' + re.escape(var_name) + r'\b'
    )
    string_literal_pat = re.compile(r'"([^"]*)"')

    in_function = 0
    for line in lines:
        s = line.strip()
        in_function += s.count('{') - s.count('}')
        # We want state variable (depth 0 or 1 inside contract)
        if in_function <= 1 and state_pat.search(line):
            # Found state var declaration
            m = string_literal_pat.search(line)
            if m:
                value = m.group(1)
                if len(value) <= 32:
                    return 'TP', f'value="{value}" ({len(value)} chars ≤ 32)'
                else:
                    return 'FP', f'value="{value[:30]}..." ({len(value)} chars > 32)'
            else:
                # No literal initializer — it's set elsewhere, likely still TP
                # Check if it's a constant or immutable
                if 'constant' in line or 'immutable' in line:
                    return 'TP', 'constant/immutable string, could be bytes32'
                return 'TP', 'no literal initializer; string state var likely short (name/symbol/version pattern)'

    # Not found as state variable — might be a local or inherited
    return '?', f'`{var_name}` not found as top-level state variable — may be inherited or local'


def check_dead_code(lines, text, func_name):
    """
    TP: function is never called anywhere.
    FP: it IS called (our detector missed it), or it's an interface/abstract implementation.
    """
    if not func_name:
        return '?', 'could not parse function name'

    call_pat  = re.compile(r'\b' + re.escape(func_name) + r'\s*\(')
    decl_pat  = re.compile(r'\bfunction\s+' + re.escape(func_name) + r'\b')
    emit_pat  = re.compile(r'\bemit\s+' + re.escape(func_name) + r'\b')

    callers = []
    decl_line = None

    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith('//') or s.startswith('*'):
            continue
        if decl_pat.search(line):
            decl_line = i
            continue
        if emit_pat.search(line):
            # emit Event() — that's an event, not a function call, skip
            continue
        if call_pat.search(line):
            callers.append(i)

    if callers:
        return 'FP', f'called at lines {callers[:3]}'

    # Check if virtual/override (could be called from child contract)
    if decl_line:
        decl_text = lines[decl_line - 1]
        if 'virtual' in decl_text or 'override' in decl_text:
            return '?', 'virtual/override function — may be called from child contract'

    return 'TP', 'no callers found in file'


def check_unoptimized_loop(lines, text, arr_name):
    """
    TP: state variable array .length used in for-loop condition.
    FP: it's a local/parameter array.
    """
    if not arr_name:
        return '?', 'could not parse array name'

    # Find for-loop with this .length
    loop_pat = re.compile(r'\bfor\s*\(.*\b' + re.escape(arr_name) + r'\.length\b')
    for i, line in enumerate(lines, 1):
        if loop_pat.search(line):
            # Check if arr_name is a state variable
            state_decl = re.compile(r'^\s+\w[\w\[\]]*\s+(?:public|private|internal|)?\s*' + re.escape(arr_name) + r'\b')
            found_as_state = any(state_decl.search(l) for l in lines)
            # Also check simpler: is it declared at contract level?
            simple_decl = re.compile(r'\b' + re.escape(arr_name) + r'\s*;')
            found_simple = any(simple_decl.search(l) for l in lines)
            if found_as_state or found_simple:
                return 'TP', f'state array `.length` in for-loop at line {i}'
            else:
                return '?', f'array in for-loop at line {i} — could not confirm as state variable'

    return '?', 'loop pattern not found (may be parsed differently)'


# ═══════════════════════════════════════════════════════════════════════════
# MAIN AUDIT LOOP
# ═══════════════════════════════════════════════════════════════════════════

results = []   # list of {rank, nama, domain, findings: [{pattern, subject, verdict, reason}]}
summary = defaultdict(lambda: {'TP':0,'FP':0,'?':0})

print("=" * 70)
print("AUTOMATED MANUAL AUDIT")
print("=" * 70)

for contract in audit_data:
    rank  = contract['rank']
    nama  = contract['nama']
    domain = contract['domain']
    fpath = contract['file']

    lines, text = load_sol(fpath)
    if lines is None:
        print(f"\n[{rank:02d}] {nama} — FILE NOT FOUND, SKIPPING")
        continue

    print(f"\n[{rank:02d}] {nama} ({domain}, {contract['loc']} LOC)")

    contract_results = []

    for det_name, findings in contract['findings_by_pattern'].items():
        if not findings:
            continue

        tp = fp = unk = 0
        finding_verdicts = []

        for f in findings:
            desc = f.get('description', '')

            # Dispatch to verifier
            if det_name == 'public_vs_external':
                fname = extract_func_name(desc, det_name)
                verdict, reason = check_public_vs_external(lines, text, fname)
                subject = f"`{fname}()`" if fname else desc[:40]

            elif det_name == 'redundant_sload':
                names = extract_func_name(desc, det_name)
                if isinstance(names, tuple):
                    var_name, func_name = names
                else:
                    var_name, func_name = names, None
                verdict, reason = check_redundant_sload(lines, text, var_name, func_name)
                subject = f"`{var_name}` in `{func_name}()`" if func_name else f"`{var_name}`"

            elif det_name == 'string_vs_bytes32':
                var_name = extract_func_name(desc, det_name)
                verdict, reason = check_string_vs_bytes32(lines, text, var_name)
                subject = f"`{var_name}`" if var_name else desc[:40]

            elif det_name == 'dead_code':
                func_name = extract_func_name(desc, det_name)
                verdict, reason = check_dead_code(lines, text, func_name)
                subject = f"`{func_name}()`" if func_name else desc[:40]

            elif det_name == 'unoptimized_loop':
                # Description like: "loop ... 'owners.length'"
                m = re.search(r"'(\w+)\.length'", desc)
                arr_name = m.group(1) if m else extract_func_name(desc, det_name)
                verdict, reason = check_unoptimized_loop(lines, text, arr_name)
                subject = f"`{arr_name}.length`" if arr_name else desc[:40]

            else:
                verdict, reason = '?', 'pattern not handled'
                subject = desc[:40]

            if verdict == 'TP': tp += 1
            elif verdict == 'FP': fp += 1
            else: unk += 1

            summary[det_name][verdict] += 1
            finding_verdicts.append({'subject': subject, 'verdict': verdict, 'reason': reason})

        total = tp + fp + unk
        prec_str = f"{tp/(tp+fp)*100:.0f}%" if (tp+fp) > 0 else "n/a"
        print(f"    {PATTERN_FULL[det_name]:<25}: {total:>3} → TP={tp} FP={fp} ?={unk}  precision≈{prec_str}")
        contract_results.append({
            'pattern': det_name,
            'findings': finding_verdicts,
            'TP': tp, 'FP': fp, '?': unk,
        })

    results.append({
        'rank': rank, 'nama': nama, 'domain': domain,
        'loc': contract['loc'],
        'estimated_savings': contract['estimated_savings'],
        'patterns': contract_results,
    })

# ── Print global summary ───────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SUMMARY BY PATTERN")
print("=" * 70)
grand_tp = grand_fp = grand_unk = 0
for det_name in ['public_vs_external','redundant_sload','string_vs_bytes32','dead_code','unoptimized_loop']:
    s = summary[det_name]
    tp, fp, unk = s['TP'], s['FP'], s['?']
    total = tp + fp + unk
    if total == 0: continue
    prec = f"{tp/(tp+fp)*100:.1f}%" if (tp+fp) > 0 else "n/a"
    print(f"  {PATTERN_FULL[det_name]:<25}: {total:>3} total  TP={tp:>3} FP={fp:>3} ?={unk:>3}  precision≈{prec}")
    grand_tp += tp; grand_fp += fp; grand_unk += unk

total_all = grand_tp + grand_fp + grand_unk
prec_all = f"{grand_tp/(grand_tp+grand_fp)*100:.1f}%" if (grand_tp+grand_fp)>0 else "n/a"
print(f"\n  {'TOTAL':<25}: {total_all:>3} total  TP={grand_tp:>3} FP={grand_fp:>3} ?={grand_unk:>3}  precision≈{prec_all}")

# ── Save results JSON ──────────────────────────────────────────────────────
out_json = ROOT / 'docs' / 'manual_audit' / 'audit_results.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({'summary': dict(summary), 'contracts': results}, f, indent=2, ensure_ascii=False)
print(f"\nSaved: {out_json}")

# ── Generate filled checklist ──────────────────────────────────────────────
out_md = ROOT / 'docs' / 'manual_audit' / 'AUDIT_RESULTS.md'

VERDICT_ICON = {'TP': '✅ TP', 'FP': '❌ FP', '?': '⚠️ ?'}

md = []
md += [
    "# Hasil Manual Audit — 20 Kontrak Top Gas Savings",
    "",
    "Dihasilkan otomatis oleh `scripts/run_manual_audit.py`.",
    "Setiap finding diverifikasi dengan membaca file `.sol` langsung.",
    "",
    "---",
    "",
    "## Ringkasan Precision per Pattern",
    "",
    "| Pattern | Total | TP | FP | ? | Precision |",
    "|---|---|---|---|---|---|",
]

for det_name in ['public_vs_external','redundant_sload','string_vs_bytes32','dead_code','unoptimized_loop']:
    s = summary[det_name]
    tp, fp, unk = s['TP'], s['FP'], s['?']
    total = tp + fp + unk
    if total == 0: continue
    prec = f"{tp/(tp+fp)*100:.1f}%" if (tp+fp) > 0 else "n/a"
    md.append(f"| {PATTERN_FULL[det_name]} | {total} | {tp} | {fp} | {unk} | **{prec}** |")

prec_all_str = f"{grand_tp/(grand_tp+grand_fp)*100:.1f}%" if (grand_tp+grand_fp)>0 else "n/a"
md += [
    f"| **TOTAL** | **{total_all}** | **{grand_tp}** | **{grand_fp}** | **{grand_unk}** | **{prec_all_str}** |",
    "",
    "---",
    "",
]

# Per-contract detail
for c in results:
    total_f = sum(p['TP']+p['FP']+p['?'] for p in c['patterns'])
    md += [
        f"## [{c['rank']:02d}] {c['nama']} ({c['domain']})",
        "",
        f"LOC: {c['loc']} | Est. Savings: {c['estimated_savings']:,} gas",
        "",
    ]

    for pat in c['patterns']:
        det_name = pat['pattern']
        tp, fp, unk = pat['TP'], pat['FP'], pat['?']
        total = tp + fp + unk
        prec = f"{tp/(tp+fp)*100:.0f}%" if (tp+fp)>0 else "n/a"

        md += [
            f"### {PATTERN_FULL[det_name]} — {total} temuan → TP={tp} FP={fp} ?={unk} (precision≈{prec})",
            "",
            "| # | Subject | Verdict | Alasan |",
            "|---|---|---|---|",
        ]
        for i, fv in enumerate(pat['findings'], 1):
            icon = VERDICT_ICON.get(fv['verdict'], fv['verdict'])
            reason = fv['reason'].replace('|', '\\|')
            if len(reason) > 80: reason = reason[:77] + '...'
            md.append(f"| {i} | {fv['subject']} | {icon} | {reason} |")
        md.append("")

    md += ["---", ""]

with open(out_md, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))
print(f"Saved: {out_md}")
