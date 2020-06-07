import Instructions
import Expressions
import ply.yacc as yacc
from Tokens import *
lexer = lex.lex()


def p_init(p):
    'init               :   start'
    p[0] = p[1]


def p_start_list_label(p):
    '''start            :   R_MAIN S_COLON list_instr list_label
                        |   R_MAIN error list_instr list_label'''
    main = [Instructions.Main(p[3])]
    p[0] = main + p[4]


def p_start_single_main(p):
    '''start            :   R_MAIN S_COLON list_instr
                        |   R_MAIN error list_instr'''
    p[0] = Instructions.Main(p[3])


def p_list_instr_list(p):
    'list_instr         :   list_instr instr'
    p[1].append(p[2])
    p[0] = p[1]


def p_list_instr_single_instr(p):
    'list_instr         :   instr'
    p[0] = [p[1]]


def p_instr(p):
    '''instr            :   assignation
                        |   goto
                        |   print
                        |   exit
                        |   unset
                        |   if'''
    p[0] = p[1]


def p_instr_error(p):
    'instr              :   error S_SEMICOLON'


def p_list_label_list(p):
    'list_label         :   list_label label'
    p[1].append(p[2])
    p[0] = p[1]


def p_list_label_single(p):
    'list_label         :   label'
    p[0] = [p[1]]


def p_label(p):
    '''label            :   LABEL_NAME S_COLON list_instr'''
    p[0] = Instructions.Label(p[1], p[3])


def p_label_error(p):
    '''label            :   LABEL_NAME error list_instr'''


def p_assignation(p):
    '''assignation      :   register S_EQUAL expression S_SEMICOLON'''
    p[0] = Instructions.Assignation(p[1], p[3])


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
    p[0] = Expressions.Register(p.slice[1].type, p.slice[1].value)


def p_array_register(p):
    'array_register     :   register list_brackets'
    p[0] = Expressions.ArrayRegister(p[1], p[2])


def p_list_array_list(p):
    'list_brackets      :   list_brackets S_L_SQR_BRA array_cont S_R_SQR_BRA'
    p[0] = p[1].append(p[3])


def p_list_array_single(p):
    'list_brackets      :   S_L_SQR_BRA array_cont S_R_SQR_BRA'
    p[0] = [p[2]]


def p_array_cont_primitive(p):
    '''array_cont       :   primitive
                        |   register'''
    p[0] = p[1]


def p_expression(p):
    '''expression       :   terminal
                        |   simple_unary
                        |   arithmetic
                        |   logic
                        |   bit
                        |   relational'''
    p[0] = p[1]


def p_terminal(p):
    '''terminal         :   primitive
                        |   register
                        |   R_READ  S_L_PAR S_R_PAR
                        |   R_ARRAY S_L_PAR S_R_PAR
                        |   conversion'''
    if p.slice[1].type == 'R_READ':
        p[0] = Expressions.Read()
    elif p.slice[1].type == 'R_ARRAY':
        p[0] = Expressions.Array()
    else:
        p[0] = p[1]


def p_primitive(p):
    '''primitive        :   INTEGER
                        |   DECIMAL
                        |   STRING
                        |   CHARACTER'''
    p[0] = Expressions.Primitive(p.slice[1].type, p.slice[1].value)


def p_conversion(p):
    '''conversion       :   S_L_PAR R_INT S_R_PAR register
                        |   S_L_PAR R_FLOAT S_R_PAR register
                        |   S_L_PAR R_CHAR S_R_PAR register'''
    if p.slice[2].type == 'R_INT':
        _type = 'INTEGER'
    elif p.slice[2].type == 'R_FLOAT':
        _type = 'DECIMAL'
    elif p.slice[2].type == 'R_CHAR':
        _type = 'CHARACTER'
    p[0] = Expressions.Conversion(_type, p[4])


def p_simple_unary(p):
    '''simple_unary     :   S_SUBS register
                        |   OPB_AND register'''
    if p.slice[1].type == 'S_SUBS':
        p[0] = Expressions.UnitExpression(
            Expressions.UNIT_OPERATION.NEGATIVE, p[2])
    elif p.slice[1].type == 'OPB_AND':
        p[0] = Expressions.UnitExpression(
            Expressions.UNIT_OPERATION.POINTER, p[2])


def p_arithmetic(p):
    '''arithmetic       :   register S_SUM register
                        |   register S_SUBS register
                        |   register S_ASTERISK register
                        |   register S_SLASH register
                        |   register S_PERCENTAGE register
                        |   R_ABS S_L_PAR register S_L_PAR'''
    if p.slice[2].type == 'S_SUM':
        p[0] = Expressions.BinaryExpression(
            Expressions.ARITHMETIC_OPERATION.SUM, p[1], p[3])
    elif p.slice[2].type == 'S_SUBS':
        p[0] = Expressions.BinaryExpression(
            Expressions.ARITHMETIC_OPERATION.SUBSTRACTION, p[1], p[3])
    elif p.slice[2].type == 'S_ASTERISK':
        p[0] = Expressions.BinaryExpression(
            Expressions.ARITHMETIC_OPERATION.MULTIPLICATION, p[1], p[3])
    elif p.slice[2].type == 'S_SLASH':
        p[0] = Expressions.BinaryExpression(
            Expressions.ARITHMETIC_OPERATION.DIVISION, p[1], p[3])
    elif p.slice[2].type == 'S_PERCENTAGE':
        p[0] = Expressions.BinaryExpression(
            Expressions.ARITHMETIC_OPERATION.MODULE, p[1], p[3])
    elif p.slice[1].type == 'R_ABS':
        p[0] = Expressions.UnitExpression(
            Expressions.UNIT_OPERATION.ABSOLUTE, p[3])


def p_logic(p):
    '''logic            :   OP_NOT register
                        |   register OP_OR register
                        |   register OP_AND register
                        |   register R_XOR register'''
    if p.slice[2].type == 'OP_OR':
        p[0] = Expressions.BinaryExpression(
            Expressions.LOGIC_OPERATION.OR, p[1], p[3])
    elif p.slice[2].type == 'OP_AND':
        p[0] = Expressions.BinaryExpression(
            Expressions.LOGIC_OPERATION.AND, p[1], p[3])
    elif p.slice[2].type == 'R_XOR':
        p[0] = Expressions.BinaryExpression(
            Expressions.LOGIC_OPERATION.XOR, p[1], p[3])
    elif p.slice[1].type == 'OP_NOT':
        p[0] = Expressions.UnitExpression(
            Expressions.LOGIC_OPERATION.NOT, p[2])


def p_bit(p):
    '''bit              :   OPB_NOT register
                        |   register OPB_OR register
                        |   register OPB_AND register
                        |   register OPB_XOR register
                        |   register OPB_L_SHIFT register
                        |   register OPB_R_SHIFT register'''
    if p.slice[2].type == 'OPB_OR':
        p[0] = Expressions.BinaryExpression(
            Expressions.BIT_OPERATION.OR, p[1], p[3])
    elif p.slice[2].type == 'OPB_AND':
        p[0] = Expressions.BinaryExpression(
            Expressions.BIT_OPERATION.AND, p[1], p[3])
    elif p.slice[2].type == 'OPB_XOR':
        p[0] = Expressions.BinaryExpression(
            Expressions.BIT_OPERATION.XOR, p[1], p[3])
    elif p.slice[2].type == 'OPB_L_SHIFT':
        p[0] = Expressions.BinaryExpression(
            Expressions.BIT_OPERATION.L_SHIFT, p[1], p[3])
    elif p.slice[2].type == 'OPB_R_SHIFT':
        p[0] = Expressions.BinaryExpression(
            Expressions.BIT_OPERATION.R_SHIFT, p[1], p[3])
    elif p.slice[1].type == 'OPB_NOT':
        p[0] = Expressions.UnitExpression(
            Expressions.BIT_OPERATION.NOT, p[2])


def p_relational(p):
    '''relational       :   register OP_COMPARISSON register
                        |   register OP_DISTINCT register
                        |   register OP_LESS_EQUAL register
                        |   register OP_GREATER_EQUAL register
                        |   register OP_GREATER register
                        |   register OP_LESS register'''
    if p.slice[2].type == 'OP_COMPARISSON':
        p[0] = Expressions.BinaryExpression(
            Expressions.RELATIONAL_OPERATION.COMPARISSON, p[1], p[3])
    elif p.slice[2].type == 'OP_DISTINCT':
        p[0] = Expressions.BinaryExpression(
            Expressions.RELATIONAL_OPERATION.DISTINCT, p[1], p[3])
    elif p.slice[2].type == 'OP_LESS_EQUAL':
        p[0] = Expressions.BinaryExpression(
            Expressions.RELATIONAL_OPERATION.LESS_EQUAL, p[1], p[3])
    elif p.slice[2].type == 'OP_GREATER_EQUAL':
        p[0] = Expressions.BinaryExpression(
            Expressions.RELATIONAL_OPERATION.GREATER_EQUAL, p[1], p[3])
    elif p.slice[2].type == 'OP_LESS':
        p[0] = Expressions.BinaryExpression(
            Expressions.RELATIONAL_OPERATION.LESS, p[1], p[3])
    elif p.slice[2].type == 'OP_GREATER':
        p[0] = Expressions.BinaryExpression(
            Expressions.RELATIONAL_OPERATION.GREATER, p[1], p[3])


def p_goto(p):
    'goto               :   R_GOTO LABEL_NAME S_SEMICOLON'
    p[0] = Instructions.GoTo(p.slice[2].value)


def p_print(p):
    'print              :   R_PRINT S_L_PAR print_content S_R_PAR S_SEMICOLON'
    p[0] = Instructions.Print(p[3])


def p_print_content(p):
    '''print_content    :   register
                        |   primitive'''
    p[0] = p[1]


def p_exit(p):
    'exit               :   R_EXIT S_SEMICOLON'
    p[0] = Instructions.Exit()


def p_unset(p):
    'unset              :   R_UNSET S_L_PAR register S_R_PAR S_SEMICOLON'
    p[0] = Instructions.Unset(p[3])


def p_if(p):
    'if                 :   R_IF S_L_PAR expression S_R_PAR goto'
    p[0] = Instructions.If(p[3], p[5])


def p_error(p):
    print("Error sintáctico en '%s'" % p.value)
    print(p)
    if not p:
        print("end of file")
        return

    # panic mode for ';'

    # parser.errok()
    # parser.restart()
    # return tok


parser = yacc.yacc()

input = "main :\n\t$a0=$t1+$tw+$tx;\n\t$t1=$t2+$t3+$t4;"

popeado = 'main: \t\n print(sex); $t0 = read(); \t\n  \t\n goto $t3; \n ret0: \t\n $t90 = array(); \t\n exit; \t\n f1: \n $a1 = $efecamaster; \t\n goto f2; \t\n ret1: \n $v0 = $v1; \t\n goto ret0; \t\n f2: \n $v1 = $a1*$a1; \t\n goto ret1;'
#lexer = lex.lex()

# lexer.input(popeado)

parser.parse(popeado)
