# lexer.py
import re

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []

        self.token_patterns = [
            ("COMMENT_BLOCK", r"/\*[\s\S]*?\*/"),
            ("COMMENT_SINGLE", r"//.*?(?:\n|$)"),
            ("KEYWORD", r"\b(let|const|int|str|bool)\b"),
            ("BOOLEAN", r"\b(true|false)\b"),
            ("IDENTIFIER", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
            ("NUMBER", r"\b\d+\.\d+|\b\d+\b"),
            ("STRING", r'"([^"\\]|\\.)*"'),
            ("ASSIGN", r"="),
            ("OPERATOR", r"[+\-*/]"),
            ("SEMICOLON", r";"),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("LBRACE", r"{"),
            ("RBRACE", r"}"),
            ("WHITESPACE", r"\s+"),
            ("UNKNOWN", r".")
        ]

        # Pre-compile all regular expressions
        self.token_patterns = [(name, re.compile(pattern)) for name, pattern in self.token_patterns]

    def advance(self, length=1):
        self.position += length

    def tokenize(self):
        while self.position < len(self.code):
            match = None
            for token_type, regex in self.token_patterns:
                match = regex.match(self.code, self.position)
                if match:
                    if token_type in ["WHITESPACE", "COMMENT_SINGLE", "COMMENT_BLOCK"]:
                        self.advance(match.end() - self.position)
                    else:
                        self.tokens.append((token_type, match.group(0)))
                        self.advance(match.end() - self.position)
                    break

            if not match:
                raise Exception(f"Illegal character at position {self.position}")

        return self.tokens
