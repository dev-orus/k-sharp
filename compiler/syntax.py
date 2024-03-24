KEYWORD = 'KEYWORD'
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
COMMENT = 'COMMENT'
PTR_SCOPE = 'PTR_SCOPE'
OPERATOR = 'OPERATOR'
POWERWORD = 'POWERWORD'
ANGLE_BRACKETS = 'ANGLE_BRACKETS'

SYNTAX = {
    r'^\n': NEWLINE,
    r'^\;': SEMICOLON,
    r'^\s': WHITESPACE,
    r'^\-\>': PTR_SCOPE,
    r'^return|yield|raise|class|struct|if|elif|else|try|except|finally|\&\&|\|\||\!': KEYWORD,
    r'^# *(include|del)': POWERWORD,
    r'^//(.+?)(?=\n|$)': COMMENT,
    r'^(0(x|X)\d+|-0(x|X)\d+|-\d+|\d+)': NUMBER,
    r'^([-]?[0-9]*\.?[0-9]+)': NUMBER,
    r'^\"(?:[^""]|(?R))*\"': STRING,
    r"^\'(?:[^'']|(?R))*\'": STRING,
    r'^([_a-zA-Z](?:[a-zA-Z0-9_.]|::|->)*)\*': PTR_IDENTIFIER,
    r'^[_a-zA-Z](?:[a-zA-Z0-9_.]|::|->)*': IDENTIFIER,
    r'^\-\-|\+\+|\<|\>|\=|\/|\*|\+|\%|\-': OPERATOR,
    r'\<(?:[^<>]|(?R))*\>': ANGLE_BRACKETS,
    r'\[(?:[^[\]]|(?R))*\]': SQUARE_BRACKETS,
    r'\((?:[^()]|(?R))*\)': ROUND_BRACKETS,
    r'\{(?:[^{}]|(?R))*\}': CURLY_BRACKETS,
}