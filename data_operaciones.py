import csv
import random
from pymongo import MongoClient

data = {}

def load_board(file_name):
    board = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            board.append(row)
    return board

def update_mongo_document():
    try:
        global data
        # Implementación de la actualización del documento MongoDB
        pass
    except Exception as e:
        print(f'Error: {e}')
        return False

def atacar_coordenada(coord):
    archivo_csv = "machine_board.csv"
    tablero_maquina = load_board("machine_board.csv")
    estado_nuevo = '-1'
    
    for item in tablero_maquina:
        if item["Coord"] == coord:
            coord_state = item["State"]
            tablero_maquina = leer_csv(archivo_csv)
            if coord_state == '-1':
                message = "Ya habías impactado este barco antes"
            elif coord_state == '0':
                message = "Agua"
            elif coord_state == '1':         
                tablero_modificado = modificar_csv(tablero_maquina, coord, estado_nuevo)
                escribir_csv(archivo_csv, tablero_modificado)
                message = "¡Impacto en un barco!" 
            elif coord_state == '2':
                if random.random() < 0.5:
                    tablero_modificado = modificar_csv(tablero_maquina, coord, estado_nuevo)
                    escribir_csv(archivo_csv, tablero_modificado)
                    message = "¡Impacto en un barco en posición de defenza!"
                else:
                    estado_nuevo = '1'
                    tablero_modificado = modificar_csv(tablero_maquina, coord, estado_nuevo)
                    escribir_csv(archivo_csv, tablero_modificado)
                    message = "El misil ha fallado"
    
    return str(message)
                         
def comprobar_ganador(csv):
    tablero = load_board(csv)
    if verificar_ganador is True:
        return True
    else:
        return False
    
def verificar_ganador(tablero):
    for estado in tablero.values():
        if estado == '1':
            return False
    return True

def leer_csv(archivo_csv):
    with open(archivo_csv, mode='r', newline='') as archivo:
        lector_csv = csv.DictReader(archivo)
        return list(lector_csv)

# Función para escribir el tablero modificado de vuelta al archivo CSV
def escribir_csv(archivo_csv, tablero):
    with open(archivo_csv, mode='w', newline='') as archivo:
        campos = ['Coord', 'State']
        escritor_csv = csv.DictWriter(archivo, fieldnames=campos)
        escritor_csv.writeheader()
        escritor_csv.writerows(tablero)

# Función para modificar el estado de una coordenada específica en el tablero
def modificar_csv(tablero, coord, nuevo_estado):
    for item in tablero:
        if item["Coord"] == coord:
            item["State"] = nuevo_estado
            break
    return tablero

def defender_coordenada(coord):
    # Implementación de la lógica de defensa
    pass
