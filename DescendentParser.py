from Tokens import *
import ply.lex as lex
import Instructions
import Expressions
import ply.yacc as yacc
from graphviz import Digraph
n = -1
dot = None

def inc():
    global n
    n = n + 1
    return 'n'+str(n)


lexer = lex.lex()


def p_init(p):
    'init               :   start'
    p[0] = p[1]


def p_start_list_label(p):
    '''start            :   main list_label'''
    node_index = inc()
    dot.node(node_index, 'start')
    dot.edge(node_index, p[1].node_index)
    dot.edge(node_index, p[2].node_index)
    p[0] = [p[1]] + p[2].list_label


def p_start_main(p):
    'start              :   main'
    node_index = inc()
    dot.node(node_index, 'start')
    dot.edge(node_index, p[1].node_index)
    p[0] = [p[1]]


def p_main(p):
    '''main             :   R_MAIN S_COLON list_instr
                        |   R_MAIN error list_instr'''
    node_index = inc()
    dot.node(node_index, 'main')
    dot.edge(node_index, p[3].node_index)
    p[0] = Instructions.Main(node_index, p[3].instructions_list)


def p_list_instr(p):
    'list_instr         :   instr list_instr_p'
    node_index = inc()
    dot.node(node_index, 'instruction')
    instructions = [p[1]] + p[2].instructions_list
    dot.edge(node_index, p[1].node_index)
    p[0] = Instructions.InstructionsList(node_index, instructions)
    try:
        'para vincular la posible lista de instrucciones'
        dot.edge(node_index, p[2].node_index)
    except AttributeError:
        '''es la última instrucción por lo que list_instr_p produce epsilon
        y no contiene atributo para vincular los nodos (ahí levanta error)
        así que se controla el error omitiendo ese vínculo'''


def p_list_instr_p_instr(p):
    'list_instr_p       :   instr list_instr_p'
    node_index = inc()
    instructions = [p[1]] + p[2].instructions_list
    dot.node(node_index, 'instruction')
    dot.edge(node_index, p[1].node_index)
    p[0] = Instructions.InstructionsList(node_index, instructions)
    try:
        'para vincular la posible lista de instrucciones'
        dot.edge(node_index, p[2].node_index)
    except AttributeError:
        '''es la última instrucción por lo que list_instr_p produce epsilon
        y no contiene atributo para vincular los nodos (ahí levanta error)
        así que se controla el error omitiendo ese vínculo'''


def p_list_instr_p_epsilon(p):
    'list_instr_p       :   '
    p[0] = Instructions.InstructionsList(None, [])


def p_instr(p):
    '''instr            :   assignation
                        |   print
                        |   exit
                        |   unset
                        |   goto
                        |   if'''
    p[0] = p[1]


def p_list_label(p):
    'list_label         :   label list_label_p'
    node_index = inc()
    dot.node(node_index, 'label_list')
    labels = [p[1]] + p[2].list_label
    dot.edge(node_index, p[1].node_index)
    p[0] = Instructions.LabelList(node_index, labels)
    try:
        'para vincular la posible lista de labels'
        dot.edge(node_index, p[2].node_index)
    except AttributeError:
        '''es la última instrucción por lo que list_label_p produce epsilon
        y no contiene atributo para vincular los nodos (ahí levanta error)
        así que se controla el error omitiendo ese vínculo'''


def p_list_label_p_label(p):
    'list_label_p         :  label list_label_p'
    node_index = inc()
    labels = [p[1]] + p[2].list_label
    dot.node(node_index, 'label')
    dot.edge(node_index, p[1].node_index)
    p[0] = Instructions.LabelList(node_index, labels)
    try:
        'para vincular la posible lista de labels'
        dot.edge(node_index, p[2].node_index)
    except AttributeError:
        '''es la última instrucción por lo que list_label_p produce epsilon
        y no contiene atributo para vincular los nodos (ahí levanta error)
        así que se controla el error omitiendo ese vínculo'''


def p_list_label_p_epsilon(p):
    'list_label_p         :  '
    p[0] = Instructions.LabelList(None, [])


