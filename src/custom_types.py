from enum import Enum, auto

class ValueType(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    ANY = auto()  # For type inference with 'let'

class Value:
    def __init__(self, type_, value, is_const=False):
        self.type = type_
        self.value = value
        self.is_const = is_const

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        const_str = "const " if self.is_const else ""
        return f"{const_str}{self.type.name}({self.value})"

def validate_type(value, expected_type):
    if expected_type == ValueType.INT:
        if not isinstance(value, int):
            raise TypeError(f"Expected integer, got {type(value).__name__}")
    elif expected_type == ValueType.FLOAT:
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected number, got {type(value).__name__}")
    elif expected_type == ValueType.STRING:
        if not isinstance(value, str):
            raise TypeError(f"Expected string, got {type(value).__name__}")
    elif expected_type == ValueType.BOOLEAN:
        if not isinstance(value, bool):
            raise TypeError(f"Expected boolean, got {type(value).__name__}")

def infer_type(value):
    if isinstance(value, bool):
        return ValueType.BOOLEAN
    elif isinstance(value, int):
        return ValueType.INT
    elif isinstance(value, float):
        return ValueType.FLOAT
    elif isinstance(value, str):
        return ValueType.STRING
    else:
        raise TypeError(f"Cannot infer type for {type(value).__name__}")
