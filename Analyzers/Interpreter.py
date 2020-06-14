import Instructions
from Parser import parse
from Expressions import *
from Table import Symbol
from Table import SymbolTable


symbol_table = SymbolTable()
label_table = SymbolTable()
actual_label = None
parameters = False


def process_labels(labels):
    for label in labels:
        label_table.add(label.name, label)


def process_instructions(instructions):
    for instr in instructions:
        if isinstance(instr, Instructions.Assignation):
            if isinstance(instr.reg, Register):
                process_normal_assignation(instr)
            elif isinstance(instr.reg, ArrayRegister):
                process_array_assignation(instr)
        elif isinstance(instr, Instructions.Print):
            process_print(instr)
        elif isinstance(instr, Instructions.If):
            process_if(instr)
        elif isinstance(instr, Instructions.GoTo):
            process_goto(instr)
        elif isinstance(instr, Instructions.Main):
            process_main()
        elif isinstance(instr, Instructions.Label):
            process_label(instr)
        elif isinstance(instr, Instructions.Unset):
            process_unset(instr)
        elif isinstance(instr, Instructions.Exit):
            process_exit()
        else:
            print("Se ha intentado realizar una instrucción inválida")
            print(instr)


def process_normal_assignation(instr):
    'contains a register and an expression'
    primitive = process_expression(instr.expr)
    try:
        symb = Symbol(instr.reg.name, instr.reg.type,
                      primitive.type, primitive.value)
        symbol_table.add(instr.reg.name, symb)
        global actual_label
        if not actual_label.type_defined and symb.reg_type == REG_TYPE.RETURN_VALUE:
            actual_label.type = REG_TYPE.FUNCTION
            actual_label.type_defined = True
    except AttributeError:
        print('*FALLO EN LA ASIGNACION*\nNO SE PUEDE REALIZAR LA ASIGNACIÓN DE', instr.reg.name)


def process_array_assignation(instr):
    'contains an array register and an expression'
    expression = process_expression(instr.expr)
    try:
        index_list = instr.reg.index_list
        array_reg = instr.reg.reg
        symbol_array = symbol_table.get(array_reg.name)
        array = symbol_array.value  # es el diccionario del registro
        i = 1
        name = array_reg.name
        for bracket in index_list:
            primitive_index = process_terminal(bracket)
            index = primitive_index.value
            if i != len(index_list):
                next_array = array.get(index, None)
                i = i+1
                name = name+'['+str(index)+']'
                if next_array == None:
                    array[index] = Symbol(name, array_reg.type, TYPE.ARRAY, {})
                array = array[index]
            else:
                name = name+'['+str(index)+']'
                if isinstance(array, dict):
                    array[index] = Symbol(
                        name, array_reg.type, expression.type, expression.value)
                else:
                    array.value[index] = Symbol(
                        name, array_reg.type, expression.type, expression.value)
    except AttributeError:
        print('*Fallo en la asignación*\nNo se puede realizar la asignaciín de \'' +
              instr.reg.reg.name+'\'')


def process_expression(expr):
    if isinstance(expr, Terminal):
        return process_terminal(expr)
    elif isinstance(expr, BinaryExpression):
        op1 = process_terminal(expr.op1)
        op2 = process_terminal(expr.op2)
        return process_binary_expression(expr.operation, op1, op2)
    elif isinstance(expr, UnitExpression):
        operand = process_terminal(expr.operand)
        return process_unit_expression(expr.operation, operand)


def process_unit_expression(operation, operand):
    operations = {
        UNIT_OPERATION.NEGATIVE: process_negative,
        UNIT_OPERATION.POINTER: process_pointer,
        UNIT_OPERATION.ABSOLUTE: process_absolute,
        LOGIC_OPERATION.NOT: process_not,
        BIT_OPERATION.NOT: process_bit_not,
    }
    operation = operations.get(operation, lambda: print("operador invalido"))
    try:
        return operation(operand)
    except UnboundLocalError:
        print('*TIPO NO VÁLIDOS*\n' +
              'No es posible realizar la operación \''+operation.name+'\'')
        print('Tipo: \''+operand.type.name+'\'')


def process_negative(operand):
    if operand.type == TYPE.INTEGER or operand.type == TYPE.DECIMAL:
        value = - operand.value
    return Primitive('', operand.type, value)


def process_pointer(operand):
    return Primitive('', operand.type, operand.value)


def process_absolute(operand):
    return Primitive('', operand.type, abs(operand.value))


def process_not(operand):
    if (operand.type == TYPE.INTEGER):
        if operand.value == 1:
            value = 0
        elif operand.value == 0:
            value = 1
    return Primitive('', TYPE.INTEGER, value)


def process_bit_not(operand):
    value = ~ operand.value
    return Primitive('', TYPE.INTEGER, value)


def process_binary_expression(operation, op1, op2):
    operations = {
        ARITHMETIC_OPERATION.SUM: process_sum,
        ARITHMETIC_OPERATION.SUBSTRACTION: process_substraction,
        ARITHMETIC_OPERATION.MULTIPLICATION: process_multiplication,
        ARITHMETIC_OPERATION.DIVISION: process_division,
        ARITHMETIC_OPERATION.MODULE: process_module,
        LOGIC_OPERATION.OR: process_or,
        LOGIC_OPERATION.AND: process_and,
        LOGIC_OPERATION.XOR: process_xor,
        RELATIONAL_OPERATION.COMPARISSON: process_comparisson,
        RELATIONAL_OPERATION.DISTINCT: process_distinct,
        RELATIONAL_OPERATION.LESS_EQUAL: process_less_equal,
        RELATIONAL_OPERATION.GREATER_EQUAL: process_greater_equal,
        RELATIONAL_OPERATION.LESS: process_less,
        RELATIONAL_OPERATION.GREATER: process_greater,
        BIT_OPERATION.AND: process_bit_and,
        BIT_OPERATION.OR: process_bit_or,
        BIT_OPERATION.XOR: process_bit_xor,
        BIT_OPERATION.L_SHIFT: process_bit_left_shift,
        BIT_OPERATION.R_SHIFT: process_bit_right_shift,
    }
    function = operations.get(operation, lambda: print("operador invalido"))
    try:
        return function(op1, op2)
    except:
        try:
            print('*TIPOS NO VÁLIDOS*\n' +
                  'No es posible realizar la operación \''+operation.name+'\'')
            # Si no se pudo realizar la operacion es por la compatibilidad de tipos...
            print('Tipos: \''+op1.type.name+'\' y \''+op2.type.name+'\'')
        except AttributeError:
            # ... o es porque se obtuvo un None
            print('Se obtuvo un valor None')
        return None


def process_sum(op1, op2):
    if (op1.type == TYPE.INTEGER and op2.type == TYPE.INTEGER) or (op1.type == TYPE.DECIMAL and op2.type == TYPE.DECIMAL) or (op1.type == TYPE.STRING and op2.type == TYPE.STRING):
        _type = op1.type
        value = op1.value + op2.value
    elif (op1.type == TYPE.CHARACTER and op2.type == TYPE.CHARACTER) or (op1.type == TYPE.CHARACTER and op2.type == TYPE.STRING) or (op1.type == TYPE.STRING and op2.type == TYPE.CHARACTER):
        _type = TYPE.STRING
        value = op1.value + op2.value
    elif (op1.type == TYPE.INTEGER and op2.type == TYPE.DECIMAL) or (op1.type == TYPE.DECIMAL and op2.type == TYPE.INTEGER):
        _type = TYPE.DECIMAL
        value = op1.value + op2.value
    return Primitive('', _type, value)


def process_substraction(op1, op2):
    if op1.type == TYPE.INTEGER and op2.type == TYPE.INTEGER:
        _type = TYPE.INTEGER
        value = op1.value - op2.value
    elif (op1.type == TYPE.INTEGER and op2.type == TYPE.DECIMAL) or (op1.type == TYPE.DECIMAL and op2.type == TYPE.INTEGER):
        _type = TYPE.DECIMAL
        value = op1.value - op2.value
    return Primitive('', _type, value)


