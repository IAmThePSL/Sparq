import re
import sys

# Define token types
TOKEN_TYPES = [
    # Comments should be checked before other tokens to ensure proper handling
    ("COMMENT_BLOCK", r"/\*[\s\S]*?\*/"),  # Multi-line comments
    ("COMMENT_SINGLE", r"//.*?(?:\n|$)"),  # Single-line comments (updated pattern)
    ("KEYWORD", r"\b(let|const|int|str|bool)\b"),  # Keywords
    ("IDENTIFIER", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),  # Identifiers
    ("NUMBER", r"\b\d+\.\d+|\b\d+\b"),  # Integers and floating-point numbers
    ("STRING", r'"([^"\\]|\\.)*"'),  # String literals with escape sequences
    ("ASSIGN", r"="),  # Assignment operator
    ("OPERATOR", r"[+\-*/]"),  # Arithmetic operators
    ("SEMICOLON", r";"),  # Statement terminator
    ("LPAREN", r"\("),  # Left parenthesis
    ("RPAREN", r"\)"),  # Right parenthesis
    ("LBRACE", r"{"),  # Left brace
    ("RBRACE", r"}"),  # Right brace
    ("WHITESPACE", r"\s+"),  # Whitespace (to be ignored)
    ("UNKNOWN", r"."),  # Catch-all for unknown characters
]

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []
        # Pre-compile all regular expressions for better performance
        self.token_patterns = [(token_type, re.compile(pattern)) for token_type, pattern in TOKEN_TYPES]

    def advance(self, length=1):
        """Advance the position by the given length."""
        self.position += length

    def tokenize(self):
        while self.position < len(self.code):
            match = None
            for token_type, regex in self.token_patterns:
                match = regex.match(self.code, self.position)
                if match:
                    matched_text = match.group(0)
                    matched_length = len(matched_text)

                    # Skip comments and whitespace
                    if token_type in ["WHITESPACE", "COMMENT_SINGLE", "COMMENT_BLOCK"]:
                        self.advance(matched_length)
                        break
                    else:
                        self.tokens.append((token_type, matched_text))
                        self.advance(matched_length)
                    break

            if not match:
                # Provide more context in the error message
                context = self.code[max(0, self.position-10):min(len(self.code), self.position+10)]
                raise Exception(f"Illegal character at position {self.position}. Context: '...{context}...'")

        return self.tokens

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise Exception(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def main(file_path):
    try:
        # Read the file content
        code = read_file(file_path)

        # Initialize the lexer with the file content
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # Output the tokens in a more readable format
        for token_type, value in tokens:
            print(f"{token_type}: {value}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 lexer.py <filename>")
    else:
        file_path = sys.argv[1]
        main(file_path)
