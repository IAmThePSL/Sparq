# evaluator.py: Evaluates the AST (interpreter logic)
class Evaluator:
    def __init__(self):
        self.variables = {}

    def evaluate(self, ast):
        for node in ast:
            if node["type"] == "VariableDeclaration":
                self.variables[node["name"]] = node["value"]
                print(f"Variable {node['name']} = {node['value']}")
            else:
                raise Exception(f"Unknown AST node type: {node['type']}")
