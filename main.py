# main.py
from lexer import lexer
from parser import Parser, pretty

with open("teste.c", "r", encoding="utf-8") as f:
    code = f.read()

tokens = lexer(code)
# append EOF sentinel so parser can detect end
tokens.append(("EOF",""))
parser = Parser(tokens)
ast = parser.parse()

print(pretty(ast))
