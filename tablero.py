import tkinter as tk
from tkinter import Canvas, Entry, Button
import csv
from PIL import Image, ImageTk

class BoardGUI:
    def __init__(self, root, csv_file):
        self.root = root
        self.canvas = Canvas(self.root, width=440, height=440)  # Ajustar el tamaño del canvas
        self.canvas.pack()
        self.board = self.load_board_from_csv(csv_file)
        self.image_empty = self.resize_image(Image.open('imagenes/water.png'))  # Imagen para casillas vacías y agua
        self.image_ship = self.resize_image(Image.open('imagenes/ship1.png'))  # Imagen para barco posicionado
        self.image_defending = self.resize_image(Image.open('imagenes/ship3.png'))  # Imagen para barco en posición de defensa
        self.image_destroyed = self.resize_image(Image.open('imagenes/ship2.png'))  # Ruta de la imagen para casillas marcadas
        self.draw_board()
        
         # Crear campo de entrada y botón
        self.entry = Entry(self.root)
        self.entry.pack()

    def load_board_from_csv(self, filename):
        board = {}
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera
            for row in reader:
                coord, state = row
                board[coord] = int(state)
        return board
    
    def resize_image(self, img):
        cell_size = 40
        return ImageTk.PhotoImage(img.resize((cell_size, cell_size)))

    def draw_board(self):
        cell_size = 40
        offset = 20  # Offset para los textos de las filas y columnas

        # Dibujar letras de filas
        for i in range(10):
            self.canvas.create_text(offset // 2, i * cell_size + cell_size // 2 + offset, text=str(i + 1), fill='black', font=('Arial black', 10))

        # Dibujar números de columnas
        for j in range(10):
            self.canvas.create_text(j * cell_size + cell_size // 2 + offset, offset // 2, text=chr(65 + j), fill='black', font=('Arial black', 10))

        # Dibujar el tablero
        for i in range(10):
            for j in range(10):
                coord = chr(65 + j) + str(i + 1)
                x0, y0 = j * cell_size + offset, i * cell_size + offset
                x1, y1 = x0 + cell_size, y0 + cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline='black')
                if self.board.get(coord) == 1:
                    self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.image_ship)
                elif self.board.get(coord) == -1:
                    self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.image_destroyed)
                elif self.board.get(coord) == 2:
                    self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.image_defending)    
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill='DodgerBlue2')

    def process_command(self):
        try:
            command = self.entry.get()
            return command
        except Exception as e:
            print(f"Error al obtener comando: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tablero de Juego")
    csv_file = 'tablero.csv'  # Reemplaza con tu archivo CSV real
    board_gui = BoardGUI(root, csv_file)
    root.mainloop()