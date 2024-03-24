import regex as re
import compiler.syntax as syntax
from typing import TypedDict, Any

# class Token:
#     def __init__(self, token_type, value):
#         self.type = token_type
#         self.value = value

class Token(TypedDict):
    type: str
    value: tuple[str]

KEYWORD_CHANGE = {'NULL': 'None', 'void': 'None', 'false': 'False', 'true': 'True', '&&': ' and ', '||': ' or '}

def tokenize(code: str) -> list[Token]:
    tokens: list[Token] = []
    while code:
        for s in syntax.SYNTAX:
            re_match = re.match(s, code)
            if re_match:
                if syntax.SYNTAX[s]!=syntax.WHITESPACE:
                    re_groups = re_match.groups()
                    tokens.append({"type": syntax.SYNTAX[s], "value": re_groups if re_groups else re_match.group()})
                code = code.removeprefix(re_match.group())
                break
        if not re_match:
            raise SyntaxError(f'Invalid syntax at>{code}')
    return tokens

def pci(id: str) -> str:
    return KEYWORD_CHANGE[id] if id in KEYWORD_CHANGE else str(id).replace('::', '.').replace('->', '.value.').replace('*', '.value')