# parser.py: Parses tokens into an AST

### GITHUB: I know this is not working code. So, sorry in advance for not getting this stupid code to work.
### GITHUB: I really am trying my best but I just can't seem to get it working. This is just an update for Github. 
### GITHUB: Have a nice day!

from custom_ast import ASTNode, VariableDeclarationNode, PrintNode, BinaryOperationNode
from custom_types import ValueType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def peek_token(self):
        if self.position + 1 < len(self.tokens):
            return self.tokens[self.position + 1]
        return None

    def advance(self):
        self.position += 1

    def match(self, expected_type):
        token = self.current_token()
        if token and token[0] == expected_type:
            self.advance()
            return token
        raise Exception(f"Expected {expected_type}, found {token}")

    def parse(self):
        ast = []
        while self.current_token():
            ast.append(self.parse_statement())
        return ast

    def parse_statement(self):
        token = self.current_token()
        if not token:
            raise Exception("Unexpected end of input")

        if token[0] == "KEYWORD":
            if token[1] in ["let", "const", "int", "str", "bool"]:
                return self.parse_variable_declaration()
        elif token[0] == "IDENTIFIER" and token[1] == "print":
            return self.parse_print_statement()
        else:
            raise Exception(f"Unknown statement: {token}")

    def parse_variable_declaration(self):
        token = self.current_token()
        is_const = token[1] == "const"
        var_type = None

        if token[1] in ["int", "str", "string", "bool"]:
            var_type = {
                "int": ValueType.INT,
                "str": ValueType.STRING,
                "string": ValueType.STRING,
                "bool": ValueType.BOOLEAN
            }[token[1]]

        self.advance()  # Move past type/let/const
        name_token = self.match("IDENTIFIER")  # Variable name
        self.match("ASSIGN")  # `=`
        value = self.parse_expression()  # Right-hand side
        self.match("SEMICOLON")  # `;`

        return VariableDeclarationNode(
            name=name_token[1],
            value=value,
            var_type=var_type,
            is_const=is_const
        )

    def parse_print_statement(self):
        self.match("IDENTIFIER")  # `print`
        self.match("LPAREN")  # `(`
        value = self.parse_expression()
        self.match("RPAREN")  # `)`
        self.match("SEMICOLON")  # `;`
        return PrintNode(value)

    def parse_expression(self):
        return self.parse_additive_expression()

    def parse_additive_expression(self):
        left = self.parse_multiplicative_expression()

        while self.current_token() and self.current_token()[0] == "OPERATOR":
            operator = self.current_token()[1]
            if operator not in ['+', '-']:
                break
            self.advance()
            right = self.parse_multiplicative_expression()
            left = BinaryOperationNode(operator, left, right)

        return left

    def parse_multiplicative_expression(self):
        left = self.parse_primary()

        while self.current_token() and self.current_token()[0] == "OPERATOR":
            operator = self.current_token()[1]
            if operator not in ['*', '/', '%']:
                break
            self.advance()
            right = self.parse_primary()
            left = BinaryOperationNode(operator, left, right)

        return left

    def parse_primary(self):
        token = self.current_token()
        if not token:
            raise Exception("Unexpected end of expression")

        if token[0] in ["NUMBER", "STRING", "BOOLEAN"]:
            self.advance()
            return token[1]
        elif token[0] == "IDENTIFIER":
            self.advance()
            return token[1]
        elif token[0] == "LPAREN":
            self.advance()
            expr = self.parse_expression()
            self.match("RPAREN")
            return expr
        else:
            raise Exception(f"Unexpected token in expression: {token}")
