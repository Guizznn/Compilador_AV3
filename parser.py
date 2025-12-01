from dataclasses import dataclass
from typing import List, Optional, Any, Union
import lexer



@dataclass
class Node:
    pass

@dataclass
class TranslationUnit(Node):
    external_declarations: List[Node]

@dataclass
class FunctionDefinition(Node):
    specifiers: List[str]
    declarator: Any
    body: Any  

@dataclass
class Declaration(Node):
    specifiers: List[str]
    init_declarators: List[Any]  

@dataclass
class Typedef(Node):
    declaration: Declaration

@dataclass
class Declarator(Node):
    pointer: int
    direct_decl: Any  

@dataclass
class Identifier(Node):
    name: str

@dataclass
class CompoundStatement(Node):
    items: List[Node]  

@dataclass
class IfStatement(Node):
    cond: Node
    then_stmt: Node
    else_stmt: Optional[Node]

@dataclass
class WhileStatement(Node):
    cond: Node
    body: Node

@dataclass
class ForStatement(Node):
    init: Optional[Node]
    cond: Optional[Node]
    post: Optional[Node]
    body: Node

@dataclass
class SwitchStatement(Node):
    cond: Node
    body: Node 

@dataclass
class CaseStatement(Node):
    expr: Optional[Node] 
    body: List[Node]

@dataclass
class DoWhileStatement(Node):
    body: Node
    cond: Node

@dataclass
class ReturnStatement(Node):
    expr: Optional[Node]

@dataclass
class ExpressionStatement(Node):
    expr: Optional[Node]

@dataclass
class BreakStatement(Node):
    pass

@dataclass
class ContinueStatement(Node):
    pass

@dataclass
class BinaryOp(Node):
    op: str
    left: Node
    right: Node

@dataclass
class UnaryOp(Node):
    op: str
    operand: Node

@dataclass
class TernaryOp(Node):
    cond: Node
    if_true: Node
    if_false: Node

@dataclass
class Assignment(Node):
    op: str
    left: Node
    right: Node

@dataclass
class Call(Node):
    func: Node
    args: List[Node]

@dataclass
class Constant(Node):
    value: Any

@dataclass
class ArraySubscript(Node):
    array: Node
    index: Node

@dataclass
class MemberAccess(Node):
    target: Node
    member: str
    arrow: bool  



