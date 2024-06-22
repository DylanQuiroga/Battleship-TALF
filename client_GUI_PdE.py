import socket
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter import filedialog
import time
import threading
import os
import csv, random
import ply.lex as lex
import ply.yacc as yacc
import pymongo
from pymongo import MongoClient

data = {}

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
    global data
    try:
        if t_COMENZAR == resultado[0]:
            data = load_data('tablero.csv')
            valor = update_mongo_document()
            if data:
                print("datos cargados correctamente 1")
            if valor:
                print("datos cargados correctamente 2")
            return "Juego comenzado, tableros cargados."

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

def load_data(file_name):
    global data
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        data = {rows[0]: int(rows[1]) for rows in reader}
    return data

def update_mongo_document():
    try:
        global data
        filter_criteria = {"codigo": "987654321"}
        # Conectar a la base de datos MongoDB
        client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
        db = client['battleship']
        collection = db['Potencias del eje']

        # Generar el nuevo campo "tablero"
        tablero = [{"coord": k, "state": v} for k, v in data.items()]

        # Actualizar el documento
        collection.update_one(filter_criteria, {"$set": {"tablero": tablero}})

        # Cerrar la conexión
        client.close()
        return True
    
    except Exception as e:
        print(f'Error: {e}')
        return False

def atacar_coordenada(coord):
    filter_criteria = {"codigo": "123456789"}
    # Conectar a la base de datos MongoDB
    client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
    db = client['battleship']
    collection = db['Aliados']

    document = collection.find_one(filter_criteria)
    tablero = document.get("tablero", [])
    coord_state = None
    still_ships = False
    update_needed = False

    if not document:
        print("Documento no encontrado.")
        return None

    for item in tablero:
        if item["coord"] == coord:
            coord_state = item["state"]
            if coord_state == 1:
                item["state"] = -1
                update_needed = True
            elif coord_state == 2:
                if random.random() < 0.5:
                    item["state"] = -1
                    update_needed = True
                break

        if item["state"] in [1, 2]:
            still_ships = True

    if update_needed:
        collection.update_one(filter_criteria, {"$set": {"tablero": tablero}})

    client.close()

    if coord_state is not None:
        if coord_state == 0:
            message = "Agua"
        elif coord_state == 1:
            message = "¡Impacto en un barco!"
        elif coord_state == -1:
            message = "Ya habías impactado este barco antes"
        elif coord_state == 2:
            if random.random() < 0.5:
                data[coord] = -1
                message = "¡Impacto en un barco en posición de defensa!"
            else:
                message = "El misil ha fallado"

    if still_ships:
        message += ", aún hay barcos"
    else:
        message += ", todos los barcos destruidos"

    return str(message)


def defender_coordenada(coord):
    filter_criteria = {"codigo": "987654321"}
    # Conectar a la base de datos MongoDB
    client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
    db = client['battleship']
    collection = db['Potencias del eje']

    document = collection.find_one(filter_criteria)
    if not document:
        print("Documento no encontrado.")
        return None

    tablero = document.get("tablero", [])
    coord_state = None
    still_ships = False
    update_needed = False

    for item in tablero:
        if item["coord"] == coord:
            coord_state = item["state"]
            if coord_state == 1:
                item["state"] = 2
                update_needed = True
                message = "Barco en posición de defensa"
            elif coord_state == 0:
                message = "No hay barcos en esta coordenada"
            elif coord_state == -1:
                message = "Parte de barco destruida, no se puede defender"
            elif coord_state == 2:
                message = "Este barco ya está en posición de defensa"
        
        if item["state"] in [1, 2]:
            still_ships = True

    if update_needed:
        collection.update_one(filter_criteria, {"$set": {"tablero": tablero}})

    client.close()

    if not coord_state:
        message = "Coordenada no encontrada"

    if still_ships:
        message += ", aún hay barcos"
    else:
        message += ", todos los barcos destruidos"
    
    return str(message)

class Board:
    def __init__(self, root, is_enemy=False):
        self.root = root
        self.is_enemy = is_enemy
        self.buttons = {}
        self.create_board_buttons()

    def create_board_buttons(self):
        for i in range(10):
            for j in range(10):
                coord = chr(65 + j) + str(i + 1)
                button = tk.Button(self.root, text=coord, height=2, width=4, command=lambda coord=coord: self.on_button_click(coord))
                button.grid(row=i, column=j)
                self.buttons[coord] = button

    def on_button_click(self, coord):
        if self.is_enemy:
            self.attack(coord)
        else:
            self.defend(coord)

    def attack(self, coord):
        print(f"Atacando {coord}")
        result = atacar_coordenada(coord)
        button = self.buttons[coord]
        if "Agua" in result:
            button.config(bg='blue')
        elif "¡Impacto en un barco!" in result or "¡Impacto en un barco en posición de defensa!" in result:
            button.config(bg='red')
        elif "Ya habías impactado este barco antes" in result:
            button.config(bg='purple')  # Optional, if you want a different color for already hit spots
        print(result)

    def defend(self, coord):
        print(f"Defendiendo {coord}")
        result = defender_coordenada(coord)
        button = self.buttons[coord]
        if "Barco en posición de defensa" in result:
            button.config(bg='green')

    def update_board(self, board_data, update_enemy=False):
        for item in board_data:
            coord = item['coord']
            state = item['state']
            button = self.buttons.get(coord)
            if button:
                if state == 1:
                    button.config(bg='yellow')
                elif state == -1:
                    button.config(bg='red')
                elif state == 2:
                    button.config(bg='green')
                elif state == 0:
                    if not self.is_enemy:
                        button.config(bg='blue')

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chat Cliente-Servidor")
        self._setup_main_window()

    def _setup_main_window(self):
        self.text_widget = tk.Text(self.window, width=100, height=15)
        self.text_widget.pack(padx=10, pady=10)
        
        self.entry = tk.Entry(self.window, width=100)
        self.entry.pack(padx=10, pady=10)
        self.entry.bind("<Return>", self._on_enter_pressed)
        
        self.send_button = tk.Button(self.window, text="Enviar", command=self._on_enter_pressed)
        self.send_button.pack(pady=5)
        
        self.save_button = tk.Button(self.window, text="Guardar Conversación", command=self.save_conversation)
        self.save_button.pack(pady=5)

        self.client = Client(self.text_widget)

        self.board_frame_user = tk.LabelFrame(self.window, text="Tablero Aliado")
        self.board_frame_user.pack(side="left", padx=20, pady=20)

        self.board_frame_enemy = tk.LabelFrame(self.window, text="Tablero Enemigo")
        self.board_frame_enemy.pack(side="right", padx=20, pady=20)

        self.user_board = Board(self.board_frame_user)
        self.enemy_board = Board(self.board_frame_enemy, is_enemy=True)

    def _on_enter_pressed(self, event=None):
        msg = self.entry.get()
        self._insert_message(msg, "Yo")

    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        self.entry.delete(0, tk.END)
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"{sender}: {msg}\n")
        self.text_widget.configure(state=tk.DISABLED)

        response = self.client.send_message(msg)
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"Servidor: {response}\n")
        self.text_widget.configure(state=tk.DISABLED)

        if "Juego comenzado" in response:
            self.load_boards()

    def load_boards(self):
        filter_criteria_user = {"codigo": "987654321"}
        
        client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
        db = client['battleship']
        
        collection_user = db['Potencias del eje']
        document_user = collection_user.find_one(filter_criteria_user)
        if document_user:
            tablero_user = document_user.get("tablero", [])
            self.user_board.update_board(tablero_user)
        
        client.close()

    def save_conversation(self):
        conversation = self.text_widget.get("1.0", tk.END)
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            with open(save_path, "w") as file:
                file.write(conversation)

class Client:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def send_message(self, message):
        comando = analisis(message)
        return comando if comando else "Sin respuesta del servidor"

if __name__ == "__main__":
    gui = GUI()
    gui.window.mainloop()
