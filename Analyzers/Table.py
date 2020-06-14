from enum import Enum
from Expressions import Primitive


class Symbol:
    def __init__(self, name, _type, value_type, value):
        self.name = name
        self.reg_type = _type
        self.value_type = value_type
        self.value = value


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add(self, name, symbol):
        self.symbols[name] = symbol

    def get_primitive(self, name):
        try:
            symbol = self.get(name)
            return Primitive('', symbol.value_type, symbol.value)
        except AttributeError:
            print("*ERROR*\nNo se ha definido", name)
            return None

    def get(self, name):
        return self.symbols.get(name, None)

    def update(self, symbol):
        if symbol.name in self.symbols:
            self.symbols[symbol.name] = symbol

    def delete(self, name):
        ''
    