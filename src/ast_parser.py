import re
import tempfile
from packaging.version import Version as PkgVersion
from pathlib import Path
import solcx

SOLC_MAP = {
    '0.4': '0.4.26',
    '0.5': '0.5.17',
    '0.6': '0.6.12',
    '0.7': '0.7.6',
    '0.8': '0.8.20',
}


def detect_solc_ver(source):
    m = re.search(r'pragma solidity\s*=?\s*(\d+\.\d+\.\d+)\s*;', source)
    if m:
        return m.group(1)
    m = re.search(r'pragma solidity\s+[>=^<~]*\s*(\d+\.\d+)', source)
    if not m:
        return '0.8.20'
    major_minor = '.'.join(m.group(1).split('.')[:2])
    return SOLC_MAP.get(major_minor, '0.8.20')


def dedup_pragma(source):
    seen = False
    lines = []
    for line in source.splitlines():
        if re.match(r'\s*pragma solidity', line):
            if not seen:
                lines.append(line)
                seen = True
        else:
            lines.append(line)
    return '\n'.join(lines)


def parse_multifile(source):
    parts = re.split(r'// === File: (.+?) ===', source)
    if len(parts) <= 1:
        return None
    files = {}
    for i in range(1, len(parts) - 1, 2):
        files[parts[i].strip()] = parts[i + 1]
    return files or None


# ---------------------------------------------------------------------------
# Compact AST normalizer  (solc < ~0.6 returns "compact JSON" format that
# uses name/children/attributes instead of nodeType/named-fields)
# ---------------------------------------------------------------------------

def _is_old_format(node):
    return isinstance(node, dict) and not node.get('nodeType') and 'name' in node


def _wrap_state_vars(nodes):
    """Wrap old-format state VariableDeclaration nodes into StateVariableDeclaration."""
    result = []
    for node in nodes:
        if (isinstance(node, dict)
                and node.get('nodeType') == 'VariableDeclaration'
                and node.get('stateVariable')):
            result.append({
                'nodeType': 'StateVariableDeclaration',
                'variables': [node],
                'initialValue': node.get('value'),
            })
        else:
            result.append(node)
    return result


def _normalize_compact(node):
    """Recursively convert old compact AST to modern nodeType-based AST."""
    if not isinstance(node, dict):
        return node

    # Already modern format — recurse only
    if node.get('nodeType'):
        out = {}
        for k, v in node.items():
            if isinstance(v, dict):
                out[k] = _normalize_compact(v)
            elif isinstance(v, list):
                out[k] = [_normalize_compact(i) if isinstance(i, dict) else i for i in v]
            else:
                out[k] = v
        return out

    node_type = node.get('name', '')
    attrs = node.get('attributes') or {}
    # Preserve None slots so index-based child(i) is stable
    raw_children = node.get('children') or []
    children = [_normalize_compact(c) if isinstance(c, dict) else None for c in raw_children]

    def child(i):
        return children[i] if i < len(children) else None

    def dict_children():
        return [c for c in children if c is not None]

    result = {'nodeType': node_type, 'src': node.get('src', ''), 'id': node.get('id')}

    if node_type in ('SourceUnit',):
        result['absolutePath'] = attrs.get('absolutePath', '')
        result['nodes'] = _wrap_state_vars(dict_children())

    elif node_type == 'ContractDefinition':
        result['name'] = attrs.get('name', '')
        result['contractKind'] = attrs.get('contractKind', 'contract')
        result['nodes'] = _wrap_state_vars(dict_children())

    elif node_type == 'FunctionDefinition':
        result['name'] = attrs.get('name', '')
        result['visibility'] = attrs.get('visibility', 'public')
        result['stateMutability'] = attrs.get('stateMutability', '')
        result['isConstructor'] = attrs.get('isConstructor', False)
        result['implemented'] = attrs.get('implemented', True)
        params = child(0)
        result['parameters'] = params or {'nodeType': 'ParameterList', 'parameters': []}
        body = None
        for c in reversed(dict_children()):
            if c.get('nodeType') == 'Block':
                body = c
                break
        result['body'] = body

    elif node_type == 'ParameterList':
        result['parameters'] = dict_children()

    elif node_type == 'VariableDeclaration':
        result['name'] = attrs.get('name', '')
        result['visibility'] = attrs.get('visibility', 'internal')
        result['stateVariable'] = attrs.get('stateVariable', False)
        result['storageLocation'] = attrs.get('storageLocation', 'default')
        result['typeName'] = child(0)
        result['value'] = child(1)

    elif node_type == 'ElementaryTypeName':
        result['name'] = attrs.get('name', '')

    elif node_type == 'ArrayTypeName':
        result['baseType'] = child(0)
        result['length'] = child(1)

    elif node_type == 'Mapping':
        result['keyType'] = child(0)
        result['valueType'] = child(1)

    elif node_type == 'UserDefinedTypeName':
        result['namePath'] = attrs.get('name', '')
        result['name'] = attrs.get('name', '')

    elif node_type == 'Block':
        result['statements'] = dict_children()

    elif node_type == 'ForStatement':
        # children order: [init, condition, loopExpr, body]
        result['initializationExpression'] = child(0)
        result['conditionExpression'] = child(1)
        result['loopExpression'] = child(2)
        result['body'] = child(3)

    elif node_type == 'WhileStatement':
        result['condition'] = child(0)
        result['body'] = child(1)

    elif node_type == 'IfStatement':
        result['condition'] = child(0)
        result['trueBody'] = child(1)
        result['falseBody'] = child(2)

    elif node_type == 'ExpressionStatement':
        result['expression'] = child(0)

    elif node_type == 'VariableDeclarationStatement':
        result['declarations'] = [child(0)]
        result['initialValue'] = child(1)

    elif node_type == 'Return':
        result['expression'] = child(0)

    elif node_type == 'Assignment':
        result['operator'] = attrs.get('operator', '=')
        result['leftHandSide'] = child(0)
        result['rightHandSide'] = child(1)

    elif node_type == 'BinaryOperation':
        result['operator'] = attrs.get('operator', '')
        result['leftExpression'] = child(0)
        result['rightExpression'] = child(1)

    elif node_type == 'UnaryOperation':
        result['operator'] = attrs.get('operator', '')
        result['subExpression'] = child(0)
        result['prefix'] = attrs.get('prefix', True)

    elif node_type == 'FunctionCall':
        result['expression'] = child(0)
        result['arguments'] = [c for c in children[1:] if c is not None]

    elif node_type == 'MemberAccess':
        result['expression'] = child(0)
        result['memberName'] = attrs.get('member_name', '')

    elif node_type == 'Identifier':
        result['name'] = attrs.get('value', '')

    elif node_type == 'IndexAccess':
        result['baseExpression'] = child(0)
        result['indexExpression'] = child(1)

    elif node_type == 'TupleExpression':
        result['components'] = dict_children()

    elif node_type in ('NumberLiteral', 'StringLiteral', 'BooleanLiteral', 'HexLiteral'):
        result['value'] = attrs.get('value', attrs.get('hexvalue', ''))

    elif node_type == 'Conditional':
        result['condition'] = child(0)
        result['trueExpression'] = child(1)
        result['falseExpression'] = child(2)

    elif node_type in ('EventDefinition', 'ModifierDefinition',
                       'StructDefinition', 'EnumDefinition'):
        result['name'] = attrs.get('name', '')
        result['nodes'] = dict_children()

    elif node_type == 'PragmaDirective':
        result['literals'] = attrs.get('literals', [])

    elif node_type == 'ImportDirective':
        result['file'] = attrs.get('file', '')

    elif node_type == 'EmitStatement':
        result['eventCall'] = child(0)

    elif node_type == 'UsingForDirective':
        result['libraryName'] = child(0)
        result['typeName'] = child(1)

    elif node_type == 'InheritanceSpecifier':
        result['baseName'] = child(0)

    else:
        result.update(attrs)
        if dict_children():
            result['_children'] = dict_children()

    return result


