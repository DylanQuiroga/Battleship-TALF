import tkinter as tk
from tkinter import Canvas
from pymongo import MongoClient
from PIL import Image, ImageTk
import threading

class BoardGUI:
    def __init__(self, root, mongo_uri):
        self.root = root
        self.root.title("Tablero de los aliados")
        self.root.resizable(width=False, height=False)  # Hacer que la ventana no sea resizable
        self.canvas = Canvas(self.root, width=440, height=440)
        self.canvas.pack()
        self.mongo_uri = mongo_uri
        self.image_empty = self.resize_image(Image.open('imagenes/water.png'))  # Imagen para casillas vacías
        self.image_ship = self.resize_image(Image.open('imagenes/ship1.png'))  # Imagen para barco posicionado
        self.image_defending = self.resize_image(Image.open('imagenes/ship3.png'))  # Imagen para barco en posición de defensa
        self.image_destroyed = self.resize_image(Image.open('imagenes/ship2.png'))  # Imagen para barco destruido
        self.board = {}
        self.update_lock = threading.Lock()  # Bloqueo para evitar actualizaciones simultáneas
        self.draw_board()
        self.update_board()

    def load_board_from_mongodb(self):
        try:
            client = MongoClient(self.mongo_uri)
            db = client['battleship']
            collection = db['Aliados']  # Nombre de la colección en MongoDB

            document = collection.find_one({"codigo": "123456789"})  # Filtro según tus necesidades
            if document:
                tablero = document.get("tablero", [])
                new_board = {}
                for item in tablero:
                    new_board[item["coord"]] = item["state"]
                
                with self.update_lock:
                    self.board = new_board

        except Exception as e:
            print(f'Error al cargar el tablero desde MongoDB: {e}')

        finally:
            client.close()

    def resize_image(self, img):
        cell_size = 40
        return ImageTk.PhotoImage(img.resize((cell_size, cell_size)))

    def draw_board(self):
        self.canvas.delete("all")  # Limpiar el lienzo antes de redibujar
        cell_size = 40
        offset = 20  # Offset para los textos de las filas y columnas

        # Dibujar letras de filas
        for i in range(10):
            self.canvas.create_text(offset // 2, i * cell_size + cell_size // 2 + offset, text=str(i + 1), fill='black', font=('Arial black', 10))

        # Dibujar números de columnas
        for j in range(10):
            self.canvas.create_text(j * cell_size + cell_size // 2 + offset, offset // 2, text=chr(65 + j), fill='black', font=('Arial black', 10))

        # Dibujar el tablero
        with self.update_lock:
            for i in range(10):
                for j in range(10):
                    coord = chr(65 + j) + str(i + 1)
                    x0, y0 = j * cell_size + offset, i * cell_size + offset
                    x1, y1 = x0 + cell_size, y0 + cell_size
                    self.canvas.create_rectangle(x0, y0, x1, y1, outline='black')

                    state = self.board.get(coord, 0)
                    if state == 1:
                        self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.image_ship)
                    elif state == 2:
                        self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.image_defending)
                    elif state == -1:
                        self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.image_destroyed)
                    else:
                        self.canvas.create_rectangle(x0, y0, x1, y1, fill='DodgerBlue2')
                        self.canvas.create_image(x0, y0, anchor=tk.NW, image=self.image_empty)

    def update_board(self):
        self.load_board_from_mongodb()
        self.draw_board()
        self.root.after(2000, self.update_board)  # Actualiza cada 2000 milisegundos (2 segundos)

if __name__ == "__main__":
    mongo_uri = 'mongodb+srv://monkey3:tuperacomolapapaya@basedatosalfacharlie.dwvwxn6.mongodb.net/'  # Tu URI de MongoDB
    root = tk.Tk()
    # pantalla grande root.geometry("440x440+1200+50")
    root.geometry("440x440+480+296")
    board_gui = BoardGUI(root, mongo_uri)
    root.mainloop()
