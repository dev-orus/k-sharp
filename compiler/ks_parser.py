from compiler.lexer import tokenize, Token, pci
from compiler.syntax import *
from compiler.ast_ks import *
from typing import TypedDict, Any, NotRequired

class Ast:
    # type: str
    # contents: Token | str
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

def ctt(tokens: list[Token], i: int):
    return tokens[i]['type'] if i < len(tokens) else False

def parse(code: str):
    TOKENS: list[Token] = tokenize(code)
    current_statement: list[Token] = []
    ignore = 0
    ast: list[Ast] = []
    for i, token in enumerate(TOKENS):
        if ignore:
            ignore-=1
            continue

        if token['type'] == IDENTIFIER:
            hid = ctt(TOKENS, i+1)
            hid1 = ctt(TOKENS, i+2)
            hid2 = ctt(TOKENS, i+3)
            if hid1==ROUND_BRACKETS and hid2==CURLY_BRACKETS:
                ast.append(Ast(FUNC_DECL, (pci(token['value']), pci(TOKENS[i+1]['value']), pci(TOKENS[i+2]['value']), pci(TOKENS[i+3]['value']))))
                ignore = 3
            elif hid2 == OPERATOR:
                ast.append(Ast(VAR_DECL, (pci(token['value']), pci(TOKENS[i+1]['value']))) if hid==IDENTIFIER else Ast(IDENTIFIER, pci(token['value'])))
            else:
                ast.append(Ast(DIDENTIFIER, (pci(token['value']), pci(TOKENS[i+1]['value']))) if hid==IDENTIFIER else Ast(IDENTIFIER, pci(token['value'])))
                ignore = 1

        elif token['type'] == PTR_IDENTIFIER:
            hid = ctt(TOKENS, i+1)
            hid1 = ctt(TOKENS, i+2)
            hid2 = ctt(TOKENS, i+3)
            if hid1==ROUND_BRACKETS and hid2==CURLY_BRACKETS:
                ast.append(Ast(PTR_FUNC_DECL, (pci(token['value'][0]), pci(TOKENS[i+1]['value']), pci(TOKENS[i+2]['value']), pci(TOKENS[i+3]['value']))))
                ignore = 3
            elif hid2 == OPERATOR:
                ast.append(Ast(PTR_VAR_DECL, (pci(token['value'][0]), pci(TOKENS[i+1]['value']))) if hid==IDENTIFIER else Ast(IDENTIFIER, pci(token['value'])))
            else:
                ast.append(Ast(PTR_DIDENTIFIER, (pci(token['value'][0]), pci(TOKENS[i+1]['value']))) if hid==IDENTIFIER else Ast(IDENTIFIER, pci(token['value'])))
                ignore = 1
        
        elif token['type'] == KEYWORD:
            hid = ctt(TOKENS, i+1)
            hid1 = ctt(TOKENS, i+2)
            if token['value'] == 'struct':
                if hid==IDENTIFIER and hid1==CURLY_BRACKETS:
                    ast.append(Ast(STRUCT_DECL, (pci(TOKENS[i+1]['value']), pci(TOKENS[i+2]['value']))))
                    ignore = 2
            elif token['value'] == 'class' and hid and hid1:
                if hid==IDENTIFIER and hid1==CURLY_BRACKETS:
                    ast.append(Ast(CLASS_DECL, (pci(TOKENS[i+1]['value']), pci(TOKENS[i+2]['value']))))
                    ignore = 2
            elif token['value'] in ('if', 'elif', 'except'):
                print(token['value'])
                if hid==ROUND_BRACKETS and hid1==CURLY_BRACKETS: 
                    ast.append(Ast(SCOPE_KEYWORD, (token['value'], pci(TOKENS[i+1]['value']), pci(TOKENS[i+2]['value']))))
                    ignore = 2
                elif token['value'] == 'except':
                    ast.append(Ast(SCOPE_KEYWORD, (token['value'], pci(TOKENS[i+1]['value']))))
                    ignore = 2
            else:
                if hid:
                    ast.append(Ast(SCOPE_KEYWORD, (token['value'], pci(TOKENS[i+1]['value']))))
                    ignore = 2
        else:
            ast.append(Ast(token['type'], token['value']))

    return ast