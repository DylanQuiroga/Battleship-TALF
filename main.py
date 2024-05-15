import ply.lex as lex
import ply.yacc as yacc
import tkinter as tk
from tkinter import messagebox

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

# Construimos el lexer y el parser
lexer = lex.lex()
parser = yacc.yacc()

# Creamos la ventana de la GUI
window = tk.Tk()
window.title("Batalla Naval")

# Función para manejar el comando
def handle_command():
    command = entry.get()
    try:
        result = parser.parse(command)
        
        action = result[0]
        coordinate = result[1]
        
        vertical_coordinate = coordinate[0]
        horizontal_coordinate = coordinate[1:]
        
        message = f"Comando: {action}\nCoordenada vertical: {vertical_coordinate}\nCoordenada horizontal: {horizontal_coordinate}"
        
        messagebox.showinfo("Comando", message)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Campo de entrada para el comando
entry = tk.Entry(window)
entry.pack()

# Botón para manejar el comando
button = tk.Button(window, text="Ingresar comando", command=handle_command)
button.pack()

# Iniciamos la GUI
window.mainloop()
