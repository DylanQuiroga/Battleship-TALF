import socket
import subprocess
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
import random
data = {}

# Definimos los tokens
tokens = (
    'ATACAR',
    'DEFENDER',
    'COORDINATE',
    'COMENZAR',
    'ESCANEAR',
    'CAMBIO',
    'TABLERO',
    'PROPIO',
    'ENEMIGO',
    'AYUDA'
)

# Definimos las expresiones regulares para los tokens
t_ATACAR = r'Atacar'
t_DEFENDER = r'Defender'
t_COORDINATE = r'[A-J][1-9]0?'
t_COMENZAR = r'Comenzar'
t_ESCANEAR = r'Escanear'
t_CAMBIO = r'Cambio'
t_TABLERO = r'Tablero'
t_PROPIO = r'propio'
t_ENEMIGO = r'enemigo'
t_AYUDA = r'Ayuda'

# Ignoramos los espacios en blanco
t_ignore = ' \t'

# Definimos la gramática
def p_command(p):
    '''command : action COORDINATE
                | COMENZAR
                | TABLERO bando
                | CAMBIO
                | AYUDA'''
    p[0] = (p[1], p[2] if len(p) > 2 else None)

def p_action(p):
    '''action : ATACAR
              | DEFENDER
              | ESCANEAR'''
    p[0] = p[1]

def p_bando(p):
    '''bando : PROPIO
             | ENEMIGO'''
    p[0] = p[1]

# Manejamos los errores
def p_error(p):
    print(f"Error de sintaxis en: {p.value if p else 'EOF'}")

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
            mensaje = iniciar_juego()
            return mensaje
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
        elif t_ESCANEAR == resultado[0]:
            coord = resultado[1]
            coord_vertical = coord[0]
            coord_horizontal = coord[1:]
            coord = coord_vertical + coord_horizontal
            mensaje = escanear_coordenada(coord)
            return mensaje
        elif t_CAMBIO == resultado[0]:
            cambiar_turno(0, True)
            cambiar_turno(1, False)
            restaurar_acciones()
            return "Cambio de turno"
        elif t_TABLERO == resultado[0]:
            if t_PROPIO == resultado[1]:
                abrirTableroPropio()
            elif t_ENEMIGO == resultado[1]:
                abrirTableroEnemigo()
            else:
                return "error tipo -1"
        elif t_AYUDA == resultado[0]:
            return "\nComandos disponibles:\n\nAtacar: Ataca una casilla.\nEjemplo: Atacar A1\n\nDefender: Defiende una casilla.\nEjemplo: Defender A1\n\nEscanear: Escanea una casilla en un area de 3x3\n\nCambio: Cambia el turno\n\nTablero: Permite ver el tablero.\nEjemplo: Tablero propio o Tablero enemigo\n\nComenzar: Inicia el juego\n\nAyuda: Muestra los comandos disponibles\n\n"
        else:
            return "error tipo 0"
        
    except lex.LexError as lex_error:
        print(f"Error léxico: {lex_error}")
        return "error tipo 1"
    except Exception as e:
        print(e)
        return "error tipo 2"
    
def abrirTableroPropio():
    subprocess.Popen(["python", "gui_tablero_aliado.py"])

def abrirTableroEnemigo():
    subprocess.Popen(["python", "gui_tablero_eje_oculto.py"])

def load_data(file_name):
    global data
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        data = {rows[0]: int(rows[1]) for rows in reader}
    return data

import threading
import random

def iniciar_juego():
    
    # Definir las tareas que se ejecutarán en hilos separados
    def proceso1_restaurar_acciones():
        restaurar_acciones()

    def proceso2_restaurar_acciones_aliados():
        restaurar_acciones_aliados()

    # Crear hilos para cada tarea
    hilo_acciones = threading.Thread(target=proceso1_restaurar_acciones)
    hilo_acciones_aliados = threading.Thread(target=proceso2_restaurar_acciones_aliados)

    # Iniciar los hilos
    hilo_acciones.start()
    hilo_acciones_aliados.start()

    # Esperar a que ambos hilos terminen
    hilo_acciones.join()
    hilo_acciones_aliados.join()

    # Decidir aleatoriamente quién empieza
    turno_aleatorio = random.choice([0, 1])

    mensaje = ""

    if turno_aleatorio == 0:
        cambiar_turno(0, True)
        cambiar_turno(1, False)
        mensaje = "Según la suerte... ¡Comienzan los Aliados!"
    else:
        cambiar_turno(0, False)
        cambiar_turno(1, True)
        mensaje = "Según la suerte... ¡Comienzan la Potencia del Eje!"
    return str(mensaje)
    
def consultar_accion(valor):
    '''El valor 0 es para atacar y el valor 1 es para defender'''

    filter_criteria = {"codigo": "123456789"}
    # Conectar a la base de datos MongoDB
    client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
    db = client['battleship']
    collection = db['Aliados']

    document = collection.find_one(filter_criteria)

    if not document:
        print("Documento no encontrado.")
        return None
    
    if valor == 0: accion = document.get("atacar", None)
    elif valor == 1: accion = document.get("defender", None)
    else: accion = None

    client.close()
    return accion

def consultar_turno():
    filter_criteria = {"codigo": "123456789"}
    # Conectar a la base de datos MongoDB
    client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
    db = client['battleship']
    collection = db['Aliados']

    document = collection.find_one(filter_criteria)

    if not document:
        print("Documento no encontrado.")
        return None
    
    turno = document.get("turno", None)
    client.close()
    return turno

def cambiar_turno(bando, valor):
    # El bando 0 es Aliados y el bando 1 es Potencia del eje. El valor es booleano

    if bando == 0:
        filter_criteria = {"codigo": "123456789"}
        # Conectar a la base de datos MongoDB
        client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
        db = client['battleship']
        collection = db['Aliados']

        update = {"$set": {"turno": valor}}
        collection.update_one(filter_criteria, update)

        # Restaurar acciones de ataque y defensa
        cambiar_accion(0, True)  # Atacar
        cambiar_accion(1, True)  # Defender

    elif bando == 1:
        filter_criteria = {"codigo": "987654321"}
        # Conectar a la base de datos MongoDB
        client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
        db = client['battleship']
        collection = db['Potencia del eje']

        update = {"$set": {"turno": valor}}
        collection.update_one(filter_criteria, update)

        # Restaurar acciones de ataque y defensa
        cambiar_accion(0, True)  # Atacar
        cambiar_accion(1, True)  # Defender

    else:
        print("Bando no encontrado")

    client.close()


def cambiar_accion(accion, valor):
    # La accion 0 es atacar y la accion 1 es defender. El valor es booleano'''

    if accion == 0:
        filter_criteria = {"codigo": "123456789"}
        # Conectar a la base de datos MongoDB
        client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
        db = client['battleship']
        collection = db['Aliados']

        update = {"$set": {"atacar": valor}}
        collection.update_one(filter_criteria, update)
    elif accion == 1:
        filter_criteria = {"codigo": "123456789"}
        # Conectar a la base de datos MongoDB
        client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
        db = client['battleship']
        collection = db['Aliados']

        update = {"$set": {"defender": valor}}
        collection.update_one(filter_criteria, update)
    else:
        print("Acción no encontrada")

    client.close()

def restaurar_acciones():
    filter_criteria = {"codigo": "987654321"}
    # Conectar a la base de datos MongoDB
    client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
    db = client['battleship']
    collection = db['Potencia del eje']

    update = {"$set": {"atacar": True}}
    collection.update_one(filter_criteria, update)
    update = {"$set": {"defender": True}}
    collection.update_one(filter_criteria, update)

    client.close()

def restaurar_acciones_aliados():
    filter_criteria = {"codigo": "123456789"}
    # Conectar a la base de datos MongoDB
    client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
    db = client['battleship']
    collection = db['Aliados']

    update = {"$set": {"atacar": True}}
    collection.update_one(filter_criteria, update)
    update = {"$set": {"defender": True}}
    collection.update_one(filter_criteria, update)

    client.close()

