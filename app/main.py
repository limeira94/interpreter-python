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


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int

    def __str__(self):
        return f"{self.type.name} {self.lexeme} {self.literal if self.literal is not None else 'null'}"


class Scanner:
    _SINGLE_CHAR_TOKENS = {
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
        "{": TokenType.LEFT_BRACE,
        "}": TokenType.RIGHT_BRACE,
        ",": TokenType.COMMA,
        ".": TokenType.DOT,
        "-": TokenType.MINUS,
        "+": TokenType.PLUS,
        ";": TokenType.SEMICOLON,
        "*": TokenType.STAR,
        "==": TokenType.EQUAL_EQUAL,
        "=": TokenType.EQUAL,
    }

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
                if self._math("="):
                    self._add_token(TokenType.BANG_EQUAL)
                else:
                    self._add_token(TokenType.BANG)
            case "=":
                if self._math("="):
                    self._add_token(TokenType.EQUAL_EQUAL)
                else:
                    self._add_token(TokenType.EQUAL)
            case _:
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

    def _math(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True


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