def process_multiplication(op1, op2):
    if op1.type == TYPE.INTEGER and op2.type == TYPE.INTEGER:
        _type = TYPE.INTEGER
        value = op1.value * op2.value
    elif (op1.type == TYPE.INTEGER and op2.type == TYPE.DECIMAL) or (op1.type == TYPE.DECIMAL and op2.type == TYPE.INTEGER):
        _type = TYPE.DECIMAL
        value = op1.value * op2.value
    return Primitive('', _type, value)


def process_division(op1, op2):
    if op1.type == TYPE.INTEGER and op2.type == TYPE.INTEGER:
        value = op1.value / op2.value
        if op1.value % op2.value == 0:
            _type = TYPE.INTEGER
        else:
            _type = TYPE.DECIMAL
    elif (op1.type == TYPE.INTEGER and op2.type == TYPE.DECIMAL) or (op1.type == TYPE.DECIMAL and op2.type == TYPE.INTEGER):
        _type = TYPE.DECIMAL
        value = op1.value / op2.value
    return Primitive('', _type, value)


def process_module(op1, op2):
    if (op1.type == TYPE.INTEGER and op2.type == TYPE.INTEGER) or (op1.type == TYPE.INTEGER and op2.type == TYPE.DECIMAL) or (op1.type == TYPE.DECIMAL and op2.type == TYPE.INTEGER):
        value = op1.value % op2.value
    return Primitive('', TYPE.INTEGER, value)


def process_or(op1, op2):
    value = 0
    if (op1.value == 1 or op2.value == 1):
        value = 1
    return Primitive('', TYPE.INTEGER, value)


def process_and(op1, op2):
    value = 0
    if (op1.value == 1 and op2.value == 1):
        value = 1
    return Primitive('', TYPE.INTEGER, value)


def process_xor(op1, op2):
    value = 0
    if (op1.value == 1 and op2.value == 0) or (op1.value == 0 and op2.value == 1):
        value = 1
    return Primitive('', TYPE.INTEGER, value)


def process_comparisson(op1, op2):
    value = 0
    if (op1.value == op2.value):
        value = 1
    return Primitive('', TYPE.INTEGER, value)


def process_distinct(op1, op2):
    value = 0
    if (op1.value != op2.value):
        value = 1
    return Primitive('', TYPE.INTEGER, value)


def process_less_equal(op1, op2):
    value = 0
    if (op1.value <= op2.value):
        value = 1
    return Primitive('', TYPE.INTEGER, value)


def process_greater_equal(op1, op2):
    value = 0
    if (op1.value >= op2.value):
        value = 1
    return Primitive('', TYPE.INTEGER, value)


def process_less(op1, op2):
    value = 0
    if (op1.value < op2.value):
        value = 1
    return Primitive('', TYPE.INTEGER, value)


def process_greater(op1, op2):
    value = 0
    if (op1.value > op2.value):
        value = 1
    return Primitive('', TYPE.INTEGER, value)


def process_bit_and(op1, op2):
    value = op1.value & op2.value
    return Primitive('', TYPE.INTEGER, value)


def process_bit_or(op1, op2):
    value = op1.value | op2.value
    return Primitive('', TYPE.INTEGER, value)


def process_bit_xor(op1, op2):
    value = op1.value ^ op2.value
    return Primitive('', TYPE.INTEGER, value)


def process_bit_left_shift(op1, op2):
    value = op1.value << op2.value
    return Primitive('', TYPE.INTEGER, value)


def process_bit_right_shift(op1, op2):
    value = op1.value >> op2.value
    return Primitive('', TYPE.INTEGER, value)


def process_terminal(term):
    if isinstance(term, Primitive):
        return term
    elif isinstance(term, Register):
        return symbol_table.get_primitive(term.name)
    elif isinstance(term, ArrayRegister):
        'Se está accediendo al índice de un arreglo'
        try:
            array_reg = term.reg
            index_list = term.index_list
            symbol_array = symbol_table.get(array_reg.name)
            array = symbol_array.value  # es el diccionario del registro
            i = 1
            for bracket in index_list:
                index = process_terminal(bracket).value
                if i != len(index_list):
                    array = array.get(index, None)
                    i = i+1
                else:
                    symbol = array.get(index, None)
                    return Primitive('', symbol.value_type, symbol.value)
        except Exception:
            print('*Error al obtener arreglo*\nNo se ha encontrado el indice solicitado para \''+array_reg.name+'\'')
            return None
    elif isinstance(term, Array):
        'Un arreglo está siendo creado'
        return Primitive('', TYPE.ARRAY, {})
    elif isinstance(term, Conversion):
        process_conversion(term)
    '''
    elif isinstance(term, Read):
        #return Primitive(TYPE.Read, [])
    '''


