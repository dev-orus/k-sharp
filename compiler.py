import regex as re
from syntax import *
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

DC = {'NULL': 'None', 'void': 'None', 'false': 'False', 'true': 'True'}

def tokenize(code: str, syntax=SYNTAX) -> list[Token]:
    tokens: list[Token] = []
    while code:
        for s in syntax:
            re_match = re.match(s, code)
            if re_match:
                if syntax[s]!=WHITESPACE:
                    re_groups = re_match.groups()
                    tokens.append(Token(syntax[s], re_groups if re_groups else re_match.group()))
                code = code.removeprefix(re_match.group())
                break
        if not re_match:
            raise SyntaxError(f'Invalid syntax at>{code}')
    return tokens

def trsi(c: str):
    return DC[c] if c in DC else str(c).replace('::', '.')

def transpile_round(code: str) -> str:
    TOKENS = tokenize(code.removeprefix('(').removesuffix(')'), SYNTAX2)
    pyCode = ''
    for token in TOKENS:
        if token.type == ROUND_BRACKETS:
            pyCode+=transpile_round(token.value)
        elif token.type == NUMBER:
            pyCode+=token.value[0]
        elif token.type == PTR_IDENTIFIER:
            pyCode+=token.value[0]+'.value'
        elif token.type == IDENTIFIER:
            pyCode+=trsi(token.value)
        elif token.value == COMMENT:
            if conf['comments']:
                pyCode+='#'+token.value[0]+'\n'
        elif token.type == STRING:
            pyCode+=token.value
        elif token.type == SEP:
            pyCode+=', '
        elif token.type == DIDENTIFIER:
            pyCode+=f'{token.value[1]}: {token.value[0]}'.replace('::', '.')
        elif token.type == PTR_SCOPE:
            pyCode+='.value.'
        elif token.type == OPERATOR:
            pyCode+=token.value
        elif token.type == SQUARE_BRACKETS:
            pyCode+=transpile_square(token.value)
        elif token.type == CURLY_BRACKETS:
            pyCode+=transpile_curly(token.value[0])
    return f'({pyCode})'

def transpile_curly(code: str) -> str:
    TOKENS = tokenize(code.removeprefix('{').removesuffix('}'), SYNTAX3)
    pyCode = ''
    for token in TOKENS:
        if token.type == ROUND_BRACKETS:
                pyCode+=transpile_round(token.value)
        elif token.type == NUMBER:
            pyCode+=token.value[0]
        elif token.type == PTR_IDENTIFIER:
            pyCode+=token.value[0]+'.value'
        elif token.type == IDENTIFIER:
            pyCode+=trsi(token.value)
        elif token.type == COMMENT:
            if conf['comments']:
                pyCode+='#'+token.value[0]+'\n'
        elif token.type == STRING:
            pyCode+=token.value
        elif token.type == SEP:
            pyCode+=token.value+' '
        elif token.type == NEWLINE:
            if not conf['compact']:
                pyCode+='\n'
        elif token.type == PTR_SCOPE:
            pyCode+='.value.'
        elif token.type == SQUARE_BRACKETS:
            pyCode+=transpile_square(token.value)
        elif token.type == CURLY_BRACKETS:
            pyCode+=transpile_curly(token.value[0])
    return '{'+pyCode+'}'

def transpile_square(code: str) -> str:
    TOKENS = tokenize(code.removeprefix('[').removesuffix(']'), SYNTAX5)
    pyCode = ''
    for token in TOKENS:
        if token.type == ROUND_BRACKETS:
            pyCode+=transpile_round(token.value)
        elif token.type == NUMBER:
            pyCode+=token.value[0]
        elif token.type == PTR_IDENTIFIER:
            pyCode+=token.value[0]+'.value'
        elif token.type == IDENTIFIER:
            pyCode+=trsi(token.value)
        elif token.value == COMMENT:
            if conf['comments']:
                pyCode+='#'+token.value[0]+'\n'
        elif token.type == STRING:
            pyCode+=token.value
        elif token.type == SEP:
            pyCode+=', '
        elif token.type == PTR_SCOPE:
            pyCode+='.value.'
        elif token.type == OPERATOR:
            pyCode+=token.value
        elif token.type == SQUARE_BRACKETS:
            pyCode+=transpile_square(token.value)
        elif token.type == CURLY_BRACKETS:
            pyCode+=transpile_curly(token.value[0])
    return '['+pyCode+']'

def transpile_struct(code: str, indent=1):
    code = code.removeprefix('{').removesuffix('}')
    if code.strip() == '' and indent>0:return (' ' * (indent+1))+'...'
    TOKENS = tokenize(code, SYNTAX4)
    pyCode = ''
    ptr_decl = False
    for token in TOKENS:
        if token.type == SEMICOLON:
            if ptr_decl:pyCode+=')'
            ptr_decl = False
            pyCode+=('\n' + (' ' * (indent+1))) if indent else '\n'
        elif token.type == VAR_DECL:
            pyCode+=f'{token.value[1]}: {token.value[0]} = '
        elif token.type == VAR_SET:
            pyCode+=f'{token.value[0]} = '
        elif token.type == PTR_VAR_DECL:
            ptr_decl = True
            pyCode+=f'{token.value[2]}: Ptr[{token.value[0]}] = Ptr('
        elif token.type == NUMBER:
            pyCode+=token.value[0]
        elif token.type == PTR_IDENTIFIER:
            pyCode+=token.value[0]+'.value'
        elif token.type == OPERATOR:
            pyCode+=token.value
        elif token.type == COMMENT:
            if conf['comments']:
                pyCode+='#'+token.value[0]+'\n'
        elif token.type == IDENTIFIER:
            pyCode+=trsi(token.value)
        elif token.type == FUNC_CALL:
            pyCode+=f"{str(token.value[0]).replace('::', '.')}{transpile_round(token.value[1])}"
        elif token.type == CURLY_BRACKETS:
            pyCode+=transpile_curly(token.value[0])
        elif token.type == DIDENTIFIER:
            pyCode+=f'{token.value[1]}: {token.value[0]}'
        elif token.type == SQUARE_BRACKETS:
            pyCode+=transpile_square(token.value)
    return pyCode

