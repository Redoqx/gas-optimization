"""
Detector: Dead Code
Deteksi fungsi internal/private yang tidak pernah dipanggil oleh fungsi lain dalam kontrak.
"""
from src.ast_parser import find_nodes, walk_ast


def _collect_all_calls(ast):
    """Kumpulkan semua nama fungsi yang dipanggil di mana pun dalam AST."""
    called = set()

    def visit(n, depth):
        if n.get('nodeType') == 'FunctionCall':
            expr = n.get('expression', {})
            if expr.get('nodeType') == 'Identifier':
                called.add(expr.get('name', ''))
            # method calls: foo.bar() — ambil memberName
            elif expr.get('nodeType') == 'MemberAccess':
                called.add(expr.get('memberName', ''))

    walk_ast(ast, visit)
    return called


def detect(ast):
    if not isinstance(ast, dict):
        return []

    called_names = _collect_all_calls(ast)

    findings = []
    for func in find_nodes(ast, 'FunctionDefinition'):
        visibility = func.get('visibility', '')
        name = func.get('name', '')
        is_constructor = func.get('isConstructor', False)

        if visibility not in ('internal', 'private'):
            continue
        if is_constructor or not name:
            continue

        if name not in called_names:
            line = func.get('loc', {}).get('start', {}).get('line')
            findings.append({
                'line': line,
                'description': (
                    f"Dead Code: fungsi '{name}' ({visibility}) tidak pernah dipanggil "
                    f"dalam kontrak. Pertimbangkan untuk menghapus agar hemat deployment gas."
                ),
            })

    return findings
