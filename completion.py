from jedi import Script
from compiler import transpile_code
import re

ALLOWED = '->.:#ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

patterns = [
    {
        'pattern': re.compile(r'^#\s*[include]?'),
        'label': 'include',
        'type': 'statement'
    }
]

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

def insert_string_after_char(original_string, insert_string, char, x):
    parts = original_string.split(char)
    for i in range(len(parts)):
        if i % x == 0 and i != 0:
            parts[i] += insert_string
    return char.join(parts)

def getCompletion(code, line, column):
    code1 = code
    code2 = code.split('\n')[line-1][:column]
    code = code2[::-1]
    res = ''
    for c in code:
        if c in ALLOWED:
            res+=c
        else:
            break
    res = count_leading(code2)+res[::-1].replace('::', '.').replace('->', '.value.')
    try:
        s = Script(transpile_code(insert_string_after_char(code1, '\n'+res+'\n', '\n', line-1)))
        X = 3
        c = None
        while not str(s._code_lines[line+X]).endswith(res+'\n'):
            X+=1
        c = s.complete(line+X+1, len(s._code_lines[line+X+1])-1)
        x = { d.name: {'type': d.type} for d in c }
    except:
        x = {}
    z = matchAll(res.strip())
    for a in x.keys():
        b = x[a]
        if a != 'print':
            z[a] = b
    return z