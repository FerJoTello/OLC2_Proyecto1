from Tokens import *
import Instructions
import Expressions
import ply.yacc as yacc
from graphviz import Digraph
n = -1


def inc():
    global n
    n = n + 1
    return 'n'+str(n)


dot = Digraph('AST')


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
    p[0] = p[1]


def p_main(p):
    '''main             :   R_MAIN S_COLON list_instr
                        |   R_MAIN error list_instr'''
    node_index = inc()
    dot.node(node_index, 'main')
    dot.edge(node_index, p[3].node_index)
    p[0] = Instructions.Main(node_index, p[3])


def p_list_instr_list(p):
    'list_instr         :   list_instr instr'
    node_index = inc()
    dot.node(node_index, 'list_instr')
    dot.edge(node_index, p[1].node_index)
    dot.edge(node_index, p[2].node_index)
    p[1].instructions_list.append(p[2])
    p[0] = Instructions.InstructionsList(node_index, p[1].instructions_list)


def p_list_instr_single_instr(p):
    'list_instr         :   instr'
    node_index = inc()
    dot.node(node_index, 'list_instr')
    dot.edge(node_index, p[1].node_index)
    p[0] = Instructions.InstructionsList(node_index, [p[1]])


def p_instr(p):
    '''instr            :   assignation
                        |   print
                        |   exit
                        |   unset
                        |   goto
                        |   if'''
    p[0] = p[1]


def p_instr_error(p):
    'instr              :   error S_SEMICOLON'


def p_list_label_list(p):
    'list_label         :   list_label label'
    node_index = inc()
    dot.node(node_index, 'list_label')
    dot.edge(node_index, p[1].node_index)
    dot.edge(node_index, p[2].node_index)
    p[1].list_label.append(p[2])
    list_label = p[1].list_label
    p[0] = Instructions.LabelList(node_index, list_label)


def p_list_label_single(p):
    'list_label         :   label'
    node_index = inc()
    dot.node(node_index, 'list_label')
    dot.edge(node_index, p[1].node_index)
    p[0] = Instructions.LabelList(node_index, [p[1]])


def p_label(p):
    '''label            :   LABEL_NAME S_COLON list_instr'''
    node_index = inc()
    dot.node(node_index, p.slice[1].value)
    dot.edge(node_index, p[3].node_index)
    p[0] = Instructions.Label(node_index, p[1], p[3])


def p_label_error(p):
    '''label            :   LABEL_NAME error list_instr'''


def p_assignation(p):
    '''assignation      :   register S_EQUAL expression S_SEMICOLON'''
    node_index = inc()
    dot.node(node_index, '=')
    dot.edge(node_index, p[1].node_index)
    dot.edge(node_index, p[3].node_index)
    p[0] = Instructions.Assignation(node_index, p[1], p[3])


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


def p_array_register(p):
    'array_register     :   s_register list_brackets'
    node_index = inc()
    dot.node(node_index, 'array_register')
    dot.edge(node_index, p[1].node_index)
    for bracket in p[2]:
        dot.edge(node_index, bracket.node_index)
    p[0] = Expressions.ArrayRegister(node_index, p[1], p[2])


def p_list_array_list(p):
    'list_brackets      :   list_brackets S_L_SQR_BRA array_cont S_R_SQR_BRA'
    p[1].append(p[3])
    p[0] = p[1]


def p_list_array_single(p):
    'list_brackets      :   S_L_SQR_BRA array_cont S_R_SQR_BRA'
    p[0] = [p[2]]


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
    '''binary           :   register S_SUM register
                        |   register S_SUBS register
                        |   register S_ASTERISK register
                        |   register S_SLASH register
                        |   register S_PERCENTAGE register
                        |   register OP_OR register
                        |   register OP_AND register
                        |   register R_XOR register
                        |   register OP_COMPARISSON register
                        |   register OP_DISTINCT register
                        |   register OP_LESS_EQUAL register
                        |   register OP_GREATER_EQUAL register
                        |   register OP_GREATER register
                        |   register OP_LESS register
                        |   register OPB_OR register
                        |   register OPB_AND register
                        |   register OPB_XOR register
                        |   register OPB_L_SHIFT register
                        |   register OPB_R_SHIFT register'''
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
    elif p.slice[1].type == 'R_ARRAY':
        node_index = inc()
        dot.node(node_index, 'array()')
        p[0] = Expressions.Array(node_index)
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
    p[0] = Expressions.Primitive(node_index, _type, str(p.slice[1].value))


