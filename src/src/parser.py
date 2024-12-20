# parser.py: Parses tokens into an AST
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        ast = []
        while self.position < len(self.tokens):
            stmt = self.parse_statement()
            if stmt:
                ast.append(stmt)
        return ast

    def parse_statement(self):
        token_type, value = self.peek()
        if token_type == "KEYWORD" and value == "let":
            return self.parse_variable_declaration()
        else:
            raise Exception(f"Unknown statement: {self.peek()}")

    def parse_variable_declaration(self):
        # Consume 'let'
        self.consume("KEYWORD", "let")

        # Get variable name
        token_type, name = self.consume("IDENTIFIER")
        # Ensure '=' follows
        self.consume("ASSIGN", "=")

        # Get the value
        token_type, value = self.consume("NUMBER")

        # Ensure the line ends with a semicolon
        self.consume("SEMICOLON", ";")

        return {"type": "VariableDeclaration", "name": name, "value": int(value)}

    def peek(self):
        return self.tokens[self.position]

    def consume(self, expected_type, expected_value=None):
        token = self.tokens[self.position]
        if token[0] != expected_type or (expected_value and token[1] != expected_value):
            raise Exception(f"Expected {expected_type} {expected_value}, got {token}")
        self.position += 1
        return token
