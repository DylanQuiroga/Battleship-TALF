import tkinter as tk
import csv
import random

# Crear un diccionario para almacenar el estado de los botones
button_states = {}
buttons = {}
ships = []

def on_button_click(button, coord):
    # Cambiar el color del botón y guardar su estado
    if button.cget('bg') == 'yellow':
        button.config(bg='SystemButtonFace')  # Cambiar a color predeterminado
        button_states[coord] = 0
    else:
        button.config(bg='yellow')
        button_states[coord] = 1

def save_and_exit():
    # Guardar los estados de los botones en un archivo CSV
    with open('tablero.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Coord', 'State'])
        for coord, state in button_states.items():
            writer.writerow([coord, state])
    # Cerrar la aplicación
    window.destroy()

def generate_ship(size):
    while True:
        orientation = random.choice(['horizontal', 'vertical'])
        if orientation == 'horizontal':
            start_row = random.randint(0, 9)
            start_col = random.randint(0, 10 - size)
            ship_coords = [(chr(65 + start_col + i) + str(start_row + 1)) for i in range(size)]
        else:  # vertical
            start_row = random.randint(0, 10 - size)
            start_col = random.randint(0, 9)
            ship_coords = [(chr(65 + start_col) + str(start_row + 1 + i)) for i in range(size)]
        
        if not any(set(ship_coords) & set(ship) for ship in ships):  # no overlap
            # check for adjacency
            adjacent_cells = []
            for coord in ship_coords:
                col, row = ord(coord[0]) - 65, int(coord[1:]) - 1
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= col + i < 10 and 0 <= row + j < 10:
                            adjacent_cell = chr(65 + col + i) + str(row + j + 1)
                            adjacent_cells.append(adjacent_cell)
            if not any(set(adjacent_cells) & set(ship) for ship in ships):
                return ship_coords

def clear_board():
    for button in buttons.values():
        button.config(bg='SystemButtonFace')
    for coord in button_states.keys():
        button_states[coord] = 0
    ships.clear()

def place_ships():
    clear_board()
    for size in [5, 4, 3, 2, 2]:  # ship sizes
        ship_coords = generate_ship(size)
        ships.append(ship_coords)
        for coord in ship_coords:
            button = buttons[coord]
            button.config(bg='yellow')
            button_states[coord] = 1

window = tk.Tk()
for i in range(10):
    for j in range(10):
        coord = chr(65 + j) + str(i + 1)  # Coordenada del botón (A1, A2, ..., J10)
        button = tk.Button(window, height=2, width=4)
        button.grid(row=i, column=j)
        button.config(command=lambda button=button, coord=coord: on_button_click(button, coord))
        # Inicializar el estado del botón
        button_states[coord] = 0
        buttons[coord] = button

# Crear el botón "Guardar"
save_button = tk.Button(window, text="Guardar", command=save_and_exit)
save_button.grid(row=10, column=0, columnspan=10)

# Crear el botón "Aleatorio"
random_button = tk.Button(window, text="Aleatorio", command=place_ships)
random_button.grid(row=11, column=0, columnspan=10)

# Crear el botón "Limpiar"
clear_button = tk.Button(window, text="Limpiar", command=clear_board)
clear_button.grid(row=12, column=0, columnspan=10)

window.mainloop()
