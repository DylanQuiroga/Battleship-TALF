import csv
import random
from pymongo import MongoClient

data = {}

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
        # Implementación de la actualización del documento MongoDB
        pass
    except Exception as e:
        print(f'Error: {e}')
        return False

def atacar_coordenada(coord):
    # Implementación de la lógica de ataque
    pass

def defender_coordenada(coord):
    # Implementación de la lógica de defensa
    pass
