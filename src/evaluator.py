# evaluator.py: Evaluates the AST (interpreter logic)

### GITHUB: I know this is not a working code. So, sorry in advance for not getting this stupid code to work.
### GITHUB: I really am trying my best but I just can't seem to get it working. This is just an update for Github. 
### GITHUB: Have a nice day!

# TODOS:
    # fix Error: Unknown type: ValueType.STRING
    # =============================================================================
    # In "convert_value", I or we handle string literals with:
        # elif raw_value.startswith('"') and raw_value.endswith('"'):
            # value = raw_value[1:-1]
    # make it use a proper string parser or escape sequence handler for robust string processing.
    # =============================================================================
    # fix the error that gives me "Invalid type specification: ValueType.xxxx":
    #  make it stop being a bitchy complainer:
    # sparq> let message = "Welcome";
    # AST: ['VariableDeclaration(name=message, value="Welcome")']
    # => Welcome
    #
    # sparq> string name = 'DaPSL';
    # Error: Unknown statement: ('IDENTIFIER', 'string')
    #
    # sparq> str name = "DaPSL";
    # AST: ['VariableDeclaration(name=name, value="DaPSL")']
    # Error: Invalid type specification: ValueType.STRING
    # =============================================================================


from enum import Enum

class ValueType(Enum):
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    BOOL = "boolean"

    @classmethod
    def from_str(cls, type_str):
        """Convert string type name to ValueType enum"""
        type_map = {
            "int": cls.INT,
            "float": cls.FLOAT,
            "str": cls.STRING,
            "string": cls.STRING,
            "bool": cls.BOOL,
            "boolean": cls.BOOL
        }
        if type_str is None:
            return None
        return type_map.get(str(type_str).lower())

class Value:
    """Represents a typed value in our language"""
    def __init__(self, type_name, value, is_const=False):
        self.type = type_name
        self.value = value
        self.is_const = is_const

    def __str__(self):
        return str(self.value)

def validate_type(value, expected_type):
    """Validates that a value matches the expected type."""
    # Convert string or ValueType to string representation
    if isinstance(expected_type, ValueType):
        expected_type = expected_type.value
    elif isinstance(expected_type, str):
        type_enum = ValueType.from_str(expected_type)
        if type_enum is None:
            raise TypeSystemError(f"Unknown type: {expected_type}")
        expected_type = type_enum.value

    type_validators = {
        "int": lambda v: isinstance(v, int),
        "float": lambda v: isinstance(v, (int, float)),  # Allow int->float conversion
        "string": lambda v: isinstance(v, str),
        "bool": lambda v: isinstance(v, bool)
    }

    validator = type_validators.get(expected_type)
    if not validator:
        raise TypeSystemError(f"Unknown type: {expected_type}")

    if not validator(value):
        raise TypeSystemError(f"Expected {expected_type}, got {type(value).__name__}")

def infer_type(value):
    """Infers the type of a value.

    Returns:
        ValueType: The inferred type as a ValueType enum
    """
    if isinstance(value, bool):
        return ValueType.BOOL
    elif isinstance(value, int):
        return ValueType.INT
    elif isinstance(value, float):
        return ValueType.FLOAT
    elif isinstance(value, str):
        return ValueType.STRING
    else:
        raise TypeSystemError(f"Cannot infer type for value: {value}")

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

class TypeSystemError(EvaluatorError):
    """Raised when there's a type-related error"""
    pass

class ConstantReassignmentError(EvaluatorError):
    """Raised when trying to modify a constant"""
    def __init__(self, variable_name, node=None):
        super().__init__(f"Cannot reassign constant variable '{variable_name}'", node)

