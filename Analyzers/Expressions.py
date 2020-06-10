from enum import Enum


class TYPE(Enum):
    INTEGER = 1
    DECIMAL = 2
    STRING = 3
    CHARACTER = 4


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


class BinaryExpression(Expression):
    '''contains two operands for a expression'''

    def __init__(self, node_index, operation, op1, op2):
        self.node_index = node_index
        self.operation = operation
        self.op1 = op1
        self.op2 = op2


class Terminal(Expression):
    ''''''


class Primitive(Terminal):
    '''contains a value and doesn't depend on other register'''

    def __init__(self, node_index, _type, value):
        self.node_index = node_index
        self.type = _type
        self.value = value


class Register(Terminal):
    def __init__(self, node_index, _type, name):
        self.node_index = node_index
        self.type = _type
        self.name = name


class Read(Terminal):
    ''''''

    def __init__(self, node_index):
        self.node_index = node_index


class Array(Terminal):
    ''''''

    def __init__(self, node_index):
        self.node_index = node_index


class Conversion(Terminal):
    def __init__(self, node_index, _type, reg):
        self.node_index = node_index
        self.type = _type
        self.reg = reg


class ArrayRegister(Terminal):
    def __init__(self, node_index, reg, index_list):
        self.node_index = node_index
        self.reg = reg
        self.index_list = index_list


# class
