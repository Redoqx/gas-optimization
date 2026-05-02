"""
Detector: Public vs External
Deteksi fungsi `public` yang tidak dipanggil secara internal — lebih efisien jika `external`.
`external` lebih hemat gas karena argumen dibaca langsung dari calldata, bukan dicopy ke memory.
"""
from src.ast_parser import find_nodes, walk_ast


def _collect_internal_calls(ast):
    """Kumpulkan semua nama fungsi yang dipanggil secara internal (FunctionCall dengan Identifier)."""
    called = set()

    def visit(n, depth):
        if n.get('nodeType') == 'FunctionCall':
            expr = n.get('expression', {})
            # Panggilan langsung: foo()
            if expr.get('nodeType') == 'Identifier':
                called.add(expr.get('name', ''))
            # Panggilan via this.foo() tidak dihitung — itu external call

    walk_ast(ast, visit)
    return called


def detect(ast):
    if not isinstance(ast, dict):
        return []

    internal_calls = _collect_internal_calls(ast)

    findings = []
    for func in find_nodes(ast, 'FunctionDefinition'):
        visibility = func.get('visibility', '')
        name = func.get('name', '')
        is_constructor = func.get('isConstructor', False)

        if visibility != 'public' or is_constructor or not name:
            continue

        if name not in internal_calls:
            line = func.get('loc', {}).get('start', {}).get('line')
            findings.append({
                'line': line,
                'description': (
                    f"Public vs External: fungsi '{name}' dideklarasikan `public` "
                    f"tapi tidak pernah dipanggil secara internal. "
                    f"Ubah ke `external` untuk hemat gas pada parameter calldata."
                ),
            })

    return findings
