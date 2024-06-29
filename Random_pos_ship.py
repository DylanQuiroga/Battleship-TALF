import csv
import random

class MachineBoard:
    def __init__(self):
        self.board_size = 10
        self.board = [['O' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.ships = [5, 4, 3, 3, 2]  # Tamaños de los barcos

    def is_valid_position(self, ship, row, col, orientation):
        if orientation == 'horizontal':
            if col + ship > self.board_size:
                return False
            for i in range(ship):
                if self.board[row][col + i] != 'O':
                    return False
        else:  # vertical
            if row + ship > self.board_size:
                return False
            for i in range(ship):
                if self.board[row + i][col] != 'O':
                    return False
        return True

    def place_ship(self, ship):
        while True:
            orientation = random.choice(['horizontal', 'vertical'])
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)

            if self.is_valid_position(ship, row, col, orientation):
                if orientation == 'horizontal':
                    for i in range(ship):
                        self.board[row][col + i] = 'S'
                else:
                    for i in range(ship):
                        self.board[row + i][col] = 'S'
                break

    def place_all_ships(self):
        for ship in self.ships:
            self.place_ship(ship)

    def save_board_to_csv(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Coord', 'State'])
            for row in range(self.board_size):
                for col in range(self.board_size):
                    coord = chr(65 + col) + str(row + 1)
                    state = 1 if self.board[row][col] == 'S' else 0
                    writer.writerow([coord, state])

def posicionarShip_Machine():
    machine_board = MachineBoard()
    machine_board.place_all_ships()
    machine_board.save_board_to_csv('machine_board.csv')

