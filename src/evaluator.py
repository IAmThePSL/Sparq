# evaluator.py: Evaluates the AST (interpreter logic)
class EvaluatorError(Exception):
    """Base class for evaluator exceptions"""
    def __init__(self, message, node=None):
        self.message = message
        self.node = node
        super().__init__(self.message)

class UndefinedVariableError(EvaluatorError):
    """Raised when attempting to access an undefined variable"""
    def __init__(self, variable_name, node=None):
        super().__init__(f"Undefined variable: '{variable_name}'", node)
        self.variable_name = variable_name

class TypeConversionError(EvaluatorError):
    """Raised when unable to convert a value to the expected type"""
    def __init__(self, value, target_type, node=None):
        super().__init__(f"Cannot convert '{value}' to {target_type}", node)
        self.value = value
        self.target_type = target_type

class InvalidNodeTypeError(EvaluatorError):
    """Raised when encountering an unknown node type"""
    def __init__(self, node_type, node=None):
        super().__init__(f"Unknown node type: '{node_type}'", node)
        self.node_type = node_type

class OperatorError(EvaluatorError):
    """Raised when an operation cannot be performed"""
    def __init__(self, operator, left, right, node=None):
        super().__init__(
            f"Cannot perform operation '{operator}' between '{left}' and '{right}'",
            node
        )
        self.operator = operator
        self.left = left
        self.right = right

class DivisionByZeroError(EvaluatorError):
    """Raised when attempting to divide by zero"""
    def __init__(self, node=None):
        super().__init__("Division by zero", node)

class Evaluator:
    def __init__(self):
        self.variables = {}  # Store variable bindings
        self.operators = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide,
            '%': self.modulo,
            '**': self.power
        }

    def evaluate(self, ast):
        """Evaluates an AST or list of AST nodes."""
        try:
            if isinstance(ast, list):
                result = None
                for node in ast:
                    result = self.evaluate_node(node)
                return result
            elif hasattr(ast, 'type'):
                return self.evaluate_node(ast)
            else:
                raise TypeError("Expected AST node or list of nodes")
        except Exception as e:
            if isinstance(e, EvaluatorError):
                raise
            raise EvaluatorError(f"Evaluation error: {str(e)}")

    def convert_value(self, value, node=None):
        """Converts string values to appropriate types."""
        if not isinstance(value, str):
            return value

        try:
            if value.isdigit():
                return int(value)

            if value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                return float(value)

            if value.startswith('"') and value.endswith('"'):
                return value[1:-1]

            return value

        except ValueError as e:
            raise TypeConversionError(value, "number", node)

    def evaluate_node(self, node):
        """Evaluates a single AST node."""
        try:
            if node.type == "VariableDeclaration":
                name = node.attributes.get('name')
                if not name:
                    raise EvaluatorError("Variable declaration missing name", node)

                value = self.evaluate_expression(node.attributes.get('value'))
                if value is None:
                    raise EvaluatorError("Variable declaration missing value", node)

                self.variables[name] = value
                return value

            elif node.type == "PrintStatement":
                value = self.evaluate_expression(node.attributes.get('value'))
                if value is None:
                    raise EvaluatorError("Print statement missing value", node)

                print(value)
                return value

            elif node.type == "BinaryOperation":
                return self.evaluate_binary_operation(node)

            else:
                raise InvalidNodeTypeError(node.type, node)

        except KeyError as e:
            raise EvaluatorError(f"Missing required attribute: {str(e)}", node)
        except Exception as e:
            if isinstance(e, EvaluatorError):
                raise
            raise EvaluatorError(f"Error evaluating node: {str(e)}", node)

    def evaluate_expression(self, expr):
        """Evaluates an expression, which can be a literal value, variable, or operation."""
        if isinstance(expr, (int, float)):
            return expr
        elif isinstance(expr, str):
            # Check if it's a variable reference
            if expr in self.variables:
                return self.variables[expr]
            return self.convert_value(expr)
        elif hasattr(expr, 'type'):
            return self.evaluate_node(expr)
        else:
            raise EvaluatorError(f"Invalid expression type: {type(expr)}")

    def evaluate_binary_operation(self, node):
        """Evaluates a binary operation node."""
        left = self.evaluate_expression(node.attributes.get('left'))
        right = self.evaluate_expression(node.attributes.get('right'))
        operator = node.attributes.get('operator')

        if operator not in self.operators:
            raise OperatorError(operator, left, right, node)

        return self.operators[operator](left, right, node)

    # Arithmetic operations
    def add(self, left, right, node):
        """Handles addition and string concatenation."""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left + right
        elif isinstance(left, str) or isinstance(right, str):
            return str(left) + str(right)
        raise OperatorError('+', left, right, node)

    def subtract(self, left, right, node):
        """Handles subtraction."""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left - right
        raise OperatorError('-', left, right, node)

    def multiply(self, left, right, node):
        """Handles multiplication and string repetition."""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left * right
        elif isinstance(left, str) and isinstance(right, int):
            return left * right
        elif isinstance(left, int) and isinstance(right, str):
            return right * left
        raise OperatorError('*', left, right, node)

    def divide(self, left, right, node):
        """Handles division."""
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise OperatorError('/', left, right, node)
        if right == 0:
            raise DivisionByZeroError(node)
        return left / right

    def modulo(self, left, right, node):
        """Handles modulo operation."""
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise OperatorError('%', left, right, node)
        if right == 0:
            raise DivisionByZeroError(node)
        return left % right

    def power(self, left, right, node):
        """Handles exponentiation."""
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise OperatorError('**', left, right, node)
        try:
            return left ** right
        except OverflowError:
            raise EvaluatorError("Result too large", node)

    def get_variable(self, name):
        """Retrieves a variable's value from the environment."""
        if name not in self.variables:
            raise UndefinedVariableError(name)
        return self.variables[name]