def p_label(p):
    '''label            :   LABEL_NAME S_COLON list_instr
                        |   LABEL_NAME error list_instr'''
    node_index = inc()
    dot.node(node_index, p.slice[1].value)
    dot.edge(node_index, p[3].node_index)
    p[0] = Instructions.Label(node_index, p[1], p[3].instructions_list)


def p_assignation(p):
    '''assignation      :   register S_EQUAL expression S_SEMICOLON'''
    node_index = inc()
    dot.node(node_index, '=')
    dot.edge(node_index, p[1].node_index)
    dot.edge(node_index, p[3].node_index)
    p[0] = Instructions.Assignation(node_index, p[1], p[3])
    p[0].lineno = p[1].lineno

def p_register(p):
    '''register         :   s_register
                        |   array_register'''
    p[0] = p[1]


def p_s_register(p):
    '''s_register       :   V_TEMP
                        |   V_PARAM
                        |   V_RETURNED
                        |   V_RETURN_LVL
                        |   V_STACK
                        |   V_STACK_POINTER'''
    node_index = inc()
    dot.node(node_index, p.slice[1].value)
    p[0] = Expressions.Register(node_index, p.slice[1].type, p.slice[1].value)
    p[0].lineno = p.slice[1].lineno


def p_array_register(p):
    'array_register     :   s_register list_brackets'
    node_index = inc()
    dot.node(node_index, 'array_register')
    dot.edge(node_index, p[1].node_index)
    for bracket in p[2]:
        dot.edge(node_index, bracket.node_index)
    p[0] = Expressions.ArrayRegister(node_index, p[1], p[2])
    p[0].lineno = p[1].lineno


def p_list_brackets(p):
    'list_brackets      :   S_L_SQR_BRA array_cont S_R_SQR_BRA list_brackets_p'
    p[0] = [p[2]] + p[4]


def p_list_brackets_p_brackets(p):
    'list_brackets_p    :   S_L_SQR_BRA array_cont S_R_SQR_BRA list_brackets_p'
    p[0] = [p[2]] + p[4]


def p_list_brackets_p_epsilon(p):
    'list_brackets_p    :   '
    p[0] = []


def p_array_cont_primitive(p):
    '''array_cont       :   primitive
                        |   s_register'''
    p[0] = p[1]


def p_expression(p):
    '''expression       :   terminal
                        |   simple_unary
                        |   abs
                        |   binary'''
    p[0] = p[1]


