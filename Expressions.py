from enum import Enum


class REG_TYPE(Enum):
    TEMPORAL = 1
    PARAMETER = 2
    RETURN_VALUE = 3
    RETURN_LEVEL = 4
    STACK_VALUE = 5
    STACK_POINTER = 6
    FUNCTION = 7
    PROCEDURE = 8
    CONTROL = 9
    MAIN = 10


class TYPE(Enum):
    INTEGER = 1
    DECIMAL = 2
    STRING = 3
    CHARACTER = 4
    ARRAY = 5


class UNIT_OPERATION(Enum):
    NEGATIVE = 1
    POINTER = 2
    ABSOLUTE = 3


class ARITHMETIC_OPERATION(Enum):
    SUM = 1
    SUBSTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4
    MODULE = 5


class LOGIC_OPERATION(Enum):
    NOT = 1
    OR = 2
    AND = 3
    XOR = 4


class BIT_OPERATION(Enum):
    NOT = 1
    AND = 2
    OR = 3
    XOR = 4
    L_SHIFT = 5
    R_SHIFT = 6


class RELATIONAL_OPERATION(Enum):
    COMPARISSON = 1
    DISTINCT = 2
    LESS_EQUAL = 3
    GREATER_EQUAL = 4
    LESS = 5
    GREATER = 6


class Expression:
    '''original father class'''


class UnitExpression(Expression):
    '''contains only one operand for a expression'''

    def __init__(self, node_index, operation, operand):
        self.node_index = node_index
        self.operation = operation
        self.operand = operand
        self.lineno = 0


class BinaryExpression(Expression):
    '''contains two operands for a expression'''

    def __init__(self, node_index, operation, op1, op2):
        self.node_index = node_index
        self.operation = operation
        self.op1 = op1
        self.op2 = op2
        self.lineno = 0


class Terminal(Expression):
    ''''''


class Primitive(Terminal):
    '''contains a value and doesn't depend on other register'''

    def __init__(self, node_index, _type, value):
        self.node_index = node_index
        self.type = _type
        self.value = value
        self.lineno = 0


class Register(Terminal):
    def __init__(self, node_index, _type, name):
        self.node_index = node_index
        self.type = self.set_type(_type)
        self.name = name
        self.lineno = 0

    def set_type(self, _type):
        types = {
            'V_TEMP': REG_TYPE.TEMPORAL,
            'V_PARAM': REG_TYPE.PARAMETER,
            'V_RETURNED': REG_TYPE.RETURN_VALUE,
            'V_RETURN_LVL': REG_TYPE.RETURN_LEVEL,
            'V_STACK': REG_TYPE.STACK_VALUE,
            'V_STACK_POINTER': REG_TYPE.STACK_POINTER
        }
        return types.get(_type)


class Read(Terminal):
    def __init__(self, node_index):
        self.node_index = node_index
        self.lineno = 0


class Array(Terminal):
    def __init__(self, node_index):
        self.node_index = node_index
        self.lineno = 0


class Conversion(Terminal):
    def __init__(self, node_index, _type, reg):
        self.node_index = node_index
        self.type = _type
        self.reg = reg
        self.lineno = 0


class ArrayRegister(Terminal):
    def __init__(self, node_index, reg, index_list):
        self.node_index = node_index
        self.reg = reg
        self.index_list = index_list
        self.lineno = 0


# class