def transpile_code(code: str, indent=0) -> str:
    if code.strip() == '' and indent>0:return (' ' * (indent+1))+'...'
    TOKENS = tokenize(code, SYNTAX)
    pyCode = 'from dataclasses import dataclass\n' if indent==0 else (' ' * (indent+1))
    ptr_decl = False
    for token in TOKENS:
        if token.type == FUNC_DECL:
            pyCode+=f'def {token.value[1]}{transpile_round(token.value[2])} -> {trsi(token.value[0])}:\n' + transpile_code(str(token.value[3]).removeprefix('{').removesuffix('}'), indent+1) + '\n' + (' ' * (indent+1 if indent else 0))
        elif token.type == PTR_FUNC_DECL:
            pyCode+=f'def {token.value[2]}{transpile_round(token.value[3])} -> Ptr[{trsi(token.value[0])}]:\n' + transpile_code(str(token.value[4]).removeprefix('{').removesuffix('}'), indent+1) + '\n' + (' ' * (indent+1 if indent else 0))
        elif token.type == COMMENT:
            if ptr_decl:pyCode+=')'
            ptr_decl = False
            if conf['comments']:
                pyCode+='#'+token.value[0]+'\n'
        elif token.type == IDENTIFIER:
            pyCode+=trsi(token.value)
        elif token.type == KEYWORD:
            pyCode+=token.value+' '
        elif token.type == ROUND_BRACKETS:
            pyCode+=transpile_round(token.value)
        elif token.type == NEWLINE:
            if ptr_decl:pyCode+=')'
            ptr_decl = False
            pyCode+=('\n' + (' ' * (indent+1))) if indent else '\n'
        elif token.type == SEMICOLON:
            if ptr_decl:pyCode+=')'
            ptr_decl = False
            pyCode+=('\n' + (' ' * (indent+1))) if indent else '\n'
        elif token.type == VAR_DECL:
            pyCode+=f'{token.value[1]}: {trsi(token.value[0])} = '
        elif token.type == VAR_SET:
            pyCode+=f'{token.value[0]} = '
        elif token.type == PTR_VAR_DECL:
            ptr_decl = True
            pyCode+=f'{token.value[2]}: Ptr[{token.value[0]}] = Ptr('
        elif token.type == NUMBER:
            pyCode+=token.value[0]
        elif token.type == PTR_IDENTIFIER:
            pyCode+=token.value[0]+'.value'
        elif token.type == OPERATOR:
            pyCode+=token.value
        elif token.type == FUNC_CALL:
            pyCode+=f"{str(token.value[0]).replace('::', '.')}{transpile_round(token.value[1])}"
        elif token.type == CURLY_BRACKETS:
            pyCode+=transpile_curly(token.value[0])
        elif token.type == INCLUDE:
            pyCode+='from '+str(token.value[0]).removeprefix('<').removesuffix('>') + ' import *'
        elif token.type == STRUCT_DECL:
            pyCode+='@dataclass\n'
            pyCode+=f'class {token.value[0]}:\n{(' ' * (indent+2))}{transpile_struct(token.value[1], indent=indent+1)}\n'
        elif token.type == PTR_SCOPE:
            pyCode+='.value.'
        elif token.type == DIDENTIFIER:
            pyCode+=f'{token.value[1]}: {trsi(token.value[0])} = {trsi(token.value[0])}()'
        elif token.type == DIDENTIFIER_CALL:
            pyCode+=f'{token.value[1]}: {trsi(token.value[0])} = {trsi(token.value[0])}{transpile_round(token.value[2])}'
        elif token.type == PTR_DIDENTIFIER:
            pyCode+=f'{token.value[2]}: Ptr[{trsi(token.value[0])}] = Ptr({trsi(token.value[0])}())'
        elif token.type == PTR_DIDENTIFIER_CALL:
            pyCode+=f'{token.value[2]}: Ptr[{trsi(token.value[0])}] = Ptr({trsi(token.value[0])}{transpile_round(token.value[3])})'
        elif token.type == CLASS_DECL:
            pyCode+=f'class {token.value[0]}:\n{(' ' * (indent+2))}{transpile_code(str(token.value[1]).removeprefix('{').removesuffix('}'), indent+1)}'
        elif token.type == DECORATOR:
            pyCode+='@'+token.value[0]
        elif token.type == SQUARE_BRACKETS:
            pyCode+=transpile_square(token.value)
        elif token.type == SCOPE_KEYWORD:
            if token.value[0] in ('try', 'else'):
                pyCode+=f'{token.value[0]}:\n{(' ' * (indent+2))}{transpile_code(str(token.value[1]).removeprefix('{').removesuffix('}'), indent+1)}\n{(' ' * (indent+1))}'
            else:
                pyCode+=f'{token.value[0]} {transpile_round(token.value[1])}:\n{(' ' * (indent+2))}{transpile_code(str(token.value[2]).removeprefix('{').removesuffix('}'), indent+1)}\n{(' ' * (indent+1))}'
        else:
            print(token.type, token.value)
    pyCode += 'if __name__ == "__main__":main()' if indent==0 else (' ' * (indent+1))
    return pyCode