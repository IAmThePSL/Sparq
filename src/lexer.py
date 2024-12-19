# lexer.py: Tokenizes the input code
import re
import sys

# Define token types
TOKEN_TYPES = [
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
    ("COMMENT_SINGLE", r"//.*"),  # Single-line comments
    ("COMMENT_BLOCK", r"/\*[\s\S]*?\*/"),  # Multi-line comments
    ("UNKNOWN", r"."),  # Catch-all for unknown characters
]

# Lexer class
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []

    def advance(self):
        """Advance to the next token without adding anything to the token list."""
        self.position += 1

    def tokenize(self):
        while self.position < len(self.code):
            match = None
            for token_type, pattern in TOKEN_TYPES:
                regex = re.compile(pattern)
                match = regex.match(self.code, self.position)
                if match:
                    if token_type in ["WHITESPACE", "COMMENT_SINGLE", "COMMENT_BLOCK"]:
                        # Skip comments and whitespace
                        self.advance()
                    else:
                        self.tokens.append((token_type, match.group(0)))
                    self.position = match.end()
                    break
            if not match:
                raise Exception(f"Illegal character at position {self.position}")
        return self.tokens

# Function to read file contents
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Main function to process the file and tokenize
def main(file_path):
    code = ""
    try:
        # Read the file content
        code = read_file(file_path)
        # Initialize the lexer with the file content
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # Output the tokens
        print(tokens)
    except Exception as e:
        print(f"Error: {e}")
        if code == "":
            print(f"Failed to read the file: {file_path}")
        else:
            print("Tokenization failed.")

# Entry point
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 lexer.py <filename>")
    else:
        file_path = sys.argv[1]
        main(file_path)
