"""
Detector: Unchecked Arithmetic
Deteksi operasi +/- di dalam loop yang kemungkinan besar tidak overflow,
tapi tidak dibungkus `unchecked {}` (Solidity >=0.8.0).
Contoh paling umum: loop counter `i++` atau `i += 1`.
"""
import re
from src.ast_parser import find_nodes, walk_ast


def _has_checked_arithmetic(ast):
    """Return True jika kontrak menggunakan pragma solidity >=0.8."""
    for node in find_nodes(ast, 'PragmaDirective'):
        # Modern AST stores version in 'literals' list; old compact uses 'value'
        literals = node.get('literals', [])
        text = ' '.join(str(l) for l in literals) if literals else node.get('value', '')
        m = re.search(r'(\d+)\.(\d+)', text)
        if m:
            major, minor = int(m.group(1)), int(m.group(2))
            if major > 0 or minor >= 8:
                return True
    return False


def _is_inside_unchecked(node, ast):
    """Heuristik sederhana — tidak bisa traverse parent di AST flat, jadi cek via UncheckedStatement nodes."""
    return False  # diisi lewat konteks walk di bawah


def _find_loop_increments(loop_node):
    """Cari operasi aritmatika di loop body yang BUKAN di dalam unchecked block.

    Mencakup:
      BinaryOperation  operator +/-         → a + b, a - b
      Assignment       operator +=/-=       → x += 1, x -= 1
      UnaryOperation   operator ++/--       → i++, ++i
    """
    findings_local = []
    unchecked_src_ranges = []  # list of (start_byte, end_byte)

    def collect_unchecked(n, depth):
        if n.get('nodeType') == 'UncheckedStatement':
            src = n.get('src', '')
            try:
                parts = src.split(':')
                start = int(parts[0])
                length = int(parts[1])
                unchecked_src_ranges.append((start, start + length))
            except Exception:
                pass

    walk_ast(loop_node, collect_unchecked)

    def _in_unchecked(src_str):
        try:
            parts = src_str.split(':')
            pos = int(parts[0])
            return any(s <= pos <= e for s, e in unchecked_src_ranges)
        except Exception:
            return False

    def visit(n, depth):
        nt = n.get('nodeType', '')
        op = n.get('operator', '')
        src = n.get('src', '')

        is_arith = (
            (nt == 'BinaryOperation' and op in ('+', '-'))
            or (nt == 'Assignment' and op in ('+=', '-='))
            or (nt == 'UnaryOperation' and op in ('++', '--'))
        )
        if is_arith and not _in_unchecked(src):
            line = n.get('loc', {}).get('start', {}).get('line')
            findings_local.append(line)

    walk_ast(loop_node.get('body', {}), visit)
    # Also check loop expression (i++ lives there, not in body)
    loop_expr = loop_node.get('loopExpression') or loop_node.get('loopExpression', {})
    if isinstance(loop_expr, dict):
        walk_ast(loop_expr, visit)
    return findings_local


def detect(ast):
    if not isinstance(ast, dict):
        return []

    if not _has_checked_arithmetic(ast):
        return []

    findings = []
    for loop in find_nodes(ast, 'ForStatement'):
        lines = _find_loop_increments(loop)
        seen = set()
        for line in lines:
            if line not in seen:
                seen.add(line)
                findings.append({
                    'line': line,
                    'description': (
                        f"Unchecked Arithmetic: operasi aritmatika di dalam loop (baris {line}) "
                        f"tidak dibungkus `unchecked {{}}`. Jika tidak mungkin overflow/underflow, "
                        f"bungkus untuk hemat ~20 gas per iterasi."
                    ),
                })

    return findings
