KEYWORD = 'KEYWORD'
USE_KEYWORD = 'USE_KEYWORD'
USE_KEYWORD2 = 'USE_KEYWORD2'
WHITESPACE = 'WHITESPACE'
NEWLINE = 'NEWLINE'
SEMICOLON = 'SEMICOLON'
NUMBER = 'NUMBER'
WHITESPACE = 'WHITESPACE'
ROUND_BRACKETS = 'ROUND_BRACKETS'
CURLY_BRACKETS = 'CURLY_BRACKETS'
SQUARE_BRACKETS = 'SQUARE_BRACKETS'
SQUARE_BRACKETS = 'SQUARE_BRACKETS'
IDENTIFIER = 'IDENTIFIER'
PTR_IDENTIFIER = 'PTR_IDENTIFIER'
STRING = 'STRING'
SEP = 'SEP'
SEP1 = 'SEP1'
COMMENT = 'COMMENT'
MCOMMENT = 'COMMENT_M'
PTR_SCOPE = 'PTR_SCOPE'
OPERATOR = 'OPERATOR'
POWERWORD = 'POWERWORD'
ANGLE_BRACKETS = 'ANGLE_BRACKETS'
SOPERATOR = 'SOPERATOR'

SYNTAX = {
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::|->)*)\*': PTR_IDENTIFIER,
    r'^(?:\*\*|\*)?[_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::|->)*': IDENTIFIER,
    r'\<([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::|->)*)\>': ANGLE_BRACKETS,
    r'^\n': NEWLINE,
    r'^\;': SEMICOLON,
    r'^\s': WHITESPACE,
    r'^\-\>': PTR_SCOPE,
    r'^use|return|yield|raise|class|struct|if|elif|else|try|except|finally|\&\&|\|\||\!': KEYWORD,
    r'^# *(include|del)': POWERWORD,
    r'^//(.+?)(?=\n|$)': COMMENT,
    r'\/\*(?:[^\/\*\*\/]|(?R))*\*\/': MCOMMENT,   
    r'^[-]?[0-9]*\.?[0-9]+|[0-9]+': NUMBER,
    r'^([-]?[0-9]*\.?[0-9]+)': NUMBER,
    r'^\"(?:[^""]|(?R))*\"': STRING,
    r"^\'(?:[^'']|(?R))*\'": STRING,
    r'^\-\-|\+\+|\=|\/|\+|\%|\-|\*': OPERATOR,
    r'^\<|\>': SOPERATOR,
    r'\[(?:[^[\]]|(?R))*\]': SQUARE_BRACKETS,   
    r'\((?:[^()]|(?R))*\)': ROUND_BRACKETS,
    r'\{(?:[^{}]|(?R))*\}': CURLY_BRACKETS,
}

SYNTAX2 = {
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::|->)*)\*': PTR_IDENTIFIER,
    r'^(?:\*\*|\*)?[_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::|->)*': IDENTIFIER,
    r'\<([_a-zA-Z](?:[a-zA-Z0-9_.\[\]]|::|->)*)\>': ANGLE_BRACKETS,
    r'\,': SEP,
    r'\:': SEP1,
    r'^\n': NEWLINE,
    r'^\;': SEMICOLON,
    r'^\s': WHITESPACE,
    r'^\-\>': PTR_SCOPE,
    r'^use|return|yield|raise|class|struct|if|elif|else|try|except|finally|\&\&|\|\||\!': KEYWORD,
    r'^# *(include|del)': POWERWORD,
    r'^//(.+?)(?=\n|$)': COMMENT,
    r'\/\*(?:[^\/\*\*\/]|(?R))*\*\/': MCOMMENT,   
    r'^[-]?[0-9]*\.?[0-9]+|[0-9]+': NUMBER,
    r'^([-]?[0-9]*\.?[0-9]+)': NUMBER,
    r'^\"(?:[^""]|(?R))*\"': STRING,
    r"^\'(?:[^'']|(?R))*\'": STRING,
    r'^\-\-|\+\+|\=|\/|\+|\%|\-|\*': OPERATOR,
    r'^\<|\>': SOPERATOR,
    r'\[(?:[^[\]]|(?R))*\]': SQUARE_BRACKETS,   
    r'\((?:[^()]|(?R))*\)': ROUND_BRACKETS,
    r'\{(?:[^{}]|(?R))*\}': CURLY_BRACKETS,
}