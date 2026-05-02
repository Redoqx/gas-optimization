"""
Detector: String vs Bytes32
Deteksi deklarasi `string` yang berpotensi diganti `bytes32` (teks pendek ≤ 32 karakter).
Heuristik: state variable atau parameter bertipe `string` tanpa inisialisasi panjang dinamis.
"""
from src.ast_parser import find_nodes


def _is_string_type(type_name_node):
    if not isinstance(type_name_node, dict):
        return False
    if type_name_node.get('nodeType') == 'ElementaryTypeName':
        return type_name_node.get('name') == 'string'
    return False


def detect(ast):
    if not isinstance(ast, dict):
        return []

    findings = []

    # State variables dengan tipe string
    for sv in find_nodes(ast, 'StateVariableDeclaration'):
        for decl in sv.get('variables', []):
            type_name = decl.get('typeName', {})
            if _is_string_type(type_name):
                line = decl.get('loc', {}).get('start', {}).get('line')
                var_name = decl.get('name', '<unknown>')
                findings.append({
                    'line': line,
                    'description': (
                        f"String vs Bytes32: state variable '{var_name}' bertipe `string`. "
                        f"Jika nilainya selalu ≤32 karakter, ganti ke `bytes32` untuk hemat gas."
                    ),
                })

    # Parameter fungsi bertipe string
    for func in find_nodes(ast, 'FunctionDefinition'):
        params = func.get('parameters', {}).get('parameters', [])
        for p in params:
            type_name = p.get('typeName', {})
            if _is_string_type(type_name):
                line = p.get('loc', {}).get('start', {}).get('line')
                param_name = p.get('name', '<unknown>')
                func_name = func.get('name', '<anonymous>')
                findings.append({
                    'line': line,
                    'description': (
                        f"String vs Bytes32: parameter '{param_name}' di fungsi '{func_name}' "
                        f"bertipe `string`. Pertimbangkan `bytes32` jika panjang terbatas."
                    ),
                })

    return findings