def p_conversion(p):
    '''conversion       :   S_L_PAR R_INT S_R_PAR register
                        |   S_L_PAR R_FLOAT S_R_PAR register
                        |   S_L_PAR R_CHAR S_R_PAR register'''
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


def p_simple_unary(p):
    '''simple_unary     :   S_SUBS register
                        |   OPB_AND register
                        |   OP_NOT register
                        |   OPB_NOT register'''
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


def p_abs(p):
    'abs                :   R_ABS S_L_PAR register S_R_PAR'
    node_index = inc()
    dot.node(node_index, 'abs()')
    dot.edge(node_index, p[3].node_index)
    p[0] = Expressions.UnitExpression(
        node_index,
        Expressions.UNIT_OPERATION.ABSOLUTE,
        p[3])


def p_goto(p):
    'goto               :   R_GOTO LABEL_NAME S_SEMICOLON'
    node_index = inc()
    dot.node(node_index, 'goto')
    node_lbl_index = inc()
    dot.node(node_lbl_index, p.slice[2].value)
    dot.edge(node_index, node_lbl_index)
    p[0] = Instructions.GoTo(node_index, p.slice[2].value)


def p_print(p):
    'print              :   R_PRINT S_L_PAR print_content S_R_PAR S_SEMICOLON'
    node_index = inc()
    dot.node(node_index, 'print()')
    dot.edge(node_index, p[3].node_index)
    p[0] = Instructions.Print(node_index, p[3])


def p_print_content(p):
    '''print_content    :   register
                        |   primitive'''
    p[0] = p[1]


def p_exit(p):
    'exit               :   R_EXIT S_SEMICOLON'
    node_index = inc()
    dot.node(node_index, 'exit')
    p[0] = Instructions.Exit(node_index)


def p_unset(p):
    'unset              :   R_UNSET S_L_PAR register S_R_PAR S_SEMICOLON'
    node_index = inc()
    dot.node(node_index, 'unset()')
    dot.edge(node_index, p[3].node_index)
    p[0] = Instructions.Unset(node_index, p[3])


def p_if(p):
    'if                 :   R_IF S_L_PAR expression S_R_PAR goto'
    node_index = inc()
    dot.node(node_index, 'if')
    dot.edge(node_index, p[3].node_index)
    dot.edge(node_index, p[5].node_index)
    p[0] = Instructions.If(node_index, p[3], p[5])


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

#input = "main :\n\t$a0=$t1;\n\t$t1=$t2+$t3;"
#input = "main :\n\t$a0=$t1;\n\t$t1=$t2+$t3; label1:$t5='xd';"
#input = "main :\n\t$a0=$t1;\n\t$t1=$t2+$t3; $t5=32; $sp=(int)$t5; $t6=abs( $sp ); $t7=array(); $t8=-$t6;"
#
input2 = "main :\n\t$a0=$t1;\n\t$t1['valor']=$t2+$t3; $t1[1][0]=32; $t1[2][0][0]='se popeo'; aasdasd: goto xd; $sp='feca'; print($sp); xd:if ($t1!=$t5) goto aasdasd; exit;"
popeado = 'main: \t\n print(sex); $t0 = read(); \t\n  \t\n goto $t3; \n ret0: \t\n $t90 = array(); \t\n exit; \t\n f1: \n $a1 = $efecamaster; \t\n goto f2; \t\n ret1: \n $v0 = $v1; \t\n goto ret0; \t\n f2: \n $v1 = $a1*$a1; \t\n goto ret1;'
#lexer = lex.lex()

# lexer.input(popeado)

# parser.parse(input)
parser.parse(input2)
dot.view()
'''
'''
