reserved = {
    'int' :     'R_INT',
    'float':    'R_FLOAT',
    'char':     'R_CHAR',
    'array':    'R_ARRAY',
    'main':     'R_MAIN',
    'goto':     'R_GOTO',
    'print':    'R_PRINT',
    'read':     'R_READ',
    'unset':    'R_UNSET',
    'exit':     'R_EXIT',
    'if':       'R_IF',
    'xor':      'R_XOR',
    'abs':      'R_ABS',
}

tokens = [
    'S_SUM',
    'S_SUBS',
    'S_ASTERISK',
    'S_SLASH',
    'S_PERCENTAGE',
    'S_EQUAL',
    'S_L_PAR',
    'S_R_PAR',
    'S_L_SQR_BRA',
    'S_R_SQR_BRA',
    'S_COLON',
    'S_SEMICOLON',
    'OP_COMPARISSON',
    'OP_DISTINCT',
    'OP_LESS_EQUAL',
    'OP_GREATER_EQUAL',
    'OP_LESS',
    'OP_GREATER',
    'OP_OR',
    'OP_AND',
    'OP_NOT',
    'OPB_L_SHIFT',
    'OPB_R_SHIFT',
    'OPB_OR',
    'OPB_AND',
    'OPB_NOT',
    'OPB_XOR',
    'LABEL_NAME',
    'V_TEMP',
    'V_PARAM',
    'V_RETURNED',
    'V_RETURN_LVL',
    'V_STACK',
    'V_STACK_POINTER',
    'DECIMAL',
    'INTEGER',
    'CHARACTER',
    'STRING',
    'COMMENT'
]   +   list(reserved.values())


#   Tokens as variables
t_S_SUM             = r'\+'
t_S_SUBS            = r'-'
t_S_ASTERISK        = r'\*'
t_S_SLASH           = r'/'
t_S_PERCENTAGE      = r'%'
t_S_EQUAL           = r'='
t_S_L_PAR           = r'\('
t_S_R_PAR           = r'\)'
t_S_L_SQR_BRA       = r'\['
t_S_R_SQR_BRA       = r'\]'
t_S_COLON           = r':'
t_S_SEMICOLON       = r';'
t_OP_COMPARISSON    = r'=='
t_OP_DISTINCT       = r'!='
t_OP_LESS_EQUAL     = r'<='
t_OP_GREATER_EQUAL  = r'>='
t_OP_LESS           = r'<'
t_OP_GREATER        = r'>'
t_OP_OR             = r'\|\|'
t_OP_AND            = r'&&'
t_OP_NOT            = r'!'
t_OPB_L_SHIFT       = r'<<'
t_OPB_R_SHIFT       = r'>>'
t_OPB_OR            = r'\|'
t_OPB_AND           = r'&'
t_OPB_NOT           = r'~'
t_OPB_XOR           = r'\^'

def t_LABEL_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'LABEL_NAME')
    return t

def t_V_TEMP(t):
    r'\$t\d+'
    t.value = str(t.value)
    return t

def t_V_PARAM(t):
    r'\$a\d+'
    t.value = str(t.value)
    return t

def t_V_RETURNED(t):
    r'\$v\d+'
    t.value = str(t.value)
    return t

def t_V_RETURN_LVL(t):
    r'\$ra'
    t.value = str(t.value)
    return t

def t_V_STACK(t):
    r'\$s\d+'
    t.value = str(t.value)
    return t

def t_V_STACK_POINTER(t):
    r'\$sp'
    t.value = str(t.value)
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("No se pudo convertir %d", t.value)
        t.value = 0
    return t

def t_INTEGER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("No se pudo convertir %d", t.value)
        t.value = 0
    return t

def t_CHARACTER(t):
    r'(\".\"|\'.\')'
    t.value = t.value[1:-1]
    return t

def t_STRING(t):
    r'(\'.*?\'|\".*?\")'
    t.value = t.value[1:-1]
    return t

def t_COMMENT(t):
    r'\#(.*)'
    t.lexer.lineno += 1
    t.lexer.skip(1)

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Caracter no valido '%s'" % t.value[0])
    t.lexer.skip(1)

'''
lexer = lex.lex()

lexer.input("main:\n\t$t1=\"sex\";\n\t$a0=$t1;")

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
'''