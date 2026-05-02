"""
Detector: Redundant SLOAD
Deteksi state variable yang dibaca >1x di dalam fungsi yang sama tanpa cache lokal.
"""
from src.ast_parser import find_nodes, walk_ast


def _collect_state_var_names(ast):
    """Kumpulkan semua nama state variable dari kontrak."""
    state_vars = set()
    for sv in find_nodes(ast, 'StateVariableDeclaration'):
        for decl in sv.get('variables', []):
            name = decl.get('name')
            if name:
                state_vars.add(name)
    return state_vars


def _count_identifier_reads(node, state_vars):
    """Hitung berapa kali tiap state var dibaca dalam subtree node."""
    counts = {}
    def visit(n, depth):
        if n.get('nodeType') == 'Identifier':
            name = n.get('name', '')
            if name in state_vars:
                counts[name] = counts.get(name, 0) + 1
    walk_ast(node, visit)
    return counts


def detect(ast):
    if not isinstance(ast, dict):
        return []

    state_vars = _collect_state_var_names(ast)
    if not state_vars:
        return []

    findings = []
    for func in find_nodes(ast, 'FunctionDefinition'):
        body = func.get('body')
        if not body:
            continue
        counts = _count_identifier_reads(body, state_vars)
        for var_name, count in counts.items():
            if count > 1:
                line = func.get('loc', {}).get('start', {}).get('line')
                findings.append({
                    'line': line,
                    'description': (
                        f"Redundant SLOAD: '{var_name}' dibaca {count}x "
                        f"di fungsi '{func.get('name', '<anonymous>')}'. "
                        f"Cache ke variabel lokal untuk hemat gas."
                    ),
                })
    return findings