class Evaluator:

    def __init__(self):
        self.variables = {}
        self.operators = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide,
            '%': self.modulo,
            '**': self.power
        }

    def resolve_variable_type(self, raw_value, declared_type):
        """Resolves the variable type based on declaration or inference."""
        if declared_type is None:
            return infer_type(raw_value)

        # if it's a already a ValueType enum, return it
        if isinstance(declared_type, ValueType):
            return declared_type

        # if it's a string, convert it to ValueType enum
        if isinstance(declared_type, str):
            value_type = ValueType.from_str(declared_type)
            if value_type is None:
                raise TypeSystemError(f"Unknown type: {declared_type}")
            return value_type

        raise TypeSystemError(f"Invalid type: {declared_type}")

    def convert_value(self, raw_value, expected_type=None, node=None):
        """Converts and validates a value according to the expected type."""
        try:
            # Handle Value objects
            if isinstance(raw_value, Value):
                value = raw_value.value
            # Handle string literals
            elif isinstance(raw_value, str):
                if raw_value.lower() == "true":
                    value = True
                elif raw_value.lower() == "false":
                    value = False
                # Improved string literal handling
                elif (raw_value.startswith('"') and raw_value.endswith('"')) or \
                     (raw_value.startswith("'") and raw_value.endswith("'")):
                    value = raw_value[1:-1]  # Strip quotes
                elif raw_value.isdigit():
                    value = int(raw_value)
                elif raw_value.replace('.', '', 1).isdigit() and raw_value.count('.') == 1:
                    value = float(raw_value)
                else:
                    value = raw_value
            else:
                value = raw_value

            # If expected type is STRING, ensure the value is a string
            if expected_type in ["string", ValueType.STRING]:
                value = str(value)

            # Validate type if specified
            if expected_type:
                if isinstance(expected_type, ValueType):
                    expected_type = expected_type.value
                validate_type(value, expected_type)
            return value

        except ValueError as e:
            raise TypeConversionError(raw_value, expected_type or "unknown", node)
        except TypeError as e:
            raise TypeSystemError(str(e), node)

    def evaluate(self, ast):
        """Evaluates an AST or list of AST nodes."""
        try:
            visited = set()  # Create a set to track visited nodes
            if isinstance(ast, list):
                result = None
                for node in ast:
                    if node in visited:  # Check if the node has already been visited
                        # Skip the node if it has already been visited
                        continue  # Skip this node, as it has already been visited
                    visited.add(node)  # Add the node to the visited set
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

    def evaluate_expression(self, expr):
            """Evaluates an expression, which can be a literal value, variable, or operation."""
            if isinstance(expr, (int, float, bool)):
                return expr
            elif isinstance(expr, str):
                # Check if it's a variable reference
                if expr in self.variables:
                    return self.variables[expr].value
                return self.convert_value(expr)
            elif hasattr(expr, 'type'):
                return self.evaluate_node(expr)
            else:
                raise EvaluatorError(f"Invalid expression type: {type(expr)}")

    def evaluate_node(self, node):
        """Routes node evaluation to appropriate handler based on node type."""
        try:
            handlers = {
                "VariableDeclaration": self._evaluate_variable_declaration,
                "PrintStatement": self._evaluate_print_statement,
                "BinaryOperation": self._evaluate_binary_operation,
                "Identifier": self._evaluate_identifier
            }

            handler = handlers.get(node.type)
            if handler is None:
                raise InvalidNodeTypeError(node.type, node)

            return handler(node)

        except Exception as e:
            if isinstance(e, EvaluatorError):
                raise
            raise EvaluatorError(f"Error evaluating node: {str(e)}", node)

    def _evaluate_variable_declaration(self, node):
        """Handles variable declaration nodes."""
        name = node.attributes.get('name')
        if not name:
            raise EvaluatorError("Variable declaration missing name", node)

        raw_value = self.evaluate_expression(node.attributes.get('value'))
        type_enum = self._resolve_variable_type(raw_value, node.attributes.get('var_type'))
        is_const = node.attributes.get('is_const', False)

        self._check_constant_reassignment(name, node)
        value = self.convert_value(raw_value, type_enum.value, node)
        self.variables[name] = Value(type_enum.value, value, is_const)

        return value

    def _resolve_variable_type(self, raw_value, declared_type):
        """Resolves the variable type based on declaration or inference."""
        # Handle no type declaration (inference)
        if declared_type is None:
            return infer_type(raw_value)

        # Convert string type to ValueType enum
        if isinstance(declared_type, (str, ValueType)):
            type_enum = ValueType.from_str(declared_type) if isinstance(declared_type, str) else declared_type
            if type_enum is None:
                raise TypeSystemError(f"Unknown type: {declared_type}")
                return type_enum

        raise TypeSystemError(f"Invalid type specification: {declared_type}")


    def _check_constant_reassignment(self, name, node):
        """Checks if we're trying to reassign a constant."""
        if name in self.variables and self.variables[name].is_const:
            raise ConstantReassignmentError(name, node)

    def _evaluate_print_statement(self, node):
        """Handles print statement nodes."""
        value = self.evaluate_expression(node.attributes.get('value'))
        if value is None:
            raise EvaluatorError("Print statement missing value", node)

        output_value = value.value if isinstance(value, Value) else value
        print(output_value)
        return output_value

    def _evaluate_binary_operation(self, node):
        """Handles binary operation nodes."""
        return self.evaluate_binary_operation(node)

    def _evaluate_identifier(self, node):
        """Handles identifier nodes."""
        name = node.attributes.get('name')
        if not name:
            raise EvaluatorError("Identifier missing name", node)
        return self.get_variable(name).value

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
        if right == 0 or (isinstance(right, float) and right == 0.0):
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
