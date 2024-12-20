# parser.py: Parses tokens into an AST
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def advance(self):
        self.position += 1

    def parse_print(self):
        """Parse a print statement like `print(x)`."""
        if self.current_token() == ("IDENTIFIER", "print"):
            self.advance()  # Skip `print`
            if self.current_token() == ("LPAREN", "("):
                self.advance()  # Skip `(`
                expr = self.parse_expression()  # Parse the expression inside
                if self.current_token() == ("RPAREN", ")"):
                    self.advance()  # Skip `)`
                    return ("PRINT", expr)
        raise Exception("Syntax error in print statement")

    def parse_expression(self):
        """Parse a basic expression (e.g., variable, number)."""
        token = self.current_token()
        if token and token[0] in ["IDENTIFIER", "NUMBER", "STRING"]:
            self.advance()
            return token
        raise Exception("Invalid expression")

    def parse(self):
        """Parse the tokens into an AST."""
        token = self.current_token()
        if token and token[0] == "IDENTIFIER" and token[1] == "print":
            return self.parse_print()
        else:
            raise Exception(f"Unknown statement: {token}")
