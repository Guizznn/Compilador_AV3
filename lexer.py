import re


TOKEN_SPEC = [

   
    ("COMMENT", r"//.*"),
    ("MULTI_COMMENT", r"/\*[\s\S]*?\*/"),
    ("PREPROCESSOR", r"#[^\n]*"),

 
    ("SKIP", r"[ \t\n\r]+"),


    ("AUTO", r"auto\b"),
    ("BREAK", r"break\b"),
    ("CASE", r"case\b"),
    ("CHAR", r"char\b"),
    ("CONST", r"const\b"),
    ("CONTINUE", r"continue\b"),
    ("DEFAULT", r"default\b"),
    ("DO", r"do\b"),
    ("DOUBLE", r"double\b"),
    ("ELSE", r"else\b"),
    ("ENUM", r"enum\b"),
    ("EXTERN", r"extern\b"),
    ("FLOAT", r"float\b"),
    ("FOR", r"for\b"),
    ("GOTO", r"goto\b"),
    ("IF", r"if\b"),
    ("INLINE", r"inline\b"),
    ("INT", r"int\b"),
    ("LONG", r"long\b"),
    ("REGISTER", r"register\b"),
    ("RESTRICT", r"restrict\b"),
    ("RETURN", r"return\b"),
    ("SHORT", r"short\b"),
    ("SIGNED", r"signed\b"),
    ("SIZEOF", r"sizeof\b"),
    ("STATIC", r"static\b"),
    ("STRUCT", r"struct\b"),
    ("SWITCH", r"switch\b"),
    ("TYPEDEF", r"typedef\b"),
    ("UNION", r"union\b"),
    ("UNSIGNED", r"unsigned\b"),
    ("VOID", r"void\b"),
    ("VOLATILE", r"volatile\b"),
    ("WHILE", r"while\b"),


    ("STRING", r"\"([^\"\\]|\\.)*\""),
    ("CHAR_LITERAL", r"'([^'\\]|\\.)'"),
    ("NUMBER", r"0[xX][0-9a-fA-F]+([uU]|[lL]{1,2})?|\b\d+(\.\d+)?([eE][+-]?\d+)?([uU]|[lL]{1,2})?\b"),

    ("EQ", r"=="),
    ("NEQ", r"!="),
    ("LE", r"<="),
    ("GE", r">="),
    ("SHIFT_LEFT_ASSIGN", r"<<="),
    ("SHIFT_RIGHT_ASSIGN", r">>="),

    ("PLUS_ASSIGN", r"\+="),
    ("MINUS_ASSIGN", r"-="),
    ("MUL_ASSIGN", r"\*="),
    ("DIV_ASSIGN", r"/="),
    ("MOD_ASSIGN", r"%="),
    ("BIT_AND_ASSIGN", r"&="),
    ("BIT_OR_ASSIGN", r"\|="),
    ("BIT_XOR_ASSIGN", r"\^="),


    ("INCREMENT", r"\+\+"),
    ("DECREMENT", r"--"),



    ("LOGICAL_AND", r"&&"),
    ("LOGICAL_OR", r"\|\|"),

    ("SHIFT_LEFT", r"<<"),
    ("SHIFT_RIGHT", r">>"),

    ("ARROW", r"->"),

   
    ("LT", r"<"),
    ("GT", r">"),

    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MULTIPLY", r"\*"),
    ("DIVIDE", r"/"),
    ("MOD", r"%"),

    ("ASSIGN", r"="),

    ("AND", r"&"),
    ("OR", r"\|"),
    ("XOR", r"\^"),
    ("NOT", r"!"),
    ("TILDE", r"~"),



    ("QUESTION", r"\?"),
    ("COLON", r":"),

    
    ("SEMICOLON", r";"),
    ("COMMA", r","),

    ("ELLIPSIS", r"\.\.\."),
    ("DOT", r"\."),



    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),

    
    ("ID", r"[A-Za-z_]\w*"),
]


token_regex = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))

def lexer(code):
    tokens = []
    for match in token_regex.finditer(code):
        kind = match.lastgroup
        value = match.group()

        if kind in ("SKIP", "COMMENT", "MULTI_COMMENT", "PREPROCESSOR"):
            continue  

        tokens.append((kind, value))
    return tokens

