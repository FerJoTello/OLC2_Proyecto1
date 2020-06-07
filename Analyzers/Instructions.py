class Instruction:
    '''original father class'''


class Assignation(Instruction):
    def __init__(self, reg, expr):
        self.reg = reg
        self.expr = expr


class GoTo(Instruction):
    def __init__(self, label):
        self.label = label


class Print(Instruction):
    def __init__(self, content):
        self.content = content


class Exit(Instruction):
    def __init__(self):
        '''exit class'''


class Unset(Instruction):
    def __init__(self, reg):
        self.reg = reg


class If(Instruction):
    def __init__(self, expr, goto):
        self.expr = expr
        self.goto = goto


class Label(Instruction):
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

class Main(Label):
    def __init__(self, instructions):
        self.name = "main"
        self.instructions = instructions