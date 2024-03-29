from jedi import Script
from compiler import transpile
import re
from os.path import join, dirname, exists
from traceback import format_exc

parent = dirname(__file__)

ALLOWED = '{,"\'# -<>.:#ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
ALLOWED2 = '-<>.:#ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

patterns = [
    {
        'pattern': re.compile(r'^# *in?c?l?u?d?e?'),
        'label': 'include',
        'type': 'keyword'
    },
    {
        'pattern': re.compile(r'^vo?i?d?'),
        'label': 'void',
        'type': 'keyword'
    },
    {
        'pattern': re.compile(r'^st?r?u?c?t?'),
        'label': 'struct',
        'type': 'keyword'
    },
    {
        'pattern': re.compile(r'^NU?L?L?'),
        'label': 'NULL',
        'type': 'keyword'
    },
    {
        'pattern': re.compile(r'^fa?l?s?e?'),
        'label': 'false',
        'type': 'keyword'
    },
    {
        'pattern': re.compile(r'^tr?u?e?'),
        'label': 'true',
        'type': 'keyword'
    },
    {
        'pattern': re.compile(r'^us?e?'),
        'label': 'use',
        'type': 'keyword'
    }
]

DISABLED = ('def', 'import', 'from', 'None', 'False', 'True')

def matchAll(string: str) -> dict[dict]:
    res = {}
    for p in patterns:
        re_match = p['pattern'].match(string)
        if re_match:
            res[p['label']] = {'type': p['type'], 'doc': '', 'sign': ''}
    return res

def count_leading(s):
    re_match = re.match(r'^\s*', s)
    if re_match:
        return re_match.group()
    return ''

def extract_params(params_string):
    wispCode = '\n  '
    pattern = r'([&_a-zA-Z][a-zA-Z0-9_.\[\]]*)\s*(?::\s*([&_a-zA-Z][a-zA-Z0-9_.\[\]]*))?(?:(.*?(?=,|$)))?'
    matches: list[tuple[str]] = re.findall(pattern, params_string)
    for m in matches:
        if m[1]:
            wispCode+=m[1]+' '
        # if m[0].strip().startswith('**'):
            # wispCode+='&&'
        # elif m[0].strip().startswith('*'):
            # wispCode+='&'
        wispCode+=m[0]
        if m[2]:
            wispCode+=m[2]
        wispCode+=",\n  "
    return wispCode.rstrip()+'\n'

def get_wisp(code:str):
    re_match = re.search(r"^def\s+([_a-zA-Z][a-zA-Z0-9_.\[\]]*)\s*\((.*?)\)\s*->\s*([_a-zA-Z][a-zA-Z0-9_.\[\]]*)", code.strip(), re.DOTALL)
    re_match1 = re.search(r"^def\s+([_a-zA-Z][a-zA-Z0-9_.\[\]]*)\s*\((.*?)\)", code.strip(), re.DOTALL)
    re_match2 = re.search(r"^([_a-zA-Z][a-zA-Z0-9_.\[\]]*)\s*=", code.strip(), re.DOTALL)
    re_match3 = re.search(r"^([_a-zA-Z][a-zA-Z0-9_.\[\]]*)\s*\:\s*([_a-zA-Z][a-zA-Z0-9_.\[\]]*)\s*=", code.strip(), re.DOTALL)
    formatted_signature = ''
    if re_match:
        function_name = re_match.group(1).strip()
        parameters = extract_params(re_match.group(2))
        returnType = re_match.group(3).strip().replace('.value.', '->').replace('.', '::')
        returnType = 'void' if returnType == 'None' else returnType
        formatted_signature = f"{returnType} {function_name}({parameters})"
    elif re_match1:
        function_name = re_match1.group(1).strip()
        parameters = re_match1.group(2).strip()
        returnType = 'void'
        formatted_signature = f"{returnType} {function_name}({parameters})"
    elif re_match2:
        var_decl = re_match2.group()
        formatted_signature = f"auto {var_decl}"
    elif re_match3:
        var_name = re_match3.group(1)
        var_type = re_match3.group(2)
        formatted_signature = f"{var_type} {var_name} = {code.strip().removeprefix(re_match3.group()).strip()}"
    return formatted_signature

def insert_string_after_char(original_string, insert_string, char, x):
    parts = original_string.split(char)
    for i in range(len(parts)):
        if i == x:
            parts[i] += insert_string
    return char.join(parts)

def getDefinition(code: str, line: int, colnum: int, file: str):
    index = sum(len(line) + 1 for line in code.split('\n')[:line-1]) + colnum - 1
    try:res = re.search(r'^[_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*', code[index:]).group()
    except:return {"err": True}
    s = Script(transpile(insert_string_after_char(code, '\n'+res+'\n', '\n', line-1)), path=dirname(file))
    for i in range(line-1, len(s._code_lines)-1):
        if (str(s._code_lines[i]).strip()==res.strip()):
            c = s.goto(i, len(str(s._code_lines[i]).strip())-1)
            if c:
                definition = c[0]
                return {"file": str(definition.module_path), "line": definition.line, "col": definition.column}
            else:
                return {"err": True}
    return {"err": True}