# ---------------------------------------------------------------------------
# Core AST functions
# ---------------------------------------------------------------------------

def smart_compile_ast(filepath):
    src = Path(filepath).read_text(encoding='utf-8')
    if 'pragma solidity' not in src:
        return None

    ver = detect_solc_ver(src)
    try:
        if PkgVersion(ver) < PkgVersion('0.4.11'):
            ver = '0.4.26'
    except Exception:
        pass

    installed = [str(v) for v in solcx.get_installed_solc_versions()]
    if ver not in installed:
        solcx.install_solc(ver)

    files = parse_multifile(src)

    def _maybe_normalize(ast_node):
        if _is_old_format(ast_node):
            return _normalize_compact(ast_node)
        return ast_node

    if files:
        try:
            inp = {
                "language": "Solidity",
                "sources": {n: {"content": c} for n, c in files.items()},
                "settings": {
                    "optimizer": {"enabled": False},
                    "outputSelection": {"*": {"": ["ast"]}},
                },
            }
            out = solcx.compile_standard(inp, solc_version=ver)
            return _maybe_normalize(out['sources'][next(iter(out['sources']))]['ast'])
        except Exception:
            pass

        try:
            with tempfile.TemporaryDirectory() as td:
                tdp = Path(td)
                for name, content in files.items():
                    fp = tdp / name
                    fp.parent.mkdir(parents=True, exist_ok=True)
                    fp.write_text(content, encoding='utf-8')
                main_fp = str(tdp / next(iter(files)))
                out = solcx.compile_files(
                    [main_fp],
                    output_values=['ast'],
                    solc_version=ver,
                    optimize=False,
                    allow_paths=[td],
                )
                if out:
                    return _maybe_normalize(list(out.values())[0]['ast'])
        except Exception:
            pass
    else:
        src_clean = dedup_pragma(src)
        try:
            out = solcx.compile_source(
                src_clean, output_values=['ast'], solc_version=ver, optimize=False
            )
            return _maybe_normalize(list(out.values())[0]['ast'])
        except Exception:
            pass

    try:
        main_src = src if not files else list(files.values())[0]
        stripped = re.sub(r'^\s*import\s+[^;]+;', '', main_src, flags=re.MULTILINE)
        stripped = dedup_pragma(stripped)
        out = solcx.compile_source(
            stripped, output_values=['ast'], solc_version=ver, optimize=False
        )
        if out:
            return _maybe_normalize(list(out.values())[0]['ast'])
    except Exception:
        pass

    return None


def generate_ast(filepath):
    return smart_compile_ast(filepath)


def walk_ast(node, callback, depth=0):
    if not isinstance(node, dict):
        return
    callback(node, depth)
    for value in node.values():
        if isinstance(value, dict):
            walk_ast(value, callback, depth + 1)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    walk_ast(item, callback, depth + 1)


def find_nodes(ast, target_type):
    result = []

    def visit(n, d):
        # Modern format uses nodeType; old compact format used name as node type.
        # After normalization, both should have nodeType set — but handle both
        # just in case a partially-normalized or raw old-format AST is passed.
        nt = n.get('nodeType') or n.get('name')
        if nt == target_type:
            result.append(n)

    walk_ast(ast, visit)
    return result
