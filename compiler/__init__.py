from compiler.ks_parser import parse
from compiler.syntax import *
from compiler.ast_ks import *
from compiler.syntax import *
from os import path
from json import load

if path.exists('ksconfig.json'):
    with open('ksconfig.json')as f:
        conf = load(f)
else:
    conf = {'outDir': 'out', 'compact': True, 'comments': False}

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

def transpile_round(code: str) -> str:
    TOKENS = parse(code.removeprefix('(').removesuffix(')'), SYNTAX2)
    pyCode = ''
    for token in TOKENS:
        if token.type == ROUND_BRACKETS:
            pyCode+=transpile_round(token.value)
        elif token.type == NUMBER:
            pyCode+=token.value[0]
        elif token.type == PTR_IDENTIFIER:
            pyCode+=token.value[0]+'.value'
        elif token.type == IDENTIFIER:
            pyCode+=token.value
        elif token.value == COMMENT:
            if conf['comments']:
                pyCode+='#'+token.value[0]
        elif token.type == STRING:
            pyCode+=token.value
        elif token.type == SEP:
            pyCode+=', '
        elif token.type == DIDENTIFIER:
            pyCode+=f'{token.value[1]}: {token.value[0]}'.replace('::', '.')
        elif token.type == PTR_SCOPE:
            pyCode+='.value.'
        elif token.type == OPERATOR:
            if token.value == '++':
                pyCode+='+=1'
            elif token.value == '--':
                pyCode+='-=1'
            else:
                pyCode+=token.value
        elif token.type == SQUARE_BRACKETS:
            pyCode+=transpile_square(token.value)
        elif token.type == CURLY_BRACKETS:
            pyCode+=transpile_curly(token.value)
    return f'({pyCode})'

def transpile_round2(code: str) -> str:
    TOKENS = parse(code.removeprefix('(').removesuffix(')'), SYNTAX2)
    pyCode = ''
    for token in TOKENS:
        if token.type == ROUND_BRACKETS:
            pyCode+=transpile_round(token.value)
        elif token.type == NUMBER:
            pyCode+=token.value[0]
        elif token.type == PTR_IDENTIFIER:
            pyCode+=token.value[0]+'.value'
        elif token.type == IDENTIFIER:
            pyCode+=token.value
        elif token.value == COMMENT:
            if conf['comments']:
                pyCode+='#'+token.value[0]
        elif token.type == STRING:
            pyCode+=token.value
        elif token.type == SEP:
            pyCode+=', '
        elif token.type == DIDENTIFIER:
            pyCode+=f'{token.value[0]} {token.value[1]} '.replace('::', '.')
        elif token.type == PTR_SCOPE:
            pyCode+='.value.'
        elif token.type == OPERATOR:
            if token.value == '++':
                pyCode+='+=1'
            elif token.value == '--':
                pyCode+='-=1'
            else:
                pyCode+=token.value
        elif token.type == SQUARE_BRACKETS:
            pyCode+=transpile_square(token.value)
        elif token.type == CURLY_BRACKETS:
            pyCode+=transpile_curly(token.value)
    return f'({pyCode})'

def transpile_curly(code: str) -> str:
    TOKENS = parse(code.removeprefix('{').removesuffix('}'), SYNTAX2)
    pyCode = ''
    for token in TOKENS:
        if token.type == ROUND_BRACKETS:
                pyCode+=transpile_round(token.value)
        elif token.type == NUMBER:
            pyCode+=token.value[0]
        elif token.type == PTR_IDENTIFIER:
            pyCode+=token.value[0]+'.value'
        elif token.type == IDENTIFIER:
            pyCode+=token.value
        elif token.type == COMMENT:
            if conf['comments']:
                pyCode+='#'+token.value[0]
        elif token.type == STRING:
            pyCode+=token.value
        elif token.type == SEP:
            pyCode+=token.value+' '
        elif token.type == SEP1:
            pyCode+=token.value+' '
        elif token.type == NEWLINE:
            if not conf['compact']:
                pyCode+='\n'
        elif token.type == PTR_SCOPE:
            pyCode+='.value.'
        elif token.type == SQUARE_BRACKETS:
            pyCode+=transpile_square(token.value)
        elif token.type == CURLY_BRACKETS:
            pyCode+=transpile_curly(token.value)
    return '{'+pyCode+'}'

