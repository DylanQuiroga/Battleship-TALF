import ply.lex as lex
import ply.yacc as yacc

# Definimos los tokens
tokens = (
    'ATACAR',
    'DEFENDER',
    'COORDINATE',
)

# Definimos las expresiones regulares para los tokens
t_ATACAR = r'Atacar'
t_DEFENDER = r'Defender'
t_COORDINATE = r'[A-J][1-9]0?'

# Ignoramos los espacios en blanco
t_ignore = ' \t'

# Definimos la gramática
def p_command(p):
    'command : action COORDINATE'
    p[0] = (p[1], p[2])

def p_action(p):
    '''action : ATACAR
              | DEFENDER'''
    p[0] = p[1]

# Manejamos los errores
def p_error(p):
    print(f"Error de sintaxis en: {p.value}")

# Función para construir el lexer
def construir_lexer():
    lexer = lex.lex()
    return lexer

# Función para construir el parser
def construir_parser():
    parser = yacc.yacc()
    return parser

def main():
    lexer = construir_lexer()
    parser = construir_parser()

    # Prueba del lexer y el parser con una cadena de ejemplo
    data = "Atacar A5"

    # Tokenize
    lexer.input(data)
    for tok in lexer:
        print(tok)

    # Parse
    result = parser.parse(data)
    print(result)

if __name__ == "__main__":
    main()
