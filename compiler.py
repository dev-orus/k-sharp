import regex as re
from syntax import *
import ksconfig

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

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
            pyCode+=str(token.value).replace('::', '.')
            if ksconfig.comments:
                pyCode+='#'+token.value[0]+'\n'
        elif token.type == STRING:
            pyCode+=token.value
        elif token.type == SEP:
            pyCode+=', '
        elif token.type == DIDENTIFIER:
            pyCode+=f'{token.value[1]}: {token.value[0]}'.replace('::', '.')
        elif token.type == PTR_SCOPE:
            pyCode+='.value.'
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
            pyCode+=str(token.value).replace('::', '.')
        elif token.type == COMMENT:
            if ksconfig.comments:
                pyCode+='#'+token.value[0]+'\n'
        elif token.type == STRING:
            pyCode+=token.value
        elif token.type == SEP:
            pyCode+=token.value+' '
        elif token.type == NEWLINE:
            if not ksconfig.compact:
                pyCode+='\n'
        elif token.type == PTR_SCOPE:
            pyCode+='.value.'
    return '{'+pyCode+'}'

def transpile_struct(code: str, indent=1):
    code = code.removeprefix('{').removesuffix('}')
    if code.strip() == '' and indent>0:return (' ' * (indent+1))+'...'
    TOKENS = tokenize(code, SYNTAX4)
    pyCode = ''
    for token in TOKENS:
        if token.type == SEMICOLON:
            pyCode+=('\n' + (' ' * (indent+1))) if indent else '\n'
        elif token.type == VAR_DECL:
            pyCode+=f'{token.value[1]}: {token.value[0]} = '
        elif token.type == VAR_SET:
            pyCode+=f'{token.value[0]} = '
        elif token.type == PTR_VAR_DECL:
            pyCode+=f'{token.value[2]}: Ptr[{token.value[0]}] = '
        elif token.type == NUMBER:
            pyCode+=token.value[0]
        elif token.type == PTR_IDENTIFIER:
            pyCode+=token.value[0]+'.value'
        elif token.type == OPERATOR:
            pyCode+=token.value
        elif token.type == COMMENT:
            if ksconfig.comments:
                pyCode+='#'+token.value[0]+'\n'
        elif token.type == IDENTIFIER:
            pyCode+=str(token.value).replace('::', '.')
        elif token.type == FUNC_CALL:
            pyCode+=f"{str(token.value[0]).replace('::', '.')}{transpile_round(token.value[1])}"
        elif token.type == CURLY_BRACKETS:
            pyCode+=transpile_curly(token.value[0])
        elif token.type == DIDENTIFIER:
            pyCode+=f'{token.value[1]}: {token.value[0]}'
    return pyCode

def transpile_code(code: str, indent=0) -> str:
    if code.strip() == '' and indent>0:return (' ' * (indent+1))+'...'
    TOKENS = tokenize(code, SYNTAX)
    pyCode = 'from dataclasses import dataclass\n' if indent==0 else (' ' * (indent+1))

    for token in TOKENS:
        if token.type == FUNC_DECL:
            pyCode+=f'def {token.value[1]}{transpile_round(token.value[2])} -> {token.value[0]}:\n' + transpile_code(str(token.value[3]).removeprefix('{').removesuffix('}'), indent+1) + '\n' + (' ' * (indent+1 if indent else 0))
        elif token.type == PTR_FUNC_DECL:
            pyCode+=f'def {token.value[2]}{transpile_round(token.value[3])} -> Ptr[{token.value[0]}]:\n' + transpile_code(str(token.value[4]).removeprefix('{').removesuffix('}'), indent+1) + '\n' + (' ' * (indent+1 if indent else 0))
        elif token.type == COMMENT:
            if ksconfig.comments:
                pyCode+='#'+token.value[0]+'\n'
        elif token.type == IDENTIFIER:
            pyCode+=str(token.value).replace('::', '.')
        elif token.type == KEYWORD:
            pyCode+=token.value+' '
        elif token.type == ROUND_BRACKETS:
            pyCode+=transpile_round(token.value)
        elif token.type == NEWLINE:
            pyCode+=('\n' + (' ' * (indent+1))) if indent else '\n'
        elif token.type == SEMICOLON:
            pyCode+=('\n' + (' ' * (indent+1))) if indent else '\n'
        elif token.type == VAR_DECL:
            pyCode+=f'{token.value[1]}: {token.value[0]} = '
        elif token.type == VAR_SET:
            pyCode+=f'{token.value[0]} = '
        elif token.type == PTR_VAR_DECL:
            pyCode+=f'{token.value[2]}: Ptr[{token.value[0]}] = '
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
            pyCode+=f'{token.value[1]}: {token.value[0]} = {token.value[0]}()'
        elif token.type == DIDENTIFIER_CALL:
            pyCode+=f'{token.value[1]}: {token.value[0]} = {token.value[0]}{transpile_round(token.value[2])}'
        elif token.type == PTR_DIDENTIFIER:
            pyCode+=f'{token.value[2]}: Ptr[{token.value[0]}] = Ptr({token.value[0]}())'
        elif token.type == PTR_DIDENTIFIER_CALL:
            pyCode+=f'{token.value[2]}: Ptr[{token.value[0]}] = Ptr({token.value[0]}{transpile_round(token.value[3])})'
        else:
            print(token.type, token.value)
    pyCode += 'if __name__ == "__main__":main()' if indent==0 else (' ' * (indent+1))
    return pyCode