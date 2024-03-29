from compiler.lexer import tokenize, Token, pci
from compiler.syntax import *
from compiler.ast_ws import *
from typing import TypedDict, Any, NotRequired

class Ast:
    # type: str
    # contents: Token | str
    def __init__(self, token_type, value, htype = 0):
        self.type = token_type
        self.value = value
        self.htype = htype

def ctt(tokens: list[Token], i: int):
    return tokens[i]['type'] if i < len(tokens) else False

def parse(code: str, syntax=SYNTAX):
    TOKENS: list[Token] = tokenize(code, syntax)
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
            elif hid == OPERATOR and hid1 == OPERATOR and TOKENS[i+2]['value']=='=':
                ast.append(Ast(IDENTIFIER, pci(token['value'])))
                ast.append(Ast(OPERATOR, pci(TOKENS[i+1]['value'])))
                ast.append(Ast(OPERATOR, pci(TOKENS[i+2]['value'])))
                ignore = 2
            elif hid == OPERATOR and TOKENS[i+1]['value']=='=':
                ast.append(Ast(VAR_SET, pci(token['value'])))
                ignore = 1
            elif hid == OPERATOR and TOKENS[i+1]['value'] in ('++', '--'):
                ast.append(Ast(IDENTIFIER, pci(token['value'])))
                ast.append(Ast(OPERATOR, TOKENS[i+1]['value']))
                ignore = 1
            elif hid==IDENTIFIER and hid1 == OPERATOR and TOKENS[i+2]['value']=='=':
                ast.append(Ast(VAR_DECL, (pci(token['value']), pci(TOKENS[i+1]['value']))))
                ignore = 2
            elif hid==IDENTIFIER:
                ast.append(Ast(DIDENTIFIER, (pci(token['value']), pci(TOKENS[i+1]['value']))))
                ignore = 1
            else:
                ast.append(Ast(IDENTIFIER, pci(token['value'])))

        elif token['type'] == PTR_IDENTIFIER:
            hid = ctt(TOKENS, i+1)
            hid1 = ctt(TOKENS, i+2)
            hid2 = ctt(TOKENS, i+3)
            if hid==IDENTIFIER and hid1==ROUND_BRACKETS and hid2==CURLY_BRACKETS:
                ast.append(Ast(PTR_FUNC_DECL, (pci(token['value'][0]), pci(TOKENS[i+1]['value']), pci(TOKENS[i+2]['value']), pci(TOKENS[i+3]['value']))))
                ignore = 3
            elif hid == OPERATOR and hid1 == OPERATOR and TOKENS[i+2]['value']=='=':
                ast.append(Ast(PTR_IDENTIFIER, pci(token['value'][0])))
                ast.append(Ast(OPERATOR, pci(TOKENS[i+1]['value'])))
                ast.append(Ast(OPERATOR, pci(TOKENS[i+2]['value'])))
                ignore = 2
            elif hid == OPERATOR and TOKENS[i+1]['value']=='=':
                ast.append(Ast(PTR_VAR_SET, pci(token['value'][0])))
                ignore = 1
            elif hid == OPERATOR and TOKENS[i+1]['value'] in ('++', '--'):
                ast.append(Ast(PTR_IDENTIFIER, pci(token['value'][0])))
                ast.append(Ast(OPERATOR, TOKENS[i+1]['value']))
                ignore = 1
            elif hid==IDENTIFIER and hid1 == OPERATOR and TOKENS[i+2]['value']=='=':
                ast.append(Ast(PTR_VAR_DECL, (pci(token['value'][0]), pci(TOKENS[i+1]['value']))))
                ignore = 2
            elif hid==IDENTIFIER:
                ast.append(Ast(PTR_DIDENTIFIER, (pci(token['value'][0]), pci(TOKENS[i+1]['value']))))
                ignore = 1
            else:
                ast.append(Ast(PTR_IDENTIFIER, pci(token['value'])))
        
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
                if hid==ROUND_BRACKETS and hid1==CURLY_BRACKETS: 
                    ast.append(Ast(SCOPE_KEYWORD, (token['value'], pci(TOKENS[i+1]['value']), pci(TOKENS[i+2]['value']))))
                    ignore = 2
                elif token['value'] == 'except':
                    ast.append(Ast(SCOPE_KEYWORD, (token['value'], pci(TOKENS[i+1]['value']))))
                    ignore = 2
            elif token['value'] == 'use':
                if hid==IDENTIFIER and hid1==CURLY_BRACKETS:
                    ast.append(Ast(USE_KEYWORD2, (pci(TOKENS[i+1]['value']), pci(TOKENS[i+2]['value']))))
                    ignore = 2
                elif hid==IDENTIFIER:
                    ast.append(Ast(USE_KEYWORD, pci(TOKENS[i+1]['value'])))
                    ignore = 1
            else:
                ast.append(Ast(KEYWORD, pci(token['value'])))

        elif token['type'] == POWERWORD:
            hid = ctt(TOKENS, i+1)
            hid1 = ctt(TOKENS, i+2)
            if token['value'][0] == 'include':
                if hid==ANGLE_BRACKETS:
                    ast.append(Ast(POWERWORD, (token['value'][0], TOKENS[i+1]['value']), 0))
                    ignore = 1
                elif hid==STRING:
                    ast.append(Ast(POWERWORD, (token['value'][0], TOKENS[i+1]['value']), 1))
                    ignore = 1
        elif token['type'] == SOPERATOR:
            ast.append(Ast(OPERATOR, token['value']))
        elif token['type'] == OPERATOR:
            ast.append(Ast(OPERATOR, token['value']))
        else:
            ast.append(Ast(token['type'], token['value']))

    return ast