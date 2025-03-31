import re

TOKEN_INT = "INT"
TOKEN_FLOAT = "FLOAT"
TOKEN_ID = "ID"
TOKEN_INT_DECLAR = "INT_DECLAR"
TOKEN_FLOAT_DECLAR = "FLOAT_DECLAR"
TOKEN_WHILE = "WHILE"
TOKEN_IF = "IF"
TOKEN_ELSE = "ELSE"
TOKEN_ENDWHILE = "ENDWHILE"
TOKEN_ENDIF = "ENDIF"
TOKEN_PRINT = "PRINT"
TOKEN_COS = "COS"
TOKEN_SIN = "SIN"
TOKEN_EQUAL = "EQUAL"
TOKEN_EQUALITY = "EQUALITY"
TOKEN_LESS = "LESS"
TOKEN_LESS_EQUAL = "LESS_EQUAL"
TOKEN_GREATER = "GREATER"
TOKEN_GREATER_EQUAL = "GREATER_EQUAL"
TOKEN_NOT_EQUAL = "NOT_EQUAL"
TOKEN_SEMI = "SEMI"
TOKEN_LPAREN = "LPAREN"
TOKEN_RPAREN = "RPAREN"
TOKEN_SUM = "SUM"
TOKEN_DIF = "DIF"
TOKEN_MULT = "MULT"
TOKEN_DIV = "DIV"
TOKEN_EOF = "EOF"

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ""
        dot_count = 0
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == "."):
            if self.current_char == ".":
                if dot_count > 0:
                    raise Exception("Too many decimal points in number")
                dot_count += 1
            result += self.current_char
            self.advance()
        return Token(TOKEN_FLOAT if dot_count == 1 else TOKEN_INT, result)

    def identifier(self):
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            result += self.current_char
            self.advance()
        keywords = {
            "int": TOKEN_INT_DECLAR,
            "float": TOKEN_FLOAT_DECLAR,
            "while": TOKEN_WHILE,
            "if": TOKEN_IF,
            "else": TOKEN_ELSE,
            "endwhile": TOKEN_ENDWHILE,
            "endif": TOKEN_ENDIF,
            "print": TOKEN_PRINT,
            "cos": TOKEN_COS,
            "sin": TOKEN_SIN,
        }
        return Token(keywords.get(result, TOKEN_ID), result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit() or self.current_char == ".":
                return self.number()
            if self.current_char.isalnum():
                return self.identifier()
            if self.current_char == "=":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(TOKEN_EQUALITY, "==")
                return Token(TOKEN_EQUAL, "=")
            if self.current_char == "<":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(TOKEN_LESS_EQUAL, "<=")
                return Token(TOKEN_LESS, "<")
            if self.current_char == ">":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(TOKEN_GREATER_EQUAL, ">=")
                return Token(TOKEN_GREATER, ">")
            if self.current_char == "!":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(TOKEN_NOT_EQUAL, "!=")
                raise Exception("Undefined token '!' found")
            token_map = {
                ";": TOKEN_SEMI,
                "(": TOKEN_LPAREN,
                ")": TOKEN_RPAREN,
                "+": TOKEN_SUM,
                "-": TOKEN_DIF,
                "*": TOKEN_MULT,
                "/": TOKEN_DIV,
            }
            if self.current_char in token_map:
                token_type = token_map[self.current_char]
                char = self.current_char
                self.advance()
                return Token(token_type, char)
            raise Exception(f"Illegal character {self.current_char}")
        return Token(TOKEN_EOF, None)

if __name__ == "__main__":
    text = "int x = 10; while (x > 0) x = x - 1; endwhile; float a = cos(3.14); print(a)"
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.type != TOKEN_EOF:
        print(token)
        token = lexer.get_next_token()
