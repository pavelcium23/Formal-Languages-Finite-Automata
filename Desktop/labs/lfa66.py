import sys
from enum import Enum
from typing import List, Union, Optional

# Token Types
class TokenType(Enum):
    TOKEN_EOF = 0
    TOKEN_NUMBER = 1
    TOKEN_ID = 2
    TOKEN_EQUALS = 3
    TOKEN_EQUALITY = 4
    TOKEN_SMALLER = 5
    TOKEN_SMALLER_EQUAL = 6
    TOKEN_GREATER = 7
    TOKEN_GREATER_EQUAL = 8
    TOKEN_SEMI = 9
    TOKEN_LPAREN = 10
    TOKEN_RPAREN = 11
    TOKEN_LBRACE = 12
    TOKEN_RBRACE = 13
    TOKEN_COMMA = 14
    TOKEN_PLUS = 15
    TOKEN_MINUS = 16
    TOKEN_MULTIPLY = 17
    TOKEN_DIVIDE = 18

# AST Node Types
class NodeType(Enum):
    PROGRAM = 0
    BINARY_EXPR = 1
    IDENTIFIER = 2
    NUMERIC_LITERAL = 3
    WHILE_STATEMENT = 4
    CONDITIONAL_EXPR = 5
    ASSIGNMENT = 6

class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, contents: str):
        self.contents = contents
        self.i = 0
        self.c = contents[self.i] if contents else '\0'
    
    def advance(self):
        if self.c != '\0' and self.i < len(self.contents) - 1:
            self.i += 1
            self.c = self.contents[self.i]
        else:
            self.c = '\0'
    
    def retreat(self):
        if self.i > 0:
            self.i -= 1
            self.c = self.contents[self.i]
    
    def skip_whitespace(self):
        while self.c == ' ' or self.c == '\n':
            self.advance()
    
    def get_current_char_as_string(self) -> str:
        return self.c
    
    def collect_id(self) -> Token:
        value = ''
        while self.c.isalnum():
            value += self.c
            self.advance()
        return Token(TokenType.TOKEN_ID, value)
    
    def advance_with_token(self, token: Token) -> Token:
        self.advance()
        return token
    
    def get_next_token(self) -> Token:
        while self.c != '\0':
            if self.c == ' ' or self.c == '\n':
                self.skip_whitespace()
                continue
            
            if self.c.isdigit() or self.c == '.':
                value = ''
                while self.c.isdigit() or self.c == '.':
                    value += self.c
                    self.advance()
                return Token(TokenType.TOKEN_NUMBER, value)
            
            if self.c.isalnum():
                return self.collect_id()
            
            # Handle multi-character operators
            if self.c == '=':
                self.advance()
                if self.c == '=':
                    self.advance()
                    return Token(TokenType.TOKEN_EQUALITY, "==")
                else:
                    return Token(TokenType.TOKEN_EQUALS, "=")
            
            elif self.c == '<':
                self.advance()
                if self.c == '=':
                    self.advance()
                    return Token(TokenType.TOKEN_SMALLER_EQUAL, "<=")
                else:
                    return Token(TokenType.TOKEN_SMALLER, "<")
            
            elif self.c == '>':
                self.advance()
                if self.c == '=':
                    self.advance()
                    return Token(TokenType.TOKEN_GREATER_EQUAL, ">=")
                else:
                    return Token(TokenType.TOKEN_GREATER, ">")
            
            # Handle single-character tokens
            elif self.c == ';':
                token = Token(TokenType.TOKEN_SEMI, self.c)
                self.advance()
                return token
            elif self.c == '(':
                token = Token(TokenType.TOKEN_LPAREN, self.c)
                self.advance()
                return token
            elif self.c == ')':
                token = Token(TokenType.TOKEN_RPAREN, self.c)
                self.advance()
                return token
            elif self.c == '{':
                token = Token(TokenType.TOKEN_LBRACE, self.c)
                self.advance()
                return token
            elif self.c == '}':
                token = Token(TokenType.TOKEN_RBRACE, self.c)
                self.advance()
                return token
            elif self.c == ',':
                token = Token(TokenType.TOKEN_COMMA, self.c)
                self.advance()
                return token
            elif self.c == '+':
                token = Token(TokenType.TOKEN_PLUS, self.c)
                self.advance()
                return token
            elif self.c == '-':
                token = Token(TokenType.TOKEN_MINUS, self.c)
                self.advance()
                return token
            elif self.c == '*':
                token = Token(TokenType.TOKEN_MULTIPLY, self.c)
                self.advance()
                return token
            elif self.c == '/':
                token = Token(TokenType.TOKEN_DIVIDE, self.c)
                self.advance()
                return token
            
            else:
                print(f"Unknown token: {self.c}")
                self.advance()
        
        return Token(TokenType.TOKEN_EOF, '\0')

class Expr:
    def __init__(self, kind: NodeType):
        self.kind = kind
    
    def __repr__(self):
        return f"{self.kind.name}"

class BinaryExpr(Expr):
    def __init__(self, left: Expr, right: Expr, op: str):
        super().__init__(NodeType.BINARY_EXPR)
        self.left = left
        self.right = right
        self.op = op
    
    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"

class Identifier(Expr):
    def __init__(self, symbol: str):
        super().__init__(NodeType.IDENTIFIER)
        self.symbol = symbol
    
    def __repr__(self):
        return f"ID({self.symbol})"

class NumericLiteral(Expr):
    def __init__(self, value: float):
        super().__init__(NodeType.NUMERIC_LITERAL)
        self.value = value
    
    def __repr__(self):
        return f"NUM({self.value})"

class ConditionalExpr(Expr):
    def __init__(self, left: Expr, right: Expr, op: str):
        super().__init__(NodeType.CONDITIONAL_EXPR)
        self.left = left
        self.right = right
        self.op = op
    
    def __repr__(self):
        return f"COND({self.left} {self.op} {self.right})"

class AssignmentExpr(Expr):
    def __init__(self, name: str, value: Expr):
        super().__init__(NodeType.ASSIGNMENT)
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"ASSIGN({self.name} = {self.value})"

class Stmt:
    def __init__(self, kind: NodeType):
        self.kind = kind
    
    def __repr__(self):
        return f"{self.kind.name}"

class WhileStmt(Stmt):
    def __init__(self, condition: Expr, body: List[Stmt]):
        super().__init__(NodeType.WHILE_STATEMENT)
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        body_str = '\n'.join(f"  {stmt}" for stmt in self.body)
        return f"WHILE ({self.condition}) {{\n{body_str}\n}}"

class Program:
    def __init__(self, body: List[Stmt]):
        self.kind = NodeType.PROGRAM
        self.body = body
    
    def __repr__(self):
        return '\n'.join(str(stmt) for stmt in self.body)

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()
        self.prev_token = self.current_token
    
    def advance(self):
        self.prev_token = self.current_token
        self.current_token = self.lexer.get_next_token()
        return self.current_token
    
    def eat(self, token_type: TokenType):
        if self.current_token.type == token_type:
            self.advance()
        else:
            print(f"Unexpected token `{self.current_token.value}`, expected {token_type}", file=sys.stderr)
            sys.exit(1)
    
    def produce_ast(self) -> Program:
        program = Program([])
        while self.current_token.type != TokenType.TOKEN_EOF:
            program.body.append(self.parse_stmt())
            if self.current_token.type == TokenType.TOKEN_SEMI:
                self.eat(TokenType.TOKEN_SEMI)
        return program
    
    def parse_stmt(self) -> Stmt:
        if self.current_token.type == TokenType.TOKEN_ID:
            if self.current_token.value == "while":
                return self.parse_while()
            elif self.current_token.value in ("int", "float"):
                pass  # TODO: Variable declaration
            else:
                # Try to parse as assignment
                name = self.current_token.value
                self.eat(TokenType.TOKEN_ID)
                if self.current_token.type == TokenType.TOKEN_EQUALS:
                    self.eat(TokenType.TOKEN_EQUALS)
                    value = self.parse_expr()
                    return AssignmentExpr(name, value)
                else:
                    print(f"Unexpected identifier: {name}", file=sys.stderr)
                    sys.exit(1)
        elif self.current_token.type == TokenType.TOKEN_EOF:
            pass
        else:
            return self.parse_expr()
    
    def parse_while(self) -> Stmt:
        self.eat(TokenType.TOKEN_ID)  # Eat 'while'
        condition = self.parse_conditional_expr()
        self.eat(TokenType.TOKEN_LBRACE)
        body = []
        while self.current_token.type != TokenType.TOKEN_RBRACE:
            body.append(self.parse_stmt())
            if self.current_token.type == TokenType.TOKEN_SEMI:
                self.eat(TokenType.TOKEN_SEMI)
        self.eat(TokenType.TOKEN_RBRACE)
        return WhileStmt(condition, body)
    
    def parse_expr(self) -> Expr:
        return self.parse_additive_expr()
    
    def parse_additive_expr(self) -> Expr:
        left = self.parse_multiplicative_expr()
        while self.current_token.type in (TokenType.TOKEN_PLUS, TokenType.TOKEN_MINUS):
            operator = self.current_token.value
            self.advance()
            right = self.parse_multiplicative_expr()
            left = BinaryExpr(left, right, operator)
        return left
    
    def parse_multiplicative_expr(self) -> Expr:
        left = self.parse_primary_expr()
        while self.current_token.type in (TokenType.TOKEN_MULTIPLY, TokenType.TOKEN_DIVIDE):
            operator = self.current_token.value
            self.advance()
            right = self.parse_primary_expr()
            left = BinaryExpr(left, right, operator)
        return left
    
    def parse_primary_expr(self) -> Expr:
        if self.current_token.type == TokenType.TOKEN_ID:
            identifier = Identifier(self.current_token.value)
            self.advance()
            return identifier
        elif self.current_token.type == TokenType.TOKEN_NUMBER:
            numeric = NumericLiteral(float(self.current_token.value))
            self.advance()
            return numeric
        elif self.current_token.type == TokenType.TOKEN_LPAREN:
            self.eat(TokenType.TOKEN_LPAREN)
            expr = self.parse_expr()
            self.eat(TokenType.TOKEN_RPAREN)
            return expr
        else:
            print(f"Unexpected token in expression: {self.current_token}", file=sys.stderr)
            sys.exit(1)
    
    def parse_conditional_expr(self) -> Expr:
        self.eat(TokenType.TOKEN_LPAREN)
        left = self.parse_expr()
        
        if self.current_token.type in (TokenType.TOKEN_GREATER, TokenType.TOKEN_SMALLER, 
                                     TokenType.TOKEN_EQUALITY, TokenType.TOKEN_GREATER_EQUAL,
                                     TokenType.TOKEN_SMALLER_EQUAL):
            operator = self.current_token.value
            self.advance()
            right = self.parse_expr()
            cond_expr = ConditionalExpr(left, right, operator)
            self.eat(TokenType.TOKEN_RPAREN)
            return cond_expr
        else:
            print(f"Expected comparison operator, got {self.current_token}", file=sys.stderr)
            sys.exit(1)

def main():
    # Test program
    test_program = """
    while (x > 5) {
        y = y + 1;
    }
    """
    
    lexer = Lexer(test_program)
    parser = Parser(lexer)
    program = parser.produce_ast()
    
    print("=== Generated AST ===")
    print(program)

if __name__ == "__main__":
    main()