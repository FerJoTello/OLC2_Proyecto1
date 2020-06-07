from enum import Enum


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
    GREATER =6

class Expression:
    '''original father class'''


class Terminal(Expression):
    ''''''


class Primitive(Terminal):
    '''contains a value and doesn't depend on other register'''

    def __init__(self, _type, value):
        self.type = _type
        self.value = value


class Register(Terminal):
    def __init__(self, _type, name):
        self.type = _type
        self.name = name


class Read(Terminal):
    ''''''

    def __init__(self):
        ''


class Array(Terminal):
    ''''''

    def __init__(self):
        ''


class Conversion(Terminal):
    def __init__(self, _type, reg):
        self.type = _type
        self.reg = reg


class ArrayRegister(Terminal):
    def __init__(self, reg, index_list):
        self.reg = reg
        self.index_list = index_list


class UnitExpression(Expression):
    '''contains only one operand for a expression'''

    def __init__(self, operation, operand):
        self.operation = operation
        self.operand = operand


class BinaryExpression(Expression):
    '''contains two operands for a expression'''

    def __init__(self, operation, op1, op2):
        self.operation = operation
        self.op1 = op1
        self.op2 = op2


# class
