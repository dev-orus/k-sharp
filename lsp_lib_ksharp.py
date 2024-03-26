from jedi import Script
from compiler import transpile
import re
from os.path import join, dirname, exists
from traceback import format_exc

parent = dirname(__file__)

ALLOWED = '"\'# -<>.:#ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
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
    }
]

DISABLED = ('def', 'import', 'from', 'None', 'False', 'True')

def matchAll(string: str) -> dict[dict]:
    res = {}
    for p in patterns:
        re_match = p['pattern'].match(string)
        if re_match:
            res[p['label']] = {'type': p['type']}
    return res

def count_leading(s):
    re_match = re.match(r'^\s*', s)
    if re_match:
        return re_match.group()
    return ''

# def insert_string_after_char(original_string, insert_string, char, x):
#     if x == 0:
#         return original_string
#     parts = original_string.split(char)
#     for i in range(len(parts)):
#         if i % x == 0 and i != 0:
#             parts[i] += insert_string
#     return char.join(parts)

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
    res = ''
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
            s = Script(insert_string_after_char(transpile(''), '\n'+count_leading(code2)+res+'\n', '\n', 2))
            cmp = s.complete(4, len(s._code_lines[3].removesuffix('\n')))
            x = {}
            for d in cmp:
                x[d.name] = {'type': d.type, 'doc': '', 'sign': '', 'glb': '<' in res1}
        except:
            with open(join(parent, 'err.log'), 'w')as f:
                print(format_exc(), file=f)
            x = {}
        return x
    else:
        if ('"' in code2 and code2.count('"') % 2 == 1) or ("'" in code2 and code2.count("'") % 2 == 1):
            return {}
        x = {}
        try:
            s = Script(transpile(insert_string_after_char(insert_string_after_char(code1, '\n'+count_leading(code2)+res+'\n', '\n', line-1), '\n//comp\n', '\n', line-2)))
            res = res.replace('::', '.').replace('->', '.value.')
            for i in range(line-1, len(s._code_lines)-1):
                if (str(s._code_lines[i-1]).strip()==res.strip()):
                    cmp = s.complete(i, len(s._code_lines[i-1])-1)
                    x = {}
                    for d in cmp:
                        x[d.name] = {'type': d.type, 'doc': '', 'sign': ''}
                    break
        except:
            with open(join(parent, 'err.log'), 'w')as f:
                print(format_exc(), file=f)
            x = {}
        z = matchAll(res.strip())
        for a in x.keys():
            b = x[a]
            if a not in DISABLED:
                z[a] = b
    return z