def p_binary(p):
    '''binary           :   operand S_SUM operand
                        |   operand S_SUBS operand
                        |   operand S_ASTERISK operand
                        |   operand S_SLASH operand
                        |   operand S_PERCENTAGE operand
                        |   operand OP_OR operand
                        |   operand OP_AND operand
                        |   operand R_XOR operand
                        |   operand OP_COMPARISSON operand
                        |   operand OP_DISTINCT operand
                        |   operand OP_LESS_EQUAL operand
                        |   operand OP_GREATER_EQUAL operand
                        |   operand OP_GREATER operand
                        |   operand OP_LESS operand
                        |   operand OPB_OR operand
                        |   operand OPB_AND operand
                        |   operand OPB_XOR operand
                        |   operand OPB_L_SHIFT operand
                        |   operand OPB_R_SHIFT operand'''
    node_index = inc()
    dot.node(node_index, p.slice[2].value)
    dot.edge(node_index, p[1].node_index)
    dot.edge(node_index, p[3].node_index)
    if p.slice[2].type == 'S_SUM':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.ARITHMETIC_OPERATION.SUM, p[1], p[3])
    elif p.slice[2].type == 'S_SUBS':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.ARITHMETIC_OPERATION.SUBSTRACTION, p[1], p[3])
    elif p.slice[2].type == 'S_ASTERISK':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.ARITHMETIC_OPERATION.MULTIPLICATION, p[1], p[3])
    elif p.slice[2].type == 'S_SLASH':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.ARITHMETIC_OPERATION.DIVISION, p[1], p[3])
    elif p.slice[2].type == 'S_PERCENTAGE':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.ARITHMETIC_OPERATION.MODULE, p[1], p[3])
    elif p.slice[2].type == 'OP_OR':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.LOGIC_OPERATION.OR, p[1], p[3])
    elif p.slice[2].type == 'OP_AND':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.LOGIC_OPERATION.AND, p[1], p[3])
    elif p.slice[2].type == 'R_XOR':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.LOGIC_OPERATION.XOR, p[1], p[3])
    elif p.slice[2].type == 'OP_COMPARISSON':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.RELATIONAL_OPERATION.COMPARISSON, p[1], p[3])
    elif p.slice[2].type == 'OP_DISTINCT':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.RELATIONAL_OPERATION.DISTINCT, p[1], p[3])
    elif p.slice[2].type == 'OP_LESS_EQUAL':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.RELATIONAL_OPERATION.LESS_EQUAL, p[1], p[3])
    elif p.slice[2].type == 'OP_GREATER_EQUAL':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.RELATIONAL_OPERATION.GREATER_EQUAL, p[1], p[3])
    elif p.slice[2].type == 'OP_LESS':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.RELATIONAL_OPERATION.LESS, p[1], p[3])
    elif p.slice[2].type == 'OP_GREATER':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.RELATIONAL_OPERATION.GREATER, p[1], p[3])
    elif p.slice[2].type == 'OPB_OR':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.BIT_OPERATION.OR, p[1], p[3])
    elif p.slice[2].type == 'OPB_AND':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.BIT_OPERATION.AND, p[1], p[3])
    elif p.slice[2].type == 'OPB_XOR':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.BIT_OPERATION.XOR, p[1], p[3])
    elif p.slice[2].type == 'OPB_L_SHIFT':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.BIT_OPERATION.L_SHIFT, p[1], p[3])
    elif p.slice[2].type == 'OPB_R_SHIFT':
        p[0] = Expressions.BinaryExpression(node_index,
                                            Expressions.BIT_OPERATION.R_SHIFT, p[1], p[3])
    p[0].lineno = p.slice[2].lineno

def p_terminal(p):
    '''terminal         :   primitive
                        |   register
                        |   R_READ  S_L_PAR S_R_PAR
                        |   R_ARRAY S_L_PAR S_R_PAR
                        |   conversion'''
    if p.slice[1].type == 'R_READ':
        node_index = inc()
        dot.node(node_index, 'read()')
        p[0] = Expressions.Read(node_index)
        p[0].lineno = p.slice[1].lineno
    elif p.slice[1].type == 'R_ARRAY':
        node_index = inc()
        dot.node(node_index, 'array()')
        p[0] = Expressions.Array(node_index)
        p[0].lineno = p.slice[1].lineno
    else:
        p[0] = p[1]


def p_primitive(p):
    '''primitive        :   INTEGER
                        |   DECIMAL
                        |   STRING
                        |   CHARACTER'''
    if p.slice[1].type == 'INTEGER':
        _type = Expressions.TYPE.INTEGER
    elif p.slice[1].type == 'DECIMAL':
        _type = Expressions.TYPE.DECIMAL
    elif p.slice[1].type == 'STRING':
        _type = Expressions.TYPE.STRING
    elif p.slice[1].type == 'CHARACTER':
        _type = Expressions.TYPE.CHARACTER
    node_index = inc()
    dot.node(node_index, str(p.slice[1].value))
    p[0] = Expressions.Primitive(node_index, _type, p.slice[1].value)


def p_conversion(p):
    '''conversion       :   S_L_PAR R_INT S_R_PAR s_register
                        |   S_L_PAR R_FLOAT S_R_PAR s_register
                        |   S_L_PAR R_CHAR S_R_PAR s_register'''
    if p.slice[2].type == 'R_INT':
        _type = Expressions.TYPE.INTEGER
    elif p.slice[2].type == 'R_FLOAT':
        _type = Expressions.TYPE.DECIMAL
    elif p.slice[2].type == 'R_CHAR':
        _type = Expressions.TYPE.CHARACTER
    node_index = inc()
    dot.node(node_index, 'conversion')
    node_conv_index = inc()
    dot.node(node_conv_index, '('+p.slice[2].value+')')
    dot.edge(node_index, node_conv_index)
    dot.edge(node_index, p[4].node_index)
    p[0] = Expressions.Conversion(node_index, _type, p[4])
    p[0].lineno = p.slice[1].lineno