class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # utility
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ("EOF", "")

    def next(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def accept(self, kind):
        if self.peek()[0] == kind:
            return self.next()
        return None

    def expect(self, kind):
        tok = self.next()
        if tok[0] != kind:
            prev_tok = self.tokens[self.pos - 2] if self.pos > 1 else ("START", "")
            raise ParseError(f"Expected {kind}, got {tok} (after {prev_tok})")
        return tok

    
    def parse(self):
        units = []
        while self.peek()[0] != "EOF":
            if self.peek()[0] == "SEMICOLON":
                self.next()
                continue
            try:
                units.append(self.parse_external_declaration())
            except ParseError as e:
                
                if self.peek()[0] != "EOF":
                    self.next() 
                raise e
                
        return TranslationUnit(units)

    def parse_external_declaration(self):
        specifiers = self.parse_decl_specifiers()

        
        if self.peek()[0] == "SEMICOLON":
            self.expect("SEMICOLON")
            return Declaration(specifiers, [])

        declarator = self.parse_declarator_optional()
        
        
        if self.peek()[0] == "LBRACE":
            body = self.parse_compound_statement()
            return FunctionDefinition(specifiers, declarator, body)
            
        
        init_declarators = []
        if declarator is not None:
            init = None
            if self.accept("ASSIGN"):
                init = self.parse_assignment_expression()
            init_declarators.append((declarator, init))
            
        while self.accept("COMMA"):
            dec = self.parse_declarator()
            init = None
            if self.accept("ASSIGN"):
                init = self.parse_assignment_expression()
            init_declarators.append((dec, init))
            
        self.expect("SEMICOLON")
        return Declaration(specifiers, init_declarators)

    def parse_decl_specifiers(self):
        spec = []
        while True:
            tok = self.peek()
            kind = tok[0]
            
            if kind in {"INT","FLOAT","CHAR","VOID","DOUBLE","LONG","SHORT","SIGNED","UNSIGNED","TYPEDEF","STATIC","EXTERN","AUTO","REGISTER","CONST","VOLATILE"}:
                spec.append(self.next()[1])
                
            elif kind in {"STRUCT", "UNION", "ENUM"}:
                spec.append(self.next()[1]) 
                
                if self.peek()[0] == "ID":
                    spec.append(self.next()[1]) 
                
                if self.accept("LBRACE"):
                    balance = 1
                    while balance > 0 and self.peek()[0] != "EOF":
                        next_tok = self.next()
                        if next_tok[0] == "LBRACE":
                            balance += 1
                        elif next_tok[0] == "RBRACE":
                            balance -= 1
                    if balance != 0:
                        raise ParseError("Unclosed structure/enum block")
                    
            else:
                break
        return spec

    def parse_declarator_optional(self):
        tok = self.peek()
        if tok[0] in {"ID","LPAREN","MULTIPLY"}:
            return self.parse_declarator()
        return None

    def parse_declarator(self):
        pointer = 0
        while self.accept("MULTIPLY"):
            pointer += 1
            
        name = None
        
        if self.peek()[0] == "ID":
            name = self.next()[1]
        elif self.accept("LPAREN"):
            dec = self.parse_declarator()
            self.expect("RPAREN")
            name = dec.direct_decl if isinstance(dec, Declarator) else None
        else:
             pass 

        while True:
            if self.peek()[0] == "LPAREN":
                self.expect("LPAREN")
                
                if self.peek()[0] != "RPAREN":
                    self.parse_parameter_declaration()
                    while self.accept("COMMA"):
                        self.parse_parameter_declaration() 
                
                self.expect("RPAREN")
            
            elif self.peek()[0] == "LBRACKET":
                self.expect("LBRACKET")
                if self.peek()[0] != "RBRACKET":
                     self.parse_expression()
                self.expect("RBRACKET")
            else:
                break
                
        return Declarator(pointer, Identifier(name) if name else None)

    def parse_parameter_declaration(self):
        self.parse_decl_specifiers()
        self.parse_declarator_optional()

    
    def parse_statement(self):
        t = self.peek()
        if t[0] == "LBRACE":
            return self.parse_compound_statement()
        if t[0] == "IF":
            self.next()
            self.expect("LPAREN")
            cond = self.parse_expression()
            self.expect("RPAREN")
            then_stmt = self.parse_statement()
            else_stmt = None
            if self.accept("ELSE"):
                else_stmt = self.parse_statement()
            return IfStatement(cond, then_stmt, else_stmt)
        if t[0] == "WHILE":
            self.next()
            self.expect("LPAREN")
            cond = self.parse_expression()
            self.expect("RPAREN")
            body = self.parse_statement()
            return WhileStatement(cond, body)
        if t[0] == "SWITCH":
            self.next()
            self.expect("LPAREN")
            cond = self.parse_expression()
            self.expect("RPAREN")
            body = self.parse_compound_statement() 
            return SwitchStatement(cond, body)
        if t[0] == "DO":
            self.next()
            body = self.parse_statement()
            self.expect("WHILE")
            self.expect("LPAREN")
            cond = self.parse_expression()
            self.expect("RPAREN")
            self.expect("SEMICOLON")
            return DoWhileStatement(body, cond)
        if t[0] == "FOR":
            self.next()
            self.expect("LPAREN")
            init = None
            if self.peek()[0] != "SEMICOLON":
                if self.peek()[0] in {"INT","FLOAT","CHAR","DOUBLE","LONG","VOID","SHORT"}:
                    init = self.parse_external_declaration() 
                else:
                    init = self.parse_expression_statement()
            else:
                self.expect("SEMICOLON")
                
            cond = None
            if self.peek()[0] != "SEMICOLON":
                cond = self.parse_expression()
            self.expect("SEMICOLON")
            
            post = None
            if self.peek()[0] != "RPAREN":
                post = self.parse_expression()
            self.expect("RPAREN")
            body = self.parse_statement()
            return ForStatement(init, cond, post, body)
        if t[0] == "RETURN":
            self.next()
            expr = None
            if self.peek()[0] != "SEMICOLON":
                expr = self.parse_expression()
            self.expect("SEMICOLON")
            return ReturnStatement(expr)
        if t[0] == "BREAK":
            self.next()
            self.expect("SEMICOLON")
            return BreakStatement()
        if t[0] == "CONTINUE":
            self.next()
            self.expect("SEMICOLON")
            return ContinueStatement()
            
        if t[0] in {"INT","FLOAT","CHAR","DOUBLE","LONG","SHORT","SIGNED","UNSIGNED","CONST","STATIC", "TYPEDEF", "STRUCT", "UNION", "ENUM", "VOID"}:
            return self.parse_external_declaration()
            
        return self.parse_expression_statement()

    def parse_compound_statement(self):
        self.expect("LBRACE")
        items = []
        while self.peek()[0] != "RBRACE":
            if self.peek()[0] == "EOF":
                raise ParseError("Unclosed compound statement")
            
            if self.peek()[0] == "CASE" or self.peek()[0] == "DEFAULT":
                items.append(self.parse_case_statement())
            elif self.peek()[0] in {"INT","FLOAT","CHAR","DOUBLE","LONG","SHORT","SIGNED","UNSIGNED","CONST","STATIC","TYPEDEF","STRUCT","UNION","ENUM", "VOID"}:
                items.append(self.parse_external_declaration())
            else:
                items.append(self.parse_statement())
        self.expect("RBRACE")
        return CompoundStatement(items)

    def parse_case_statement(self):
        if self.accept("CASE"):
            expr = self.parse_expression()
            self.expect("COLON")
        elif self.accept("DEFAULT"):
            expr = None
            self.expect("COLON")
        else:
            raise ParseError(f"Expected CASE or DEFAULT, got {self.peek()}")
        
        body = []
        while self.peek()[0] not in {"CASE", "DEFAULT", "RBRACE", "EOF"}:
            if self.peek()[0] in {"INT","FLOAT","CHAR","DOUBLE","LONG","SHORT","SIGNED","UNSIGNED","CONST","STATIC","TYPEDEF","STRUCT","UNION","ENUM", "VOID"}:
                body.append(self.parse_external_declaration())
            else:
                body.append(self.parse_statement())
        
        return CaseStatement(expr, body)

    def parse_expression_statement(self):
        if self.peek()[0] == "SEMICOLON":
            self.next()
            return ExpressionStatement(None)
        expr = self.parse_expression()
        self.expect("SEMICOLON")
        return ExpressionStatement(expr)

   

    PRECEDENCE = {
        "ASSIGN": 1, "PLUS_ASSIGN": 1, "MINUS_ASSIGN": 1,
        "QUESTION": 2, 
        "LOGICAL_OR": 3, "LOGICAL_AND": 4,
        "OR": 5, "XOR": 6, "AND": 7,
        "EQUAL": 8, "NOT_EQUAL": 8,
        "LESS": 9, "GREATER": 9, "LESS_EQUAL": 9, "GREATER_EQUAL": 9,
        "SHIFT_LEFT": 10, "SHIFT_RIGHT": 10,
        "PLUS": 11, "MINUS": 11,
        "MULTIPLY": 12, "DIVIDE": 12, "MOD": 12,
        "UNARY": 13, "POSTFIX": 14,
    }

    def parse_expression(self):
        return self.parse_assignment_expression()

    def parse_assignment_expression(self):
        left = self.parse_conditional_expression()
        if self.peek()[0] in {"ASSIGN","PLUS_ASSIGN","MINUS_ASSIGN","MUL_ASSIGN","DIV_ASSIGN","MOD_ASSIGN","BIT_AND_ASSIGN","BIT_OR_ASSIGN","BIT_XOR_ASSIGN","SHIFT_LEFT_ASSIGN","SHIFT_RIGHT_ASSIGN"}:
            op = self.next()[0]
            right = self.parse_assignment_expression()
            return Assignment(op, left, right)
        return left

    def parse_conditional_expression(self):
        cond = self.parse_logical_or()
        if self.accept("QUESTION"):
            if_true = self.parse_expression()
            self.expect("COLON")
            if_false = self.parse_conditional_expression()
            return TernaryOp(cond, if_true, if_false)
        return cond

    def parse_logical_or(self):
        node = self.parse_logical_and()
        while self.accept("LOGICAL_OR"):
            right = self.parse_logical_and()
            node = BinaryOp("||", node, right)
        return node

    def parse_logical_and(self):
        node = self.parse_bit_or()
        while self.accept("LOGICAL_AND"):
            right = self.parse_bit_or()
            node = BinaryOp("&&", node, right)
        return node

    def parse_bit_or(self):
        node = self.parse_bit_xor()
        while self.accept("OR"):
            right = self.parse_bit_xor()
            node = BinaryOp("|", node, right)
        return node

    def parse_bit_xor(self):
        node = self.parse_bit_and()
        while self.accept("XOR"):
            right = self.parse_bit_and()
            node = BinaryOp("^", node, right)
        return node

    def parse_bit_and(self):
        node = self.parse_equality()
        while self.accept("AND"):
            right = self.parse_equality()
            node = BinaryOp("&", node, right)
        return node

    def parse_equality(self):
        node = self.parse_relational()
        while True:
            if self.accept("EQUAL"):
                right = self.parse_relational()
                node = BinaryOp("==", node, right)
            elif self.accept("NOT_EQUAL"):
                right = self.parse_relational()
                node = BinaryOp("!=", node, right)
            else:
                break
        return node

    def parse_relational(self):
        node = self.parse_shift()
        while True:
            if self.accept("LESS"):
                right = self.parse_shift()
                node = BinaryOp("<", node, right)
            elif self.accept("GREATER"):
                right = self.parse_shift()
                node = BinaryOp(">", node, right)
            elif self.accept("LESS_EQUAL"):
                right = self.parse_shift()
                node = BinaryOp("<=", node, right)
            elif self.accept("GREATER_EQUAL"):
                right = self.parse_shift()
                node = BinaryOp(">=", node, right)
            else:
                break
        return node

    def parse_shift(self):
        node = self.parse_additive()
        while True:
            if self.accept("SHIFT_LEFT"):
                right = self.parse_additive()
                node = BinaryOp("<<", node, right)
            elif self.accept("SHIFT_RIGHT"):
                right = self.parse_additive()
                node = BinaryOp(">>", node, right)
            else:
                break
        return node

    def parse_additive(self):
        node = self.parse_multiplicative()
        while True:
            if self.accept("PLUS"):
                right = self.parse_multiplicative()
                node = BinaryOp("+", node, right)
            elif self.accept("MINUS"):
                right = self.parse_multiplicative()
                node = BinaryOp("-", node, right)
            else:
                break
        return node

    def parse_multiplicative(self):
        node = self.parse_unary()
        while True:
            if self.accept("MULTIPLY"):
                right = self.parse_unary()
                node = BinaryOp("*", node, right)
            elif self.accept("DIVIDE"):
                right = self.parse_unary()
                node = BinaryOp("/", node, right)
            elif self.accept("MOD"):
                right = self.parse_unary()
                node = BinaryOp("%", node, right)
            else:
                break
        return node

    def parse_unary(self):
        if self.accept("PLUS"):
            return UnaryOp("+u", self.parse_unary())
        if self.accept("MINUS"):
            return UnaryOp("-u", self.parse_unary())
        if self.accept("NOT"):
            return UnaryOp("!", self.parse_unary())
        if self.accept("TILDE"):
            return UnaryOp("~", self.parse_unary())
        if self.accept("INCREMENT"):
            return UnaryOp("++pre", self.parse_unary())
        if self.accept("DECREMENT"):
            return UnaryOp("--pre", self.parse_unary())
        if self.accept("MULTIPLY"):
            return UnaryOp("*", self.parse_unary())
        if self.accept("AND"):
            return UnaryOp("&", self.parse_unary())
        return self.parse_postfix()

    def parse_postfix(self):
        node = self.parse_primary()
        while True:
            if self.accept("LPAREN"):
               
                args = []
                if self.peek()[0] != "RPAREN":
                    args.append(self.parse_assignment_expression())
                    while self.accept("COMMA"):
                        args.append(self.parse_assignment_expression())
                self.expect("RPAREN")
                node = Call(node, args)
            elif self.accept("LBRACKET"):
                idx = self.parse_expression()
                self.expect("RBRACKET")
                node = ArraySubscript(node, idx)
            elif self.accept("DOT"):
                name = self.expect("ID")[1]
                node = MemberAccess(node, name, arrow=False)
            elif self.accept("ARROW"):
                name = self.expect("ID")[1]
                node = MemberAccess(node, name, arrow=True)
            elif self.accept("INCREMENT"):
                node = UnaryOp("++post", node)
            elif self.accept("DECREMENT"):
                node = UnaryOp("--post", node)
            else:
                break
        return node

    def parse_primary(self):
        tok = self.peek()
        if tok[0] == "NUMBER":
            self.next()
            value_str = tok[1].lower().rstrip('ul')
            try:
                if 'x' in value_str:
                    return Constant(int(value_str, 16))
                if '.' in value_str or 'e' in value_str:
                    return Constant(float(value_str))
                return Constant(int(value_str))
            except ValueError:
                return Constant(tok[1])
                
        if tok[0] == "STRING":
            self.next()
            return Constant(tok[1])
        if tok[0] == "CHAR_LITERAL":
            self.next()
            return Constant(tok[1])
        if tok[0] == "ID":
            name = self.next()[1]
            return Identifier(name)
        if tok[0] == "LPAREN":
            self.next()
            expr = self.parse_expression()
            self.expect("RPAREN")
            return expr
        raise ParseError(f"Unexpected primary token: {tok}")


LABEL_MAP = {
    'TranslationUnit': 'PROGRAM',
    'FunctionDefinition': 'FUNC_DEF',
    'Declaration': 'VAR_DEF',
    'CompoundStatement': 'BLOCK',
    'ExpressionStatement': 'E_STMT',
    'ReturnStatement': 'RETURN',
    'IfStatement': 'IF',
    'BinaryOp': 'BINOP',
    'UnaryOp': 'UNOP',
    'Assignment': 'VAR_ASSIGN',
    'Call': 'CALL',
    'Constant': 'NUMBER',
    'Identifier': 'VAR',
}

def pretty_compact(node):
   
    if node is None:
        return ""

    node_type = type(node).__name__
    label = LABEL_MAP.get(node_type, node_type.upper())

    children = []
    
    if isinstance(node, TranslationUnit):
        children.extend(node.external_declarations)
        
    elif isinstance(node, FunctionDefinition):
        func_name = node.declarator.direct_decl.name if node.declarator and node.declarator.direct_decl else "Anon"
        
        params = '[]' 
        
        children.append(func_name)
        children.append(params) 
        children.append(node.body)

    elif isinstance(node, CompoundStatement):
        children.extend(node.items)

    elif isinstance(node, Declaration):
        if node.init_declarators:
            dec, init = node.init_declarators[0]
            children.append(dec.direct_decl.name) 
            if init:
                children.append(init)
        
    elif isinstance(node, ExpressionStatement):
        if node.expr:
            children.append(node.expr)
            
    elif isinstance(node, ReturnStatement):
        if node.expr:
            children.append(node.expr)

    elif isinstance(node, IfStatement):
        children.append(node.cond)
        children.append(node.then_stmt)
        if node.else_stmt:
            children.append(node.else_stmt)
            
    elif isinstance(node, Assignment):
        children.append(node.left)
        children.append(node.right)
        
    elif isinstance(node, BinaryOp):
        op_label = node.op.upper() 
        children.append(op_label)
        children.append(node.left)
        children.append(node.right)
        
    elif isinstance(node, Call):
        func_name = node.func.name
        args = [pretty_compact(arg) for arg in node.args]
        return f"('{label}', '{func_name}', [{', '.join(args)}])"
        
    elif isinstance(node, Constant):
        val = node.value
       
        if isinstance(val, (int, float)):
            val_str = str(float(val)) if isinstance(val, float) or '.' in str(val) else str(val)
        else:
            val_str = f"'{val}'"
            
        return f"('{label}', {val_str})"
        
    elif isinstance(node, Identifier):
        return f"('{label}', '{node.name}')"

    
    if node_type in ['Declarator', 'Typedef', 'CaseStatement', 'DoWhileStatement', 'ForStatement', 'SwitchStatement', 'UnaryOp']:
        return None

    
    child_results = [pretty_compact(child) for child in children if child is not None]

    
    if not child_results:
        return f"('{label}')"
    else:
        
        if isinstance(node, BinaryOp):
            return f"('{label}', '{child_results[0]}', {child_results[1]}, {child_results[2]})"
            
        
        return f"('{label}', {', '.join(child_results)})"