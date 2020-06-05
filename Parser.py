from Tokens import *
lexer = lex.lex()

def p_init(t):
    'init               :   start'
    t[0] = t[1]

def p_start_list_label(t):
    'start              :   R_MAIN S_COLON list_instr list_label'
    
def p_start_single_main(t):
    'start              :   R_MAIN S_COLON list_instr'

def p_list_instr_list(t):
    'list_instr         :   list_instr instr'
    t[1].append(t[2])
    t[0] = t[1]

def p_list_instr_single_instr(t):
    'list_instr         :   instr'
    t[0] = [t[1]]

def p_instr(t):
    '''instr            :   assignation
                        |   goto
                        |   print
                        |   exit
                        |   unset
                        |   if'''
    t[0] = t[1]

def p_list_label_list(t):
    'list_label         :   list_label label'
    t[1].append(t[2])
    t[0] = t[1]

def p_list_label_single(t):
    'list_label         :   label'
    t[0] = [t[1]]

def p_label(t):
    'label              :   LABEL_NAME S_COLON list_instr'

def p_assignation(t):
    'assignation        :   register S_EQUAL expression S_SEMICOLON'

def p_register(t):
    '''register         :   s_register
                        |   array_register'''

def p_s_register(t):
    '''s_register       :   V_TEMP
                        |   V_PARAM
                        |   V_RETURNED
                        |   V_RETURN_LVL
                        |   V_STACK
                        |   V_STACK_POINTER'''

def p_array_register(t):
    'array_register     :   register list_array'

def p_list_array_list(t):
    'list_array         :   list_array S_L_SQR_BRA array_cont S_R_SQR_BRA'
    #t[0] = t[1]

def p_list_array_single(t):
    'list_array         :   S_L_SQR_BRA array_cont S_R_SQR_BRA'
    #t[0] = [t[1]]

def p_array_cont(t):
    '''array_cont       :   primitive
                        |   s_register'''

def p_expression(t):
    '''expression       :   simple_unary
                        |   conversion
                        |   arithmetic
                        |   logic
                        |   bit
                        |   relational'''

def p_simple_unary(t):
    '''simple_unary     :   primitive
                        |   register
                        |   S_SUBS register
                        |   OPB_AND register
                        |   R_READ  S_L_PAR S_R_PAR
                        |   R_ARRAY S_L_PAR S_R_PAR'''

def p_primitive(t):
    '''primitive        :   INTEGER
                        |   DECIMAL
                        |   STRING'''

def p_conversion(t):
    '''conversion       :   S_L_PAR R_INT S_R_PAR register
                        |   S_L_PAR R_FLOAT S_R_PAR register
                        |   S_L_PAR R_CHAR S_R_PAR register'''

def p_arithmetic(t):
    '''arithmetic       :   register S_SUM register
                        |   register S_SUBS register
                        |   register S_ASTERISK register
                        |   register S_SLASH register
                        |   register S_PERCENTAGE register
                        |   R_ABS S_L_PAR register S_L_PAR'''

def p_logic(t):
    '''logic            :   OP_NOT register
                        |   register OP_OR register
                        |   register OP_AND register
                        |   register R_XOR register'''

def p_bit(t):
    '''bit              :   OPB_NOT register
                        |   register OPB_AND register
                        |   register OPB_OR register
                        |   register OPB_L_SHIFT register
                        |   register OPB_R_SHIFT register'''

def p_relational(t):
    '''relational       :   register OP_COMPARISSON register
                        |   register OP_DISTINCT register
                        |   register OP_LESS_EQUAL register
                        |   register OP_GREATER_EQUAL register
                        |   register OP_GREATER register
                        |   register OP_LESS register'''

def p_goto(t):
    'goto               :   R_GOTO LABEL_NAME S_SEMICOLON'

def p_print(t):
    'print              :   R_PRINT S_L_PAR expression S_R_PAR'

def p_exit(t):
    'exit               :   R_EXIT S_SEMICOLON'

def p_unset(t):
    'unset              :   R_UNSET S_L_PAR register S_R_PAR S_SEMICOLON'

def p_if(t):
    'if                 :   R_IF S_L_PAR expression S_R_PAR goto'

def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()

input = "main ;\n\t$t1=\"sex\";\n\t$a0=$t1;"

parser.parse(input)
