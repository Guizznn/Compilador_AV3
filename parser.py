class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    
    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', None)

    def eat(self, expected_type=None):
        tok = self.current()
        if expected_type and tok[0] != expected_type:
            raise Exception(f"ERRO DE PARSING: Esperado {expected_type}, mas recebeu {tok}")
        self.pos += 1
        return tok

    
    def parse(self):
        nodes = []
        while self.current()[0] != "EOF":
            nodes.append(self.declaration())
        return ("PROGRAM", nodes)

    
    def declaration(self):
        tok_type, tok_value = self.current()

        if tok_type == "INT":
            return self.var_or_function()

        raise Exception(f"ERRO DE PARSING: Declaração inválida {self.current()}")

    def var_or_function(self):
        self.eat("INT")
        id_tok = self.eat("ID")

        
        if self.current()[0] == "LPAREN":
            return self.function_declaration(id_tok)

        
        return self.var_declaration(id_tok)

    
    def var_declaration(self, id_tok):
        if self.current()[0] == "ASSIGN":
            self.eat("ASSIGN")
            expr = self.expression()
            self.eat("SEMICOLON")
            return ("VAR_ASSIGN", id_tok[1], expr)

        self.eat("SEMICOLON")
        return ("VAR_DECL", id_tok[1])

    def function_declaration(self, id_tok):
        self.eat("LPAREN")
        params = self.parameters()
        self.eat("RPAREN")

        body = self.block()

        return ("FUNC_DEF", id_tok[1], params, body)

    def parameters(self):
        params = []

        if self.current()[0] == "INT":
            while True:
                self.eat("INT")
                name = self.eat("ID")[1]
                params.append(name)

                if self.current()[0] != "COMMA":
                    break
                self.eat("COMMA")

        return params

    
   
    def block(self):
        items = []
        self.eat("LBRACE")

        while self.current()[0] != "RBRACE":
            items.append(self.statement())

        self.eat("RBRACE")
        return ("BLOCK", items)

    
    def statement(self):
        tok = self.current()[0]

        if tok == "INT":
            return self.var_or_function()

        if tok == "RETURN":
            return self.return_statement()

        if tok == "IF":
            return self.if_statement()

        if tok == "WHILE":
            return self.while_statement()


        node = self.expression()
        self.eat("SEMICOLON")
        return node

    
    def return_statement(self):
        self.eat("RETURN")
        expr = self.expression()
        self.eat("SEMICOLON")
        return ("RETURN", expr)

    def if_statement(self):
        self.eat("IF")
        self.eat("LPAREN")
        cond = self.expression()
        self.eat("RPAREN")

        then_block = self.block()

        else_block = None
        if self.current()[0] == "ELSE":
            self.eat("ELSE")
            else_block = self.block()

        return ("IF", cond, then_block, else_block)

  
    def while_statement(self):
        self.eat("WHILE")
        self.eat("LPAREN")
        cond = self.expression()
        self.eat("RPAREN")
        body = self.block()
        return ("WHILE", cond, body)

   
    def expression(self):
        return self.assignment()

    def assignment(self):
        node = self.logical_or()

       
        if self.current()[0] == "ASSIGN" and node[0] == "VAR":
            self.eat("ASSIGN")
            value = self.assignment()
            return ("ASSIGN", node[1], value)

        return node

    def logical_or(self):
        node = self.logical_and()

        while self.current()[0] == "OR":
            op = self.eat("OR")[0]
            right = self.logical_and()
            node = ("BINOP", op, node, right)

        return node

    def logical_and(self):
        node = self.equality()

        while self.current()[0] == "AND":
            op = self.eat("AND")[0]
            right = self.equality()
            node = ("BINOP", op, node, right)

        return node

    def equality(self):
        node = self.relational()

        while self.current()[0] in ("EQ", "NEQ"):
            op = self.eat(self.current()[0])[0]
            right = self.relational()
            node = ("BINOP", op, node, right)

        return node

    def relational(self):
        node = self.term()

        while self.current()[0] in ("LT", "GT", "LE", "GE"):
            op = self.eat(self.current()[0])[0]
            right = self.term()
            node = ("BINOP", op, node, right)

        return node

    def term(self):
        node = self.factor()

        while self.current()[0] in ("PLUS", "MINUS"):
            op = self.eat(self.current()[0])[0]
            right = self.factor()
            node = ("BINOP", op, node, right)

        return node

    def factor(self):
        node = self.unary()

        while self.current()[0] in ("MUL", "DIV"):
            op = self.eat(self.current()[0])[0]
            right = self.unary()
            node = ("BINOP", op, node, right)

        return node

    def unary(self):
        tok = self.current()[0]

        if tok in ("PLUS", "MINUS", "NOT"):
            op = self.eat(tok)[0]
            right = self.unary()
            return ("UNARY", op, right)

        return self.primary()

    def primary(self):
        tok_type, tok_value = self.current()

        if tok_type == "NUMBER":
            self.eat("NUMBER")
            return ("NUMBER", tok_value)

        if tok_type == "ID":
            self.eat("ID")

            # chamada de função
            if self.current()[0] == "LPAREN":
                return self.function_call(tok_value)

            return ("VAR", tok_value)

        if tok_type == "LPAREN":
            self.eat("LPAREN")
            expr = self.expression()
            self.eat("RPAREN")
            return expr

        raise Exception(f"ERRO DE PARSING: Expressão inválida em {self.current()}")

    def function_call(self, func_name):
        self.eat("LPAREN")
        args = []

        if self.current()[0] != "RPAREN":
            while True:
                args.append(self.expression())
                if self.current()[0] != "COMMA":
                    break
                self.eat("COMMA")

        self.eat("RPAREN")
        return ("CALL", func_name, args)
