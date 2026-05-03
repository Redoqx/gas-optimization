"""
Refactorer: aplikasikan patch source-level untuk anti-pattern yang terdeteksi.

Didukung:
  - public_vs_external  : ubah `public` → `external` pada fungsi yang di-flag
  - unoptimized_loop    : cache `.length` ke variabel lokal sebelum loop
  - redundant_sload     : (heuristik) tambah komentar TODO — full patch butuh scope analysis
"""
import re
from pathlib import Path


# ── Helper: ekstrak nama dari deskripsi detector ──────────────────────────────

def _func_name_from(desc):
    """Ambil nama fungsi dari description string detector."""
    m = re.search(r"fungsi '([^']+)'", desc)
    return m.group(1) if m else None


def _loop_var_from(desc):
    """Ambil nama array dari unoptimized_loop description ('arr.length')."""
    m = re.search(r"'([^'.]+)\.length'", desc)
    return m.group(1) if m else None


def _sload_var_from(desc):
    """Ambil nama state variable dari redundant_sload description."""
    m = re.search(r"Redundant SLOAD: '([^']+)'", desc)
    return m.group(1) if m else None


# ── 1. Public → External ─────────────────────────────────────────────────────

def refactor_public_to_external(source, findings):
    """
    Ubah `public` menjadi `external` pada fungsi yang di-flag.
    Hanya mengubah keyword visibility di baris deklarasi fungsi.
    Jika line number tidak tersedia (kontrak format lama), scan seluruh file.
    """
    lines = source.splitlines()
    for f in findings:
        func_name = _func_name_from(f.get('description', ''))
        if not func_name:
            continue
        line_no = f.get('line')
        # Jika ada line hint, cari ± 3 baris; jika tidak, scan seluruh file
        lo = max(0, line_no - 3) if line_no else 0
        hi = min(len(lines), line_no + 3) if line_no else len(lines)
        pattern = r'(\bfunction\s+' + re.escape(func_name) + r'\b[^{]*?)\bpublic\b'
        for i in range(lo, hi):
            new_line, n = re.subn(pattern, r'\1external', lines[i], count=1)
            if n:
                lines[i] = new_line
                break
    return '\n'.join(lines)


# ── 2. Unoptimized Loop → cache length ───────────────────────────────────────

def refactor_cache_loop_length(source, findings):
    """
    Insert `uint256 _<var>Len = <var>.length;` sebelum for-loop yang di-flag,
    dan ganti `<var>.length` di kondisi loop dengan nama cache.

    Patch diterapkan dari bawah ke atas agar nomor baris tidak bergeser.
    Jika line number tidak tersedia, cari loop dengan `<var>.length` di seluruh file.
    """
    lines = source.splitlines()
    # Sort reverse by line (put None at front to process last → bottom-up remains safe)
    sorted_findings = sorted(
        findings,
        key=lambda f: f.get('line') or 0,
        reverse=True
    )
    for f in sorted_findings:
        arr_name = _loop_var_from(f.get('description', ''))
        if not arr_name:
            continue
        line_no = f.get('line')

        # Search range: around hint or whole file (bottom-up safe since reverse sorted)
        if line_no is not None:
            lo = max(0, line_no - 2)
            hi = min(len(lines), line_no + 4)
        else:
            lo, hi = 0, len(lines)

        # Find for-loop line that contains <arr_name>.length (exact word boundary)
        length_pat = re.compile(r'\b' + re.escape(arr_name) + r'\.length\b')
        for_idx = None
        for i in range(lo, hi):
            if re.search(r'\bfor\s*\(', lines[i]) and length_pat.search(lines[i]):
                for_idx = i
                break
        if for_idx is None:
            continue

        cache_name = f'_{arr_name}Len'
        indent = re.match(r'^(\s*)', lines[for_idx]).group(1)
        cache_line = f'{indent}uint256 {cache_name} = {arr_name}.length;'

        lines[for_idx] = length_pat.sub(cache_name, lines[for_idx])
        lines.insert(for_idx, cache_line)

    return '\n'.join(lines)


# ── 3. Redundant SLOAD → TODO komentar (safe fallback) ───────────────────────

def refactor_sload_add_comments(source, findings):
    """
    Tambahkan komentar `// TODO: cache <var> ke local` pada baris fungsi
    yang di-flag redundant_sload.

    Full auto-patch tidak aman tanpa full data-flow analysis — komentar
    memberi petunjuk untuk refactoring manual.
    """
    lines = source.splitlines()
    for f in findings:
        var_name  = _sload_var_from(f.get('description', ''))
        line_no   = f.get('line')
        if not var_name or line_no is None:
            continue
        idx = line_no - 1
        if 0 <= idx < len(lines):
            todo = f'  // TODO: cache `{var_name}` ke local var untuk hemat SLOAD'
            if todo.strip() not in lines[idx]:
                lines[idx] += todo
    return '\n'.join(lines)


# ── Entry point ───────────────────────────────────────────────────────────────

def apply_all_refactors(filepath, findings_by_type):
    """
    Aplikasikan semua refactor yang berlaku ke file .sol.

    Parameters
    ----------
    filepath : str | Path
    findings_by_type : dict  { detector_name: [finding, ...] }

    Returns
    -------
    (refactored_source: str, summary: dict)
        summary = { detector_name: n_patches_applied }
    """
    source  = Path(filepath).read_text(encoding='utf-8')
    summary = {}

    if findings_by_type.get('public_vs_external'):
        source = refactor_public_to_external(source, findings_by_type['public_vs_external'])
        summary['public_vs_external'] = len(findings_by_type['public_vs_external'])

    if findings_by_type.get('unoptimized_loop'):
        source = refactor_cache_loop_length(source, findings_by_type['unoptimized_loop'])
        summary['unoptimized_loop'] = len(findings_by_type['unoptimized_loop'])

    if findings_by_type.get('redundant_sload'):
        source = refactor_sload_add_comments(source, findings_by_type['redundant_sload'])
        summary['redundant_sload'] = len(findings_by_type['redundant_sload'])

    return source, summary


def diff_summary(original, refactored):
    """Hitung jumlah baris yang berubah antara original dan refactored."""
    orig_lines = original.splitlines()
    refc_lines = refactored.splitlines()
    changed = sum(1 for a, b in zip(orig_lines, refc_lines) if a != b)
    added   = max(0, len(refc_lines) - len(orig_lines))
    return {'lines_changed': changed, 'lines_added': added}