def process_conversion(expr):
    if expr.type == TYPE.INTEGER:
        return convert_int(expr)


def convert_int(expr):
    symb = symbol_table.get(expr.reg.name)
    if symb.type == TYPE.INTEGER:
        return symb.terminal
    elif symb.type == TYPE.DECIMAL:
        ''


def process_if(instr):
    global actual_label
    if not actual_label.type_defined:
        actual_label.type = REG_TYPE.CONTROL
    expr = process_expression(instr.expr)
    if expr.value == 1:
        process_goto(instr.goto)


def process_goto(instr):
    label = label_table.get(instr.label)
    if label != None:
        global actual_label
        aux = actual_label
        actual_label = label
        process_label(label)
        actual_label = aux
    else:
        print("*Error en goto*")
        print("No es posible hacer un salto a \'" +
              instr.label+"\'. No fue definido.")


def process_print(instr):
    try:
        content = process_terminal(instr.content)
        print('>>'+str(content.value))
    except:
        print('*Fallo en print()*')


def process_exit():
    raise Exception


def process_unset(instr):
    if isinstance(instr.reg, Register):
        try:
            del symbol_table.symbols[instr.reg.name]
        except KeyError:
            print(
                '*Fallo en unset()*\nNo se encontró un valor para el registro\''+instr.reg.name+'\'')
    elif isinstance(instr.reg, ArrayRegister):
        name = ''
        try:
            array_reg = instr.reg.reg
            index_list = instr.reg.index_list
            # es el diccionario del registro
            array = symbol_table.get(array_reg.name).value
            i = 1
            name = array_reg.name
            for bracket in index_list:
                index = process_terminal(bracket).value
                if i != len(index_list):
                    array = array.get(index, None)
                    i = i+1
                    name = name+'['+str(index)+']'
                else:
                    name = name+'['+str(index)+']'
                    del array[index]
        except:
            print(
                "*Fallo en unset*\nNo se encontró un valor para el registro '"+name+"'")


def process_label(instr):
    label = label_table.get(instr.name)
    if not label.type_defined:
        label.type = REG_TYPE.CONTROL
    global actual_label
    actual_label = label
    process_instructions(label.instructions)
    label.type_defined = True


def process_main():
    main = label_table.get('main')
    main.type = REG_TYPE.MAIN
    main.type_defined = True
    global actual_label
    actual_label = main
    process_instructions(main.instructions)


def print_things():
    print("*****************************************")
    print("| ID | LABEL_TYPE |")
    for key in label_table.symbols:
        label = label_table.get(key)
        print("| "+label.name+" | "+label.type.name+" |")
    print("*****************************************")
    print("| ID | SYMBOL_TYPE | VALUE_TYPE | VALUE |")
    print_symbols(symbol_table.symbols)
    print("*****************************************")


def print_symbols(symbols):
    for key in symbols:
        symbol = symbols.get(key)
        if symbol.value_type == TYPE.ARRAY:
            print_symbols(symbol.value)
        else:
            print("| "+symbol.name+" | "+symbol.reg_type.name+" | " +
                  symbol.value_type.name+" | "+str(symbol.value)+" |")


#input = "main: $t90 = array(); $a0=15; $a1=2; goto labelXD; $t1=-$v1; print($t1); unset($t1); unset($t1); print($t1); exit; labelXD: $t0=$a0!=$a1; if ($t0) goto labelXD1; $v1=$v0; labelXD1: $v0=2;"
arrays = "main: $t0 = array(); $t0[0]='1'; $t0[1][0]='2'; print($t1[0]);"
instructions = parse(arrays)
process_labels(instructions)
# try:
process_instructions(instructions)
# except Exception:
#print('Ha finalizado la ejecución')
print_things()
