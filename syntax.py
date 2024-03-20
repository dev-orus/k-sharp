KEYWORD = 'KEYWORD'
WHITESPACE = 'WHITESPACE'
NEWLINE = 'NEWLINE'
SEMICOLON = 'SEMICOLON'
NUMBER = 'NUMBER'
FUNC_DECL = 'FUNC_DECL'
PTR_FUNC_DECL = 'PTR_FUNC_DECL'
VAR_DECL = 'VAR_DECL'
CLASS_DECL = 'CLASS_DECL'
PTR_VAR_DECL = 'PTR_VAR_DECL'
VAR_SET = 'VAR_SET'
FUNC_CALL = 'FUNC_CALL'
WHITESPACE = 'WHITESPACE'
ROUND_BRACKETS = 'ROUND_BRACKETS'
CURLY_BRACKETS = 'CURLY_BRACKETS'
SQUARE_BRACKETS = 'SQUARE_BRACKETS'
IDENTIFIER = 'IDENTIFIER'
PTR_IDENTIFIER = 'PTR_IDENTIFIER'
STRING = 'STRING'
SEP = 'SEP'
COMMENT = 'COMMENT'
OPERATOR = 'OPERATOR'
DIDENTIFIER = 'DIDENTIFIER'
INCLUDE = 'INCLUDE'
INCLUDE_LOCAL = 'INCLUDE_LOCAL'
STRUCT_DECL = 'STRUCT_DECL'
PTR_SCOPE = 'PTR_SCOPE'
DIDENTIFIER_CALL = 'DIDENTIFIER_CALL'
PTR_DIDENTIFIER = 'PTR_DIDENTIFIER'
PTR_DIDENTIFIER_CALL = 'PTR_DIDENTIFIER_CALL'
DECORATOR = 'DECORATOR'
SCOPE_KEYWORD = 'SCOPE_KEYWORD'
DELETE = 'DELETE'

SYNTAX = {
    r'^\n': NEWLINE,
    r'^\;': SEMICOLON,
    r'^\s': WHITESPACE,
    r'^\-\>': PTR_SCOPE,
    r'^# *del *([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)': DELETE,
    r'^# *include *(<(?:[^<>]|(?R))*>)': INCLUDE,
    r'^# *include *("(?:[^""]|(?R))*")': INCLUDE_LOCAL,
    r'^return|yield|raise': KEYWORD,
    r'^(if|elif|except|for) *(\((?:[^()]|\([^()]*\))*\)) *(\{(?:[^{}]|\{[^{}]*\})*\})': SCOPE_KEYWORD,
    r'^(try|else|) *(\{(?:[^{}]|\{[^{}]*\})*\})': SCOPE_KEYWORD,
    r'^class +([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *(\{(?:[^{}]|\{[^{}]*\})*\})': CLASS_DECL,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *(\((?:[^()]|\([^()]*\))*\)) *(\{(?:[^{}]|\{[^{}]*\})*\})': FUNC_DECL,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *(\((?:[^()]|\([^()]*\))*\))': FUNC_CALL,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)(\* +| +\*)([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *(\((?:[^()]|\([^()]*\))*\)) *(\{(?:[^{}]|\{[^{}]*\})*\})': PTR_FUNC_DECL,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *= *': VAR_SET,
    r'^@([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)': DECORATOR,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *= *': VAR_DECL,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)(\* +| +\*)([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *= *': PTR_VAR_DECL,
    r'^struct +([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *(\{(?:[^{}]|\{[^{}]*\})*\})': STRUCT_DECL,
    r'^\[[^\]]*\]': SQUARE_BRACKETS,
    r'^//(.+?)(?=\n|$)': COMMENT,
    r'^(0(x|X)\d+|-0(x|X)\d+|-\d+|\d+)': NUMBER,
    r'^([-]?[0-9]*\.?[0-9]+)': NUMBER,
    r'^\((?:[^()]|(?R))*\)': ROUND_BRACKETS,
    r'^(\{(?:[^{}]|(?R))*\})': CURLY_BRACKETS,
    r'^\"(?:[^""]|(?R))*\"': STRING,
    r"^\'(?:[^'']|(?R))*\'": STRING,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)(\* +| +\*)([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *(\((?:[^()]|\([^()]*\))*\))': PTR_DIDENTIFIER_CALL,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)(\* +| +\*)([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)': PTR_DIDENTIFIER,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) +([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *(\((?:[^()]|\([^()]*\))*\))': DIDENTIFIER_CALL,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) +([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)': DIDENTIFIER,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)\*': PTR_IDENTIFIER,
    r'^[_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*': IDENTIFIER,
    r'\&\&|\|\||\!': IDENTIFIER,
    r'\-\-|\+\+|\<|\>|\=|\/|\*|\+|\%|\-': OPERATOR,
}


SYNTAX2 = {
    r'^ +': WHITESPACE,
    r'^\,': SEP,
    r'^\-\>': PTR_SCOPE,
    r'^//(.+?)(?=\n|$)': COMMENT,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) +(\((?:[^()]|\([^()]*\))*\))': FUNC_CALL,
    r'^(0(x|X)\d+|-0(x|X)\d+|-\d+|\d+)': NUMBER,
    r'^([-]?[0-9]*\.?[0-9]+)': NUMBER,
    r'^\((?:[^()]|(?R))*\)': ROUND_BRACKETS,
    r'^(\{(?:[^{}]|(?R))*\})': CURLY_BRACKETS,
    r'^\[[^\]]*\]': SQUARE_BRACKETS,
    r'^\"(?:[^""]|(?R))*\"': STRING,
    r"^\'(?:[^'']|(?R))*\'": STRING,
    r'\&\&|\|\||\!': IDENTIFIER,
    r'\-\-|\+\+|\<|\>|\=|\/|\*|\+|\%|\-': OPERATOR,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) +([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)': DIDENTIFIER,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)\*': PTR_IDENTIFIER,
    r'^[_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*': IDENTIFIER,
}

SYNTAX3 = {
    r'\n': NEWLINE,
    r' +': WHITESPACE,
    r'\,': SEP,
    r':': SEP,
    r'^\-\>': PTR_SCOPE,
    r'^//(.+?)(?=\n|$)': COMMENT,
    r'^(0(x|X)\d+|-0(x|X)\d+|-\d+|\d+)': NUMBER,
    r'^([-]?[0-9]*\.?[0-9]+)': NUMBER,
    r'^\((?:[^()]|(?R))*\)': ROUND_BRACKETS,
    r'^(\{(?:[^{}]|(?R))*\})': CURLY_BRACKETS,
    r'^\[[^\]]*\]': SQUARE_BRACKETS,
    r'^\"(?:[^""]|(?R))*\"': STRING,
    r"^\'(?:[^'']|(?R))*\'": STRING,
    r'\&\&|\|\||\!': IDENTIFIER,
    r'\-\-|\+\+|\<|\>|\=|\/|\*|\+|\%|\-': OPERATOR,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)\*': PTR_IDENTIFIER,
    r'^[_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*': IDENTIFIER,
}

SYNTAX4 = {
    r'\n': NEWLINE,
    r' +': WHITESPACE,
    r';': SEMICOLON,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) *= *': VAR_DECL,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) +([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)': DIDENTIFIER,
    r'^[_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*': IDENTIFIER,
    r'^//(.+?)(?=\n|$)': COMMENT,
    r'^(0(x|X)\d+|-0(x|X)\d+|-\d+|\d+)': NUMBER,
    r'^\((?:[^()]|(?R))*\)': ROUND_BRACKETS,
    r'^(\{(?:[^{}]|(?R))*\})': CURLY_BRACKETS,
    r'^\[[^\]]*\]': SQUARE_BRACKETS,
    r'^\"(?:[^""]|(?R))*\"': STRING,
    r"^\'(?:[^'']|(?R))*\'": STRING,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)\*': PTR_IDENTIFIER,
    r'^[_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*': IDENTIFIER,
    r'\&\&|\|\||\!': IDENTIFIER,
    r'\-\-|\+\+|\<|\>|\=|\/|\*|\+|\%|\-': OPERATOR,
}

SYNTAX5 = {
    r'^ +': WHITESPACE,
    r'^\,': SEP,
    r'^\-\>': PTR_SCOPE,
    r'^//(.+?)(?=\n|$)': COMMENT,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*) +(\((?:[^()]|\([^()]*\))*\))': FUNC_CALL,
    r'^(0(x|X)\d+|-0(x|X)\d+|-\d+|\d+)': NUMBER,
    r'^([-]?[0-9]*\.?[0-9]+)': NUMBER,
    r'^\((?:[^()]|(?R))*\)': ROUND_BRACKETS,
    r'^(\{(?:[^{}]|(?R))*\})': CURLY_BRACKETS,
    r'^\[[^\]]*\]': SQUARE_BRACKETS,
    r'^\"(?:[^""]|(?R))*\"': STRING,
    r"^\'(?:[^'']|(?R))*\'": STRING,
    r'\&\&|\|\||\!': IDENTIFIER,
    r'\-\-|\+\+|\<|\>|\=|\/|\*|\+|\%|\-': OPERATOR,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*)\*': PTR_IDENTIFIER,
    r'^[_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::)*': IDENTIFIER,
}