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
               | COMENZAR'''
    if len(p) == 2:
        p[0] = (p[1], None)
    else:
        p[0] = (p[1], p[2])

def p_action(p):
    '''action : ATACAR
              | DEFENDER'''
    p[0] = p[1]

# Manejamos los errores
def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}', línea {p.lineno}")
    else:
        print("Error de sintaxis al final del archivo")


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
        print("no es un comando valido")
        return entrada

def analizarMensaje(resultado):
    global data
    try:
        if t_COMENZAR == resultado[0]:
            data = load_data('tablero.csv')
            valor = update_mongo_document()
            if data:
                print("datos cargados correctamente 1")
            if valor:
                print("datos cargados correctamente 2")

        elif t_ATACAR == resultado[0]:
            coord = resultado[1]
            coord_vertical = coord[0]
            coord_horizontal = coord[1:]
            coord = coord_vertical + coord_horizontal
            mensaje = atacar_coordenada(coord)
            return mensaje
        elif t_DEFENDER == resultado[0]:
            coord = resultado[1]
            coord_vertical = coord[0]
            coord_horizontal = coord[1:]
            coord = coord_vertical + coord_horizontal
            mensaje = defender_coordenada(coord)
            return mensaje
        else:
            return "error tipo 0"

    except lex.LexError as lex_error:
        print(f"Error léxico: {lex_error}")
        return "error tipo 1"
    except Exception as e:
        print(e)
        return "error tipo 2"
    pass