def p_simple_unary(p):
    '''simple_unary     :   S_SUBS operand
                        |   OPB_AND operand
                        |   OP_NOT operand
                        |   OPB_NOT operand'''
    node_index = inc()
    dot.node(node_index, p.slice[1].value)
    dot.edge(node_index, p[2].node_index)
    if p.slice[1].type == 'S_SUBS':
        p[0] = Expressions.UnitExpression(
            node_index,
            Expressions.UNIT_OPERATION.NEGATIVE,
            p[2])
    elif p.slice[1].type == 'OPB_AND':
        p[0] = Expressions.UnitExpression(
            node_index,
            Expressions.UNIT_OPERATION.POINTER,
            p[2])
    elif p.slice[1].type == 'OP_NOT':
        p[0] = Expressions.UnitExpression(
            node_index,
            Expressions.LOGIC_OPERATION.NOT,
            p[2])
    elif p.slice[1].type == 'OPB_NOT':
        p[0] = Expressions.UnitExpression(
            node_index,
            Expressions.BIT_OPERATION.NOT,
            p[2])
    p[0].lineno = p.slice[1].lineno


def p_operand(p):
    '''operand          :   register
                        |   primitive'''
    p[0] = p[1]


def p_abs(p):
    'abs                :   R_ABS S_L_PAR register S_R_PAR'
    node_index = inc()
    dot.node(node_index, 'abs()')
    dot.edge(node_index, p[3].node_index)
    p[0] = Expressions.UnitExpression(
        node_index,
        Expressions.UNIT_OPERATION.ABSOLUTE,
        p[3])
    p[0].lineno = p.slice[1].lineno


def p_goto(p):
    'goto               :   R_GOTO LABEL_NAME S_SEMICOLON'
    node_index = inc()
    dot.node(node_index, 'goto')
    node_lbl_index = inc()
    dot.node(node_lbl_index, p.slice[2].value)
    dot.edge(node_index, node_lbl_index)
    p[0] = Instructions.GoTo(node_index, p.slice[2].value)
    p[0].lineno = p.slice[1].lineno


def p_print(p):
    'print              :   R_PRINT S_L_PAR operand S_R_PAR S_SEMICOLON'
    node_index = inc()
    dot.node(node_index, 'print()')
    dot.edge(node_index, p[3].node_index)
    p[0] = Instructions.Print(node_index, p[3])
    p[0].lineno = p.slice[1].lineno


def p_exit(p):
    'exit               :   R_EXIT S_SEMICOLON'
    node_index = inc()
    dot.node(node_index, 'exit')
    p[0] = Instructions.Exit(node_index)
    p[0].lineno = p.slice[1].lineno


def p_unset(p):
    'unset              :   R_UNSET S_L_PAR register S_R_PAR S_SEMICOLON'
    node_index = inc()
    dot.node(node_index, 'unset()')
    dot.edge(node_index, p[3].node_index)
    p[0] = Instructions.Unset(node_index, p[3])
    p[0].lineno = p.slice[1].lineno


def p_if(p):
    'if                 :   R_IF S_L_PAR expression S_R_PAR goto'
    node_index = inc()
    dot.node(node_index, 'if')
    dot.edge(node_index, p[3].node_index)
    dot.edge(node_index, p[5].node_index)
    p[0] = Instructions.If(node_index, p[3], p[5])
    p[0].lineno = p.slice[1].lineno


def p_error(p):
    try:
        newError =  "<tr><td><center>Sintáctico</center></td>\n"
        newError = newError + "<td><center>No se esperaba '"+p.value+"'.</center></td>\n" 
        newError = newError + "<td><center>" + str(p.lineno) + "</center></td>\n"
        newError = newError + "</tr>\n"
        reported_errors.append(newError)
    except:
        print("end of file")


def parse(input):
    try:
        global dot
        dot = Digraph('AST')
        dot.filename = 'AST'
        dot.format = 'png'
        lexer.lineno = 0
        instructions = yacc.yacc().parse(input)
        dot.render()
        return instructions
    except Exception as e:
        print(e)
        return None
