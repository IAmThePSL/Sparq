# evaluator.py: Evaluates the AST (interpreter logic)
class Evaluator:
    def __init__(self):
        self.variables = {}  # store variables

    def evaluate(self, ast):
        if ast[0] == "PRINT":
            expr = ast[1]
            if expr[0] == "IDENTIFIER":
                value = self.variables.get(expr[1], None)
                if value is None:
                    raise Exception(f"Undefined variable: {expr[1]}")
                print(value)
            elif expr[0] in ["NUMBER", "STRING"]:
                print(expr[1])
            else:
                raise Exception("Unsupported print argument")
        else:
            raise Exception(f"Unknown AST node: {ast}")