def update_mongo_document():
    try:
        global data
        filter_criteria = {"codigo": "123456789"}
        # Conectar a la base de datos MongoDB
        client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
        db = client['battleship']
        collection = db['Aliados']

        # Generar el nuevo campo "tablero"
        tablero = [{"coord": k, "state": v} for k, v in data.items()]

        # Actualizar el documento
        collection.update_one(filter_criteria, {"$set": {"tablero": tablero}})

        update = {"$set": {"cantEscanear": 3}}
        collection.update_one(filter_criteria, update)

        update = {"$set": {"atacar": True}}
        collection.update_one(filter_criteria, update)

        update = {"$set": {"defender": True}}
        collection.update_one(filter_criteria, update)

        # Cerrar la conexión
        client.close()
        return True
    
    except Exception as e:
        print(f'Error: {e}')
        return False

def atacar_coordenada(coord):
    turno = consultar_turno()
    validar = consultar_accion(0)

    if turno is None and validar is None:
        return "Error al consultar el turno"
    
    if not turno:
        return "No es tu turno"
    
    if not validar:
        return "No puedes atacar"

    filter_criteria = {"codigo": "987654321"}
    # Conectar a la base de datos MongoDB
    client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
    db = client['battleship']
    collection = db['Potencia del eje']

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

    cambiar_accion(0, False)
    return str(message)

def defender_coordenada(coord):
    turno = consultar_turno()
    validar = consultar_accion(1)

    if turno is None and validar is None:
        return "Error al consultar el turno"
    
    if not turno:
        return "No es tu turno"
    
    if not validar:
        return "No puedes defender"

    filter_criteria = {"codigo": "123456789"}
    # Conectar a la base de datos MongoDB
    client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
    db = client['battleship']
    collection = db['Aliados']

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
    
    cambiar_accion(1, False)
    return str(message)

def obtener_coordenadas_3x3(coord):
    letra, numero = coord[0], int(coord[1:])
    letras = [chr(ord(letra) + i) for i in range(-1, 2)]
    numeros = [numero + i for i in range(-1, 2)]
    coordenadas = [f"{l}{n}" for l in letras for n in numeros]
    return coordenadas

def escanear_coordenada(coord):
    filter_criteria_PdE = {"codigo": "987654321"}
    filter_criteria_Aliados = {"codigo": "123456789"}
    # Conectar a la base de datos MongoDB
    client = MongoClient('mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/')
    db = client['battleship']
    collection_PdE = db['Potencia del eje']
    collection_Aliados = db['Aliados']

    document_Aliados = collection_Aliados.find_one(filter_criteria_Aliados)
    document_Pde = collection_PdE.find_one(filter_criteria_PdE)

    if not document_Aliados and not document_Pde:
        print("Documento no encontrado.")
        return None
    
    cant_escanear = document_Aliados.get("cantEscanear", 0)
    if cant_escanear <= 0:
        return "No puedes escanear más. Se acabaron las oportunidades."
    
    tablero = document_Pde.get("tablero", [])
    coordenadas_a_escanear = obtener_coordenadas_3x3(coord)
    barcos_encontrados = False

    for item in tablero:
        if item["coord"] in coordenadas_a_escanear and item["state"] in [1, 2]:
            barcos_encontrados = True
            break

    # Descontar una oportunidad de escanear
    cant_escanear -= 1
    collection_Aliados.update_one(filter_criteria_Aliados, {"$set": {"cantEscanear": cant_escanear}})

    if barcos_encontrados:
        message = "Se han detectado barcos en el área escaneada."
    else:
        message = "No se han detectado barcos en el área escaneada."
    
    return str(message)

class GUI:
    def __init__(self, ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address, port))

        self.Window = tk.Tk()
        self.Window.withdraw()

        self.login = tk.Toplevel()
        self.login.title("Sala")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=350, bg="#34495E")

        self.pls = tk.Label(self.login, 
                            text="Ingrese a la sala", 
                            justify=tk.CENTER,
                            font="Helvetica 14 bold",
                            bg="#34495E",  
                            fg="#ECF0F1")  
        self.pls.place(relwidth=1, rely=0.07)

        self.userLabelName = tk.Label(self.login, text="Nombre bando: ", font="Helvetica 11", bg="#34495E", fg="#ECF0F1")
        self.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)

        self.userEntryName = tk.Entry(self.login, font="Helvetica 12", bg="#ECF0F1", fg="#2C3E50")
        self.userEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.4, rely=0.30)
        self.userEntryName.insert(0, "Aliados")
        self.userEntryName.focus()

        self.go = tk.Button(self.login, 
                            text="Continuar", 
                            font="Helvetica 12 bold", 
                            bg="#2ECC71",  
                            fg="#ECF0F1",  
                            command = lambda: self.goAhead(self.userEntryName.get(), "0"))
        self.go.place(relwidth=0.3, relheight=0.1, relx=0.35, rely=0.62)

        self.Window.mainloop()

    def goAhead(self, username, room_id=0):
        self.name = username
        self.server.send(str.encode(username))
        time.sleep(0.1)
        self.server.send(str.encode(room_id))

        self.login.destroy()
        self.layout()

        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def layout(self):
        self.Window.deiconify()
        self.Window.title("Ventana de comandos")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#17202A")

        self.chatBoxHead = tk.Label(self.Window, 
                                    bg = "#17202A", 
                                    fg = "#EAECEE", 
                                    text = self.name, 
                                    font = "Helvetica 11 bold", 
                                    pady = 5)
        self.chatBoxHead.place(relwidth=1)

        self.line = tk.Label(self.Window, width = 450, bg = "#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textCons = tk.Text(self.Window, 
                                width=20, 
                                height=2, 
                                bg="#17202A", 
                                fg="#EAECEE", 
                                font="Helvetica 11", 
                                padx=5, 
                                pady=5)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = tk.Label(self.Window, bg="#ABB2B9", height=80)
        self.labelBottom.place(relwidth=1, rely=0.8)

        self.entryMsg = tk.Entry(self.labelBottom, 
                                bg = "#2C3E50", 
                                fg = "#EAECEE", 
                                font = "Helvetica 11")
        self.entryMsg.place(relwidth=0.74, 
                            relheight=0.03, 
                            rely=0.008, 
                            relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg = tk.Button(self.labelBottom, 
                                text = "Enviar", 
                                font = "Helvetica 10 bold", 
                                width = 20, 
                                bg = "#ABB2B9", 
                                command = lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77, 
                            rely=0.008, 
                            relheight=0.03, 
                            relwidth=0.22)

        self.textCons.config(cursor = "arrow")
        scrollbar = tk.Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=tk.DISABLED)
        #self.sendButton("Eres parte de los aliados!")

    def sendButton(self, msg):
        self.textCons.config(state=tk.DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, tk.END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    def sendMessage(self):
        self.textCons.config(state=tk.DISABLED)
        while True:
            self.server.send(str.encode(self.msg))
            break

    def receive(self):
        while True:
            try:
                message = self.server.recv(1024).decode('utf-8')

                if message == 'NICKNAME':
                    self.server.send(self.name.encode('utf-8'))
                else:
                    self.textCons.config(state=tk.NORMAL)
                    self.textCons.insert(tk.END, message + "\n\n")
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.see(tk.END)

            except:
                print("An error occurred!")
                self.server.close()
                break


    def sendMessage(self):
        self.textCons.config(state=tk.DISABLED) 
        mensaje = analisis(self.msg)
        
        if not mensaje is None:
            self.server.send(mensaje.encode())
            self.textCons.config(state = tk.NORMAL)
            self.textCons.insert(tk.END, 
                             "<You> " + mensaje + "\n\n") 
            #print(self.msg)
            self.textCons.config(state = tk.DISABLED) 
            self.textCons.see(tk.END)
        
            


if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345
    g = GUI(ip_address, port)
