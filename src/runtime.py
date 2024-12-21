# Runtime environment and built-in functions
class Runtime:
    def __init__(self):
        self.variables = {}  # Dictionary to store variable names and values

    def execute(self, ast):
        for node in ast:
            if node.node_type == "VariableDeclaration":
                self.variables[node.attributes["name"]] = node.attributes["value"]
                print(f"Variable {node.attributes['name']} = {node.attributes['value']}")
            elif node.node_type == "Print":
                value = self.evaluate(node.attributes["value"])
                print(value)
            else:
                raise Exception(f"Unknown AST node type: {node.node_type}")

    def evaluate(self, expression):
        # For now, just return the value directly
        # Expand later to handle expressions, variables, etc.
        if isinstance(expression, str) and expression in self.variables:
            return self.variables[expression]
        return expression
