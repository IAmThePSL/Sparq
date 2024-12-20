# Abstract Syntax Tree definitions
class ASTNode:
    def __init__(self, node_type, **kwargs):
        self.node_type = node_type
        self.attributes = kwargs

    def __repr__(self):
        return f"ASTNode(type={self.node_type}, attributes={self.attributes})"

class VariableDeclarationNode(ASTNode):
    def __init__(self, name, value):
        super().__init__("VariableDeclaration", name=name, value=value)

class PrintNode(ASTNode):
    def __init__(self, value):
        super().__init__("Print", value=value)

class MathematicalOperatorNode(ASTNode):
    def __init__(self, value):
        super().__init__("", value=value)