def transpile_square(code: str) -> str:
    TOKENS = parse(code.removeprefix('[').removesuffix(']'), SYNTAX2)
    pyCode = ''
    for token in TOKENS:
        if token.type == ROUND_BRACKETS:
            pyCode+=transpile_round(token.value)
        elif token.type == NUMBER:
            pyCode+=token.value[0]
        elif token.type == PTR_IDENTIFIER:
            pyCode+=token.value[0]+'.value'
        elif token.type == IDENTIFIER:
            pyCode+=token.value
        elif token.value == COMMENT:
            if conf['comments']:
                pyCode+='#'+token.value[0]
        elif token.type == STRING:
            pyCode+=token.value
        elif token.type == SEP:
            pyCode+=', '
        elif token.type == PTR_SCOPE:
            pyCode+='.value.'
        elif token.type == OPERATOR:
            if token.value == '++':
                pyCode+='+=1'
            elif token.value == '--':
                pyCode+='-=1'
            else:
                pyCode+=token.value
        elif token.type == SQUARE_BRACKETS:
            pyCode+=transpile_square(token.value)
        elif token.type == CURLY_BRACKETS:
            pyCode+=transpile_curly(token.value)
    return '['+pyCode+']'

def transpile(code: str, indent=0) -> str:
    if code.strip() == '' and indent>0:return (' ' * (indent*2))+'...'
    TOKENS = parse(code)
    pyCode = 'from dataclasses import dataclass\nfrom typing import Any as auto\n' if indent==0 else '\n' + (' ' * (indent*2))
    ignore_fline = False
    if indent:
        ignore_fline = True
    ptr_decl = False
    for i, token in enumerate(TOKENS):
        if token.type == FUNC_DECL:
            pyCode+=f'def {token.value[1]}{transpile_round(token.value[2])} -> {token.value[0]}:' + transpile(str(token.value[3]).removeprefix('{').removesuffix('}'), indent+1) + '\n' + (' ' * (indent+1 if indent else 0))
        elif token.type == PTR_FUNC_DECL:
            pyCode+=f'def {token.value[1]}{transpile_round(token.value[2])} -> Ptr[{token.value[0]}]:' + transpile(str(token.value[3]).removeprefix('{').removesuffix('}'), indent+1) + '\n' + (' ' * (indent+1 if indent else 0))
        elif token.type == COMMENT:
            if ptr_decl:pyCode+=')'
            ptr_decl = False
            if conf['comments']:
                pyCode+='#'+token.value[0]
        elif token.type == IDENTIFIER:
            pyCode+=token.value
        elif token.type == USE_KEYWORD:
            if '.' in token.value:
                v = token.value.split('.')
                v1 = v[-1]
                v2 = '.'.join(v[0:-1])
                pyCode+=f'from {v2} import {v1}'
            else:
                pyCode+=f'import {token.value}'
        elif token.type == USE_KEYWORD2:
            pyCode+=f'from {token.value[0].removesuffix('.')} import {str(token.value[1]).removeprefix('{').removesuffix('}')}'
        elif token.type == KEYWORD:
            pyCode+=token.value+' '
        elif token.type == ROUND_BRACKETS:
            pyCode+=transpile_round(token.value)
        elif token.type == NEWLINE:
            if i+1<len(TOKENS) and not ignore_fline:
                if ptr_decl:pyCode+=')'
                ptr_decl = False
                pyCode+=('\n' + (' ' * (indent*2))) if indent else '\n'
            if ignore_fline:ignore_fline = False
        elif token.type == SEMICOLON:
            if ptr_decl:pyCode+=')'
            ptr_decl = False
            if len(TOKENS)>i+1 and not TOKENS[i+1].type==NEWLINE:
                pyCode+=('\n' + (' ' * (indent*2))) if indent else '\n'
        elif token.type == VAR_DECL:
            pyCode+=f'{token.value[1]}: {token.value[0]} = '
        elif token.type == VAR_SET:
            pyCode+=f'{token.value[0]} = '
        elif token.type == PTR_VAR_DECL:
            pyCode+=f'{token.value[1]}: Ptr[{token.value[0]}] = Ptr('
            ptr_decl = True
        elif token.type == PTR_VAR_SET:
            pyCode+=f'{token.value}.value = '
        elif token.type == NUMBER:
            pyCode+=token.value
        elif token.type == PTR_IDENTIFIER:
            pyCode+=token.value[0]+'.value'
        elif token.type == OPERATOR:
            if token.value == '++':
                pyCode+='+=1'
            elif token.value == '--':
                pyCode+='-=1'
            else:
                pyCode+=token.value
        elif token.type == FUNC_CALL:
            pyCode+=f"{str(token.value[0]).replace('::', '.')}{transpile_round(token.value[1])}"
        elif token.type == CURLY_BRACKETS:
            pyCode+=transpile_curly(token.value)
        elif token.type == POWERWORD:
            if token.value[0] == 'include':
                if token.htype==0:
                    pyCode+='from '+str(token.value[1][0]).removeprefix('<').removesuffix('>') + ' import *'
                if token.htype==1:
                    pyCode+='from '+str(token.value[1]).removeprefix('"').removesuffix('"') + ' import *'
        elif token.type == STRUCT_DECL:
            pyCode+='@dataclass\n'
            pyCode+=f'class {token.value[0]}:{transpile(token.value[1].removeprefix('{').removesuffix('}'), indent+1)}\n'
        elif token.type == PTR_SCOPE:
            pyCode+='.value.'
        elif token.type == DIDENTIFIER:
            pyCode+=f'{token.value[1]}: {token.value[0]} = {token.value[0]}()'
        elif token.type == DIDENTIFIER_CALL:
            pyCode+=f'{token.value[1]}: {token.value[0]} = {token.value[0]}{transpile_round(token.value[2])}'
        elif token.type == PTR_DIDENTIFIER:
            pyCode+=f'{token.value[1]}: Ptr[{token.value[0]}] = Ptr({token.value[0]}())'
        elif token.type == PTR_DIDENTIFIER_CALL:
            pyCode+=f'{token.value[2]}: Ptr[{token.value[0]}] = Ptr({token.value[0]}{transpile_round(token.value[3])})'
        elif token.type == CLASS_DECL:
            pyCode+=f'class {token.value[0]}:{transpile(str(token.value[1]).removeprefix('{').removesuffix('}'), indent+1)}'
        elif token.type == DECORATOR:
            pyCode+='@'+token.value[0]
        elif token.type == SQUARE_BRACKETS:
            pyCode+=transpile_square(token.value)
        elif token.type == SCOPE_KEYWORD:
            if len(token.value)==2:
                pyCode+=f'{token.value[0]}:{transpile(str(token.value[1]).removeprefix('{').removesuffix('}'), indent+1)}\n{(' ' * (indent*2))}'
            else:
                pyCode+=f'{token.value[0]} {transpile_round2(token.value[1]).removeprefix('(').removesuffix(')')}:{transpile(str(token.value[2]).removeprefix('{').removesuffix('}'), indent+1)}\n{(' ' * (indent*2))}'
        elif token.type == STRING:
            pyCode+=token.value
        else:
            # In case there is a token that isn't handled (Please send feedback if so)
            print('Problem: There is a unhandled token ->', token.type, token.value)
    pyCode += '\nif __name__ == "__main__":\n  try:exec("quit(main())")\n  except NameError:pass\n# mypy: disable-error-code = import-untyped' if indent==0 else (' ' * (indent*2))
    return pyCode
