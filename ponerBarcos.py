import tkinter as tk
import csv
import random

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
        for size in [5, 4, 3, 3, 2]:  # ship sizes
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
                button = tk.Button(self.root, height=2, width=4)
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
