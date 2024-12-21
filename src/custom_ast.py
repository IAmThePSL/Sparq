# custom_ast.py
class ASTNode:
    def __init__(self, node_type, **kwargs):
        self.type = node_type
        self.attributes = kwargs

    def __repr__(self):
        return f"{self.type}({self.attributes})"

class BinaryOperationNode(ASTNode):
    def __init__(self, operator, left, right):
        super().__init__("BinaryOperation", operator=operator, left=left, right=right)

    def __repr__(self):
        return f"BinaryOperation(operator='{self.attributes['operator']}', left={self.attributes['left']}, right={self.attributes['right']})"

class VariableDeclarationNode(ASTNode):
    def __init__(self, name, value, var_type=None, is_const=False):
        super().__init__("VariableDeclaration",
                        name=name,
                        value=value,
                        var_type=var_type,
                        is_const=is_const)

    def __repr__(self):
        return f"VariableDeclaration(name={self.attributes['name']}, value={self.attributes['value']})"

class PrintNode(ASTNode):
    def __init__(self, value):
        super().__init__("PrintStatement", value=value)

    def __repr__(self):
        return f"PrintStatement(value={self.attributes['value']})"
