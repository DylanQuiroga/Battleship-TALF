
from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox #Tkinter Python Module for GUI  
import socket #Sockets for network connection
import threading # for multiple proccess 
import csv
import ply.lex as lex
import ply.yacc as yacc
import re
import random

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

def handle_command(entrada):
    try:
        result = parser.parse(entrada)
        
        action = result[0]
        coordinate = result[1]
        
        vertical_coordinate = coordinate[0]
        horizontal_coordinate = coordinate[1:]
        coord = vertical_coordinate + horizontal_coordinate
        #message = f"Comando: {action}\nCoordenada vertical: {vertical_coordinate}\nCoordenada horizontal: {horizontal_coordinate}"
        #messagebox.showinfo("Comando", message)

        if action == t_ATACAR:
            mensaje = check_coordinate(coord, data)
            return mensaje
        elif action == t_DEFENDER:
            mensaje = defender_coordinate(coord, data)
            return mensaje

    except Exception as e:
        print("mensaje normal")

def eliminar_nombre(texto):
    # La expresión regular busca cualquier palabra seguida de ": "
    texto_limpio = re.sub(r'\w+: ', '', texto)
    return texto_limpio

def load_data(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        data = {rows[0]: int(rows[1]) for rows in reader}
    return data

def check_coordinate(coord, data):
    if coord in data:
        if data[coord] == 1:
            data[coord] = -1  # Cambia el valor a -1
            message = "¡Impacto en un barco!"
        elif data[coord] == 0:
            message = "Agua"
        elif data[coord] == -1:
            message = "Ya habías impactado este barco antes"
        elif data[coord] == 2:
            if random.random() < 0.5:
                data[coord] = -1
                message = "¡Impacto en un barco en posición de defenza!"
            else:
                message = "El misil ha fallado"
    else:
        return "Coordenada no válida"

    # Verifica si aún hay barcos en el diccionario
    if 1 in data.values() or 2 in data.values():
        message += ", aún hay barcos"
    else:
        message += ", todos los barcos destruidos"

    return str(message)

def defender_coordinate(coord, data):
    if coord in data:
        if data[coord] == 1:
            data[coord] = 2 # el numero 2 es una casilla de barco en posición de defenza
            message = "Barco en posición de defenza"
        elif data[coord] == 0:
            message = "No hay barcos en esta coordenada"
        elif data[coord] == -1:
            message = "Parte de barco destruida, no se puede defender"
        elif data[coord] == 2:
            message = "Este barco ya está en posición de defenza"
    else:
        return "Coordenada no válida"
    
    if 1 in data.values() or 2 in data.values():
        message += ", aún hay barcos"
    else:
        message += ", todos los barcos destruidos"

    return str(message)

class GUI:
    client_socket = None
    last_received_message = None
    
    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.initialize_socket()
        self.initialize_gui()
        self.listen_for_incoming_messages_in_a_thread()

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialazing socket with TCP and IPv4
        remote_ip = '127.0.0.1' # IP address 
        remote_port = 10319 #TCP port
        self.client_socket.connect((remote_ip, remote_port)) #connect to the remote server

    def initialize_gui(self): # GUI initializer
        self.root.title("Socket Chat") 
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_name_section()
        self.display_chat_entry_box()
    
    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,)) # Create a thread for the send and receive in same time 
        thread.start()
    #function to recieve msg
    def receive_message_from_server(self, so):
        while True:
            buffer = so.recv(256)
            if not buffer:
                break
            message = buffer.decode('utf-8')
         
            if "joined" in message:
                user = message.split(":")[1]
                message = user + " ha entrado"
                self.chat_transcript_area.insert('end', message + '\n')
                self.chat_transcript_area.yview(END)
            else:
                # Aqui se puede empezar a analizar los comandos de PLY
                mensaje_limpio = eliminar_nombre(message)
                print(mensaje_limpio)
                mensaje = handle_command(mensaje_limpio)
                self.chat_transcript_area.insert('end', message + '\n')
                self.chat_transcript_area.yview(END)
                self.enviarMensajePLY(mensaje)
                self.clear_text()

        so.close()

    def display_name_section(self):
        frame = Frame()
        Label(frame, text='Ingresa tu nombre:', font=("Helvetica", 16)).pack(side='left', padx=10)
        self.name_widget = Entry(frame, width=50, borderwidth=2)
        self.name_widget.pack(side='left', anchor='e')
        self.join_button = Button(frame, text="Entrar", width=10, command=self.on_join).pack(side='left')
        frame.pack(side='top', anchor='nw')

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='Caja de texto:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.chat_transcript_area = Text(frame, width=60, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Ingresa un mensaje:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.enter_text_widget = Text(frame, width=60, height=3, font=("Serif", 12))
        self.enter_text_widget.pack(side='left', pady=15)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')

    def on_join(self):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror(
                "Enter your name", "Enter your name to send a message")
            return
        self.name_widget.config(state='disabled')
        self.client_socket.send(("joined:" + self.name_widget.get()).encode('utf-8'))

    def on_enter_key_pressed(self, event):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror("Enter your name", "Enter your name to send a message")
            return
        self.send_chat()
        self.clear_text()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    def send_chat(self):
        senders_name = self.name_widget.get().strip() + ": "
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = (senders_name + data).encode('utf-8')
        self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)
        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'
    
    def enviarMensajePLY(self, mensaje: str):
        if not mensaje is None:
            mensajeBytes = ("Capitán : " + mensaje).encode('utf-8')
            self.chat_transcript_area.insert('end', mensajeBytes.decode('utf-8') + '\n')
            self.chat_transcript_area.yview(END)
            self.client_socket.send(mensajeBytes)
            self.enter_text_widget.delete(1.0, 'end')
            return 'break'
        
    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)

data = load_data("tablero.csv")
root = Tk()
gui = GUI(root)
root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
root.mainloop()
