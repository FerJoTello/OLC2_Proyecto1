class Instruction:
    '''original father class'''

class InstructionsList:
    def __init__(self, node_index, instructions_list):
        self.node_index = node_index
        self.instructions_list = instructions_list

class Assignation(Instruction):
    def __init__(self, node_index, reg, expr):
        self.node_index = node_index
        self.reg = reg
        self.expr = expr


class GoTo(Instruction):
    def __init__(self, node_index, label):
        self.node_index = node_index
        self.label = label


class Print(Instruction):
    def __init__(self, node_index, content):
        self.node_index = node_index
        self.content = content


class Exit(Instruction):
    def __init__(self, node_index):
        '''exit class'''
        self.node_index = node_index


class Unset(Instruction):
    def __init__(self, node_index, reg):
        self.node_index = node_index
        self.reg = reg


class If(Instruction):
    def __init__(self, node_index, expr, goto):
        self.node_index = node_index
        self.expr = expr
        self.goto = goto


class LabelList:
    'used only to create the ast and it is not part of the interpreter'
    def __init__(self, node_index, list_label):
        self.node_index = node_index
        self.list_label = list_label


class Label(Instruction):
    def __init__(self, node_index, name, instructions):
        self.node_index = node_index
        self.name = name
        self.instructions = instructions

class Main(Label):
    def __init__(self, node_index, instructions):
        self.node_index = node_index
        self.name = "main"
        self.instructions = instructions