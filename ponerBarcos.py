import tkinter as tk
import csv
import random
from tkinter import messagebox

class Board:
    def __init__(self):
        self.button_states = {}
        self.ships = []
        self.buttons = {}

    def generate_ship(self, size):
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
            
            if not any(set(ship_coords) & set(ship) for ship in self.ships):  # no overlap
                # check for adjacency
                adjacent_cells = []
                for coord in ship_coords:
                    col, row = ord(coord[0]) - 65, int(coord[1:]) - 1
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if 0 <= col + i < 10 and 0 <= row + j < 10:
                                adjacent_cell = chr(65 + col + i) + str(row + j + 1)
                                adjacent_cells.append(adjacent_cell)
                if not any(set(adjacent_cells) & set(ship) for ship in self.ships):
                    return ship_coords

    def clear_board(self):
        for button in self.buttons.values():
            button.config(bg='SystemButtonFace')
        for coord in self.button_states.keys():
            self.button_states[coord] = 0
        self.ships.clear()

    def place_ships(self):
        self.clear_board()
        for size in [3, 3, 2, 2, 1, 1, 1, 1]:  # ship sizes
            ship_coords = self.generate_ship(size)
            self.ships.append(ship_coords)
            for coord in ship_coords:
                button = self.buttons[coord]
                button.config(bg='yellow')
                self.button_states[coord] = 1

    def save_board_state(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Coord', 'State'])
            for coord, state in self.button_states.items():
                writer.writerow([coord, state])

class GUI:
    def __init__(self, root, board):
        self.root = root
        self.board = board
        self.create_board_buttons()
        self.create_buttons()

    def create_board_buttons(self):
        for i in range(10):
            for j in range(10):
                coord = chr(65 + j) + str(i + 1)
                button_text = chr(65 + j) + str(i + 1)  # Coordenada como texto del botón
                button = tk.Button(self.root, text=button_text, height=2, width=4)
                button.grid(row=i, column=j)
                button.config(command=lambda button=button, coord=coord: self.on_button_click(button, coord))
                self.board.button_states[coord] = 0
                self.board.buttons[coord] = button

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=11, column=0, columnspan=10, pady=10)

        save_button = tk.Button(button_frame, text="Guardar", command=self.save_board)
        save_button.pack(side=tk.LEFT, padx=5)

        random_button = tk.Button(button_frame, text="Aleatorio", command=self.place_random_ships)
        random_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(button_frame, text="Limpiar", command=self.board.clear_board)
        clear_button.pack(side=tk.LEFT, padx=5)

    def on_button_click(self, button, coord):
        if button.cget('bg') == 'yellow':
            button.config(bg='SystemButtonFace')  # Cambiar a color predeterminado
            self.board.button_states[coord] = 0
        else:
            button.config(bg='yellow')
            self.board.button_states[coord] = 1
            
        # Validar la cantidad de casillas marcadas y la secuencia
        marked_cells = [coord for coord, state in self.board.button_states.items() if state == 1]
        if not self.valid_ships(marked_cells):
            messagebox.showwarning("Advertencia", "¡Las casillas marcadas no forman barcos válidos!")
            button.config(bg='SystemButtonFace')
            self.board.button_states[coord] = 0
    
    def valid_ships(self, marked_cells):
        #funcion para validar si las celdas marcadas estan en vertical y horizontal
        def is_linear(cells):
            rows = sorted(int(cell[1:]) for cell in cells)
            cols = sorted(ord(cell[0]) for cell in cells)
            return (all(row == rows[0] for row in rows) and all(cols[i] - cols[i-1] == 1 for i in range(1, len(cols)))) or \
                   (all(col == cols[0] for col in cols) and all(rows[i] - rows[i-1] == 1 for i in range(1, len(rows))))

        def get_neighbors(coord):
            col, row = ord(coord[0]), int(coord[1:])
            neighbors = [
                chr(col - 1) + str(row), chr(col + 1) + str(row),
                chr(col) + str(row - 1), chr(col) + str(row + 1)
            ]
            return [n for n in neighbors if n in marked_cells]

        visited = set()
        for cell in marked_cells:
            if cell not in visited:
                stack = [cell]
                current_ship = []
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        current_ship.append(current)
                        stack.extend(get_neighbors(current))
                if len(current_ship) not in [1, 2, 3] or not is_linear(current_ship):
                    return False
            
        return True

    def save_board(self):
        self.board.save_board_state('tablero.csv')
        self.root.destroy()

    def place_random_ships(self):
        self.board.place_ships()

def main():
    window = tk.Tk()
    window.title("Batalla Naval")
    window.resizable(False, False)

    board = Board()
    gui = GUI(window, board)

    window.mainloop()

if __name__ == "__main__":
    main()
