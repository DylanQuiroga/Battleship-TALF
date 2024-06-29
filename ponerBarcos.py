import tkinter as tk
import csv
import random
from tkinter import messagebox


class Board:
    def __init__(self):
        self.button_states = {}
        self.ships = []
        self.buttons = {}
        self.ship_counts = {4: 0, 3: 0, 2: 0, 1: 0}
        self.max_ships = {4: 1, 3: 2, 2: 1, 1: 4}

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
        self.ship_counts = {4: 0, 3: 0, 2: 0, 1: 0}

    def place_ships(self):
        self.clear_board()
        for size in [4, 3, 3, 2, 1, 1, 1, 1]:  # Actualizar tamaños de barcos según los requisitos
            ship_coords = self.generate_ship(size)
            if ship_coords:  # Verificar si se generó el barco correctamente
                self.ships.append(ship_coords)
                for coord in ship_coords:
                    button = self.buttons[coord]
                    button.config(bg='yellow')
                    self.button_states[coord] = 1
                self.ship_counts[size] += 1
            else:
                print(f"No se pudo colocar un barco de tamaño {size}. Intentando de nuevo.")
                self.place_ships()  # Intentar colocar los barcos de nuevo si falla
                break

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
        self.create_ship_tracker()

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

        clear_button = tk.Button(button_frame, text="Limpiar", command=self.clear_board_and_update)
        clear_button.pack(side=tk.LEFT, padx=5)

    def create_ship_tracker(self):
        self.ship_tracker_frame = tk.Frame(self.root)
        self.ship_tracker_frame.grid(row=12, column=0, columnspan=10, pady=10)
        self.ship_tracker_label = tk.Label(self.ship_tracker_frame, text=self.get_ship_tracker_text(), justify=tk.LEFT)
        self.ship_tracker_label.pack()

    def get_ship_tracker_text(self):
        return f"""
        Portaviones (4 casillas): {self.board.max_ships[4] - self.board.ship_counts[4]}
        Acorazado (3 casillas): {self.board.max_ships[3] - self.board.ship_counts[3]}
        Destructor (2 casillas): {self.board.max_ships[2] - self.board.ship_counts[2]}
        Fragata (1 casilla): {self.board.max_ships[1] - self.board.ship_counts[1]}
        """

    def update_ship_tracker(self):
        self.ship_tracker_label.config(text=self.get_ship_tracker_text())

    def clear_board_and_update(self):
        self.board.clear_board()
        self.update_ship_tracker()

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
            messagebox.showwarning("Advertencia", "¡Las casillas marcadas no forman barcos válidos o exceden el límite permitido!")
            button.config(bg='SystemButtonFace')
            self.board.button_states[coord] = 0

        self.update_ship_tracker()
    
    def valid_ships(self, marked_cells):
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
        new_ship_counts = {4: 0, 3: 0, 2: 0, 1: 0}
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
                if len(current_ship) not in [1, 2, 3, 4] or not is_linear(current_ship):
                    return False
                
                new_ship_counts[len(current_ship)] += 1
                if new_ship_counts[len(current_ship)] > self.board.max_ships[len(current_ship)]:
                    return False
        
        self.board.ship_counts = new_ship_counts
        return True

    def save_board(self):
        self.board.save_board_state('tablero.csv')
        self.root.destroy()

    def place_random_ships(self):
        self.board.place_ships()
        self.update_ship_tracker()

def colocarBarcos():
    window = tk.Tk()
    window.title("Batalla Naval")
    window.resizable(False, False)

    board = Board()
    gui = GUI(window, board)

    window.mainloop()


