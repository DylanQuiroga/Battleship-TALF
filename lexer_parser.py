import ply.lex as lex
import ply.yacc as yacc

# Definimos los tokens
tokens = (
    'ATACAR',
    'DEFENDER',
    'COORDINATE',
    'COMENZAR'
)

# Definimos las expresiones regulares para los tokens
t_ATACAR = r'Atacar'
t_DEFENDER = r'Defender'
t_COORDINATE = r'[A-J][1-9]0?'
t_COMENZAR = r'Comenzar'

# Ignoramos los espacios en blanco
t_ignore = ' \t'

# Definimos la gramática
def p_command(p):
    '''command : action COORDINATE
               | COMENZAR'''  # Nueva regla para "Comenzar" sin FILENAME
    p[0] = (p[1], p[2] if len(p) > 2 else None)

def p_action(p):
    '''action : ATACAR
              | DEFENDER'''
    p[0] = p[1]

# Manejamos los errores
def p_error(p):
    print(f"Error de sintaxis en: {p.value}")

# Construimos el lexer y el parser
lexer = lex.lex()
parser = yacc.yacc()

def analisis(entrada):
    try:
        resultado = parser.parse(entrada)
        mensaje = analizarMensaje(resultado)
        return mensaje
    except Exception as e:
        # Si no es un comando válido, devolvemos el mensaje original
        return entrada

def analizarMensaje(resultado):
    # Implementación de la lógica para analizar el mensaje
    pass
