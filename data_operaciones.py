import csv
import random

def load_board(file_name):
    board = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            board.append(row)
    return board

def atacar_coordenada(coord, csv):
    tablero = load_board(csv)
    estado_nuevo = '-1'
    
    for item in tablero:
        if item["Coord"] == coord:
            coord_state = item["State"]
            tablero = leer_csv(csv)
            if coord_state == '-1':
                message = "Ya habías impactado este barco antes"
            elif coord_state == '0':
                message = "Agua"
            elif coord_state == '1':         
                tablero_modificado = modificar_csv(tablero, coord, estado_nuevo)
                escribir_csv(csv, tablero_modificado)
                message = "¡Impacto en un barco!" 
            elif coord_state == '2':
                if random.random() < 0.5:
                    tablero_modificado = modificar_csv(tablero, coord, estado_nuevo)
                    escribir_csv(csv, tablero_modificado)
                    message = "¡Impacto en un barco en posición de defenza!"
                else:
                    estado_nuevo = '1'
                    tablero_modificado = modificar_csv(tablero, coord, estado_nuevo)
                    escribir_csv(csv, tablero_modificado)
                    message = "El misil ha fallado"
    
    return str(message)
 
def defender_coordenada(coord, csv):
    tablero = load_board(csv)
    estado_nuevo = '2'
    
    for item in tablero:
        if item["Coord"] == coord:
            coord_state = item["State"]
            tablero = leer_csv(csv)
            if coord_state == '-1':
                message = "Parte de barco destruida, no se puede defender"
            elif coord_state == '0':
                message = "No hay barcos en esta coordenada"
            elif coord_state == '1':         
                tablero_modificado = modificar_csv(tablero, coord, estado_nuevo)
                escribir_csv(csv, tablero_modificado)
                message = "Barco en posición de defensa"
            elif coord_state == '2':
                message = "Este barco ya está en posición de defensa"
    
    return str(message)
                         
def comprobar_ganador(csv):
    tablero = load_board(csv)
    if verificar_tablaVacia(tablero) is True:
        return True
    else:
        return False
    
def verificar_tablaVacia(tablero):
    for estado in tablero:
        if estado["State"] in ["1", "2"]:
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

def generar_comando_maquina(tablero_jugador_csv, tablero_maquina_csv):
    # Leer el tablero del jugador desde el archivo CSV
    tablero_jugador = load_board(tablero_jugador_csv)
    tablero_maquina = load_board(tablero_maquina_csv)
    
    # Obtener todas las posibles coordenadas (A1 a J10)
    coordenadas = [f"{letra}{numero}" for letra in 'ABCDEFGHIJ' for numero in range(1, 11)]
    
    # Filtrar las coordenadas que no han sido atacadas aún
    coordenadasAtaques_disponibles = []
    for item in tablero_jugador:
        if item["State"] != '-1':
            coordenadasAtaques_disponibles.append(item["Coord"])
    
    # Filtrar las coordenadas que se pueden defender
    coordenadasDefender_disponibles = []
    for item in tablero_maquina:
        if item["State"] == '1':
            coordenadasDefender_disponibles.append(item["Coord"])
    
    # Si no hay coordenadas disponibles, se puede manejar según la lógica de tu juego
    if not coordenadasAtaques_disponibles:
        return None
    
    # Elegir una coordenada aleatoria entre las disponibles
    coordenada = random.choice(coordenadasAtaques_disponibles)
    
    acciones = ['Atacar', 'Defender']
    accion = random.choice(acciones)
    
    if accion == 'Atacar':
        # Elegir una coordenada aleatoria entre las disponibles para atacar
        coordenada = random.choice(coordenadasAtaques_disponibles)
    elif accion == 'Defender':
        # Elegir una coordenada aleatoria entre las disponibles para defender
        coordenada = random.choice(coordenadasDefender_disponibles)
    
    comando = f"{accion} {coordenada}"
    
    return comando

