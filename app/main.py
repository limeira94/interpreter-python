import sys
from enum import Enum, auto
from dataclasses import dataclass
from typing import List


class TokenType(Enum):
    # Single-character token
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL_EQUAL = auto()
    EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int

    def __repr__(self):
        return f"{self.type.name} {self.lexeme} {self.literal if self.literal is not None else 'null'}"


class Scanner:
    def __init__(self, source: str):
        self.source = source  # "(()))++--**"
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.had_error = False

    def scan_tokens(self) -> List[Token]:
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def _scan_token(self):
        char = self._advance()
        match char:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "!":
                if self._match("="):
                    self._add_token(TokenType.BANG_EQUAL)
                else:
                    self._add_token(TokenType.BANG)
            case "<":
                if self._match("="):
                    self._add_token(TokenType.LESS_EQUAL)
                else:
                    self._add_token(TokenType.LESS)
            case ">":
                if self._match("="):
                    self._add_token(TokenType.GREATER_EQUAL)
                else:
                    self._add_token(TokenType.GREATER)
            case "=":
                if self._match("="):
                    self._add_token(TokenType.EQUAL_EQUAL)
                else:
                    self._add_token(TokenType.EQUAL)
            case "/":
                if self._match("/"):
                    while self._peek() != "\n" and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case "\n":
                self.line += 1
                pass
            case '"':
                self._string()
                pass
            case "o":
                if self._match("r"):
                    self._add_token(TokenType.OR)
                pass
            case _:
                if self._is_digit(char):
                    self._number()
                elif self._is_alpha(char):
                    self._identifier()
                else:
                    print(
                        f"[line {self.line}] Error: Unexpected character: {char}",
                        file=sys.stderr,
                    )
                    self.had_error = True

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _add_token(self, type: TokenType, literal: object = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def _peek(self):
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek == "\n":
                self.line += 1
            self._advance()

        if self._is_at_end():
            print(
                f"[line {self.line}] Error: Unterminated string.",
                file=sys.stderr,
            )
            self.had_error = True
            return

        self._advance()

        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, value)

    def _is_digit(self, c):
        return c >= "0" and c <= "9"

    def _peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _number(self):
        while self._is_digit(self._peek()):
            self._advance()

        if self._peek() == "." and self._is_digit(self._peek_next()):
            self._advance()
            while self._is_digit(self._peek()):
                self._advance()

        self._add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def _identifier(self):
        while self._is_alpha_numeric(self._peek()):
            self._advance()
        text = self.source[self.start : self.current]
        token_type = KEYWORDS.get(text)
        if token_type is None:
            token_type = TokenType.IDENTIFIER

        self._add_token(token_type)

    def _is_alpha(self, c: str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    def _is_alpha_numeric(self, c: str) -> bool:
        return self._is_alpha(c) or self._is_digit(c)


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    scanner = Scanner(file_contents)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)

    if scanner.had_error:
        sys.exit(65)


if __name__ == "__main__":
    main()
