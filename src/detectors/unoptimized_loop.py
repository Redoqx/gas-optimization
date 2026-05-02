"""
Detector: Unoptimized Loop
Deteksi loop yang membaca `.length` dari state variable array di setiap iterasi.
"""
from src.ast_parser import find_nodes, walk_ast


def _collect_state_var_names(ast):
    state_vars = set()
    for sv in find_nodes(ast, 'StateVariableDeclaration'):
        for decl in sv.get('variables', []):
            name = decl.get('name')
            if name:
                state_vars.add(name)
    return state_vars


def _has_storage_length_in_condition(for_node, state_vars):
    """
    Cek apakah kondisi ForStatement mengandung <stateVar>.length.
    Node structure: for.conditionExpression -> BinaryOperation -> MemberAccess(.length)
    """
    cond = for_node.get('conditionExpression')
    if not cond:
        return None

    found = []

    def visit(n, depth):
        if n.get('nodeType') == 'MemberAccess' and n.get('memberName') == 'length':
            expr = n.get('expression', {})
            var_name = expr.get('name', '')
            if var_name in state_vars:
                found.append(var_name)

    walk_ast(cond, visit)
    return found[0] if found else None


def detect(ast):
    if not isinstance(ast, dict):
        return []

    state_vars = _collect_state_var_names(ast)
    if not state_vars:
        return []

    findings = []
    for loop in find_nodes(ast, 'ForStatement'):
        var_name = _has_storage_length_in_condition(loop, state_vars)
        if var_name:
            line = loop.get('loc', {}).get('start', {}).get('line')
            findings.append({
                'line': line,
                'description': (
                    f"Unoptimized Loop: '{var_name}.length' dibaca dari storage "
                    f"di setiap iterasi loop. Cache ke `uint len = {var_name}.length` "
                    f"sebelum loop."
                ),
            })
    return findings