def printf(*values, sep: str=' '):
    """
    idk
    """
    with open(join(parent, 'lsp.log'), 'w')as f:
        print(*values, sep=sep, file=f)

def sort_dict_by_underscores(d):
    def underscore_count(key):
        return (key.count('_'), key)
    sorted_items = sorted(d.items(), key=lambda item: underscore_count(item[0]))
    sorted_dict = dict(sorted_items)
    return sorted_dict

def getCompletion(code: str, line: int, column: int, file: str):
    code1 = code
    code2 = code.split('\n')[line-1][:column]
    code = code2[::-1]
    res1 = ''
    for c in code:
        if c in ALLOWED:
            res1+=c
        else:
            break
    re_match = re.match(r'^# *include *(<|")', res1[::-1])
    if re_match and res1[::-1].strip().endswith('>'):
        return {}
    re_match1 = re.match(r'^\s*use *', res1[::-1])
    re_match2 = re.match(r'^\s*use *[_a-zA-Z](?:[a-zA-Z0-9_.]|::|->)*\{', res1[::-1])
    res = ''
    z = {}
    for c in res1:
        if c in ALLOWED2:
            res+=c
        else:
            break
    res = res[::-1]
    if re_match:
        x = {}
        try:
            res = 'import '+res1[::-1].removeprefix(re_match.group())
            s = Script(res)
            cmp = s.complete(1, len(s._code_lines[0].removesuffix('\n')))
            x = {}
            for d in cmp:
                x[d.name] = {'type': d.type, 'doc': '', 'sign': '', 'glb': '<' in res1}
        except:
            with open(join(parent, 'err.log'), 'w')as f:
                print(format_exc(), file=f)
            x = {}
        return x
    elif re_match2:
        x = {}
        try:
            res = transpile(res1[::-1]+'}', 1).strip()
            if not res.startswith('from'):
                res = 'import '+res1[::-1].replace('::', '.').replace('->', '.value.').removeprefix(re_match2.group())
            s = Script(res)
            cmp = s.complete(1, len(s._code_lines[0].removesuffix('\n')))
            for d in cmp:
                x[d.name] = {'type': d.type, 'doc': '', 'sign': '', 'glb': '<' in res1}
        except:
            with open(join(parent, 'err.log'), 'w')as f:
                print(format_exc(), file=f)
        return x
    elif re_match1:
        x = {}
        try:
            res = transpile(res1[::-1], 1).lstrip()
            if not res1[::-1].replace('::', '.').endswith('.'):
                res = res.strip()
            s = Script(res)
            cmp = s.complete(1, len(s._code_lines[0].removesuffix('\n')))
            for d in cmp:
                x[d.name] = {'type': d.type, 'doc': '', 'sign': '', 'glb': '<' in res1}
        except:
            with open(join(parent, 'err.log'), 'w')as f:
                print(format_exc(), file=f)
        return x
    else:
        if ('"' in code2 and code2.count('"') % 2 == 1) or ("'" in code2 and code2.count("'") % 2 == 1):
            return {}
        x = {}
        res = res.replace('::', '.').replace('->', '.value.')
        try:
            s = Script(transpile(insert_string_after_char(insert_string_after_char(code1, '\n'+count_leading(code2)+res+'\n', '\n', line-1), '\n//comp\n', '\n', line-2)))
            for i in range(line-2, len(s._code_lines)-1):
                if (str(s._code_lines[i-1]).strip()==res.strip()):
                    cmp = s.complete(i, len(s._code_lines[i-1])-1)
                    for d in cmp:
                        formatted_signature = ''
                        try:
                            definitions = d.goto()
                            for definition in definitions:
                                signatures = definition.get_signatures()
                                for sign in signatures:
                                    spos = sign.get_definition_start_position()
                                    epos = sign.get_definition_end_position()
                                    if sign.module_path:
                                        with open(sign.module_path)as fv:
                                            fcode = fv.read().split('\n')
                                            fout = fcode[spos[0]-1:epos[0]]
                                            fout[0] = fout[0][spos[1]:]
                                            fout[-1] = fout[-1][:epos[1]]
                                            formatted_signature = get_wisp(f"{'\n'.join(fout)}")
                                    else:
                                        fout = s._code_lines[spos[0]-1:spos[0]][spos[1]:]
                                        formatted_signature = get_wisp(f"{'\n'.join(fout)}")
                        except:pass
                        x[d.name] = {'type': d.type, 'doc': d.docstring(True, True), 'sign': formatted_signature}
                    break
        except:
            with open(join(parent, 'err.log'), 'w')as f:
                print(format_exc(), file=f)
        z = matchAll(res.strip())
        for a in x.keys():
            b = x[a]
            if a not in DISABLED:
                z[a] = b
        return z