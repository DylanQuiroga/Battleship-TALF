import os
import subprocess
import tkinter as tk
from tkinter import PhotoImage, ttk
from PIL import Image, ImageTk
from jugadorVSmaquina import partida
from subprocess import Popen, PIPE
import webbrowser
from ponerBarcos import colocarBarcos


class BattleshipMenu:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Battleship Menu")
        self.window.geometry("400x450")
        self.window.resizable(False,False)
        self.center_window(self.window)
        
    
        # Load and resize the cover image
        cover_image = Image.open("imagenes/battleship2.jpg")
        cover_image = cover_image.resize((300, 150), Image.LANCZOS)
        self.cover_photo = ImageTk.PhotoImage(cover_image)

        # Create a label to display the cover image
        cover_label = tk.Label(self.window, image=self.cover_photo)
        cover_label.pack(pady=10)

        label = tk.Label(self.window, text="Menu", font=("Helvetica", 16))
        label.pack(pady=10)

        self.play_machine_button = tk.Button(self.window, text="Jugar contra maquina", command=self.play_machine)
        self.play_machine_button.pack(pady=10)

        self.play_player_button = tk.Button(self.window, text="Jugar contra jugador", command=self.play_player)
        self.play_player_button.pack(pady=10)

        self.generate_board_button = tk.Button(self.window, text="Generar tablero", command=self.open_poner_barcos)
        self.generate_board_button.pack(pady=10)

        self.instructions_button = tk.Button(self.window, text="Instrucciones", command=self.show_instructions)
        self.instructions_button.pack(pady=10)

        self.quit_button = tk.Button(self.window, text="Salir", command=self.window.quit)
        self.quit_button.pack(pady=10)

        # Initialize instructions_window to None
        self.instructions_window = None
    
    def center_window(self, window):
        window_width = 400
        window_height = 450

        # Obtiene las dimensiones de la pantalla
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calcula la posición x y y para centrar la ventana
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        # Establece la geometría de la ventana con la posición calculada
        window.geometry(f'{window_width}x{window_height}+{position_x}+{position_y}')

    def play_machine(self):
        self.window.destroy() 
        
        partida()
             
        print("Playing against the machine.")

    def show_instructions(self):
        if self.instructions_window is None:
            archivo_html = "instrucciones/index.html"
            abs_path = os.path.abspath(archivo_html)
            webbrowser.open(f"file://{abs_path}")

    def close_instructions(self):
        if self.instructions_window is not None:
            self.instructions_window.destroy()
            self.instructions_window = None

    def open_poner_barcos(self):
        # Asegúrate de que el path al script sea correcto. Puede necesitar ajustes.
        colocarBarcos()

    def play_player(self):
        # Crear una nueva ventana
        self.player_choice_window = tk.Toplevel(self.window)
        self.player_choice_window.title("Bandos")
        
        
        # Configurar el tamaño de la ventana si es necesario
        self.player_choice_window.geometry('500x300')
        
        self.center_window(self.player_choice_window)
        title_label = tk.Label(self.player_choice_window, text="Escoge tu bando", font=("Arial", 20))
        title_label.pack(pady=(10,20))

        allies_image_raw = PhotoImage(file="instrucciones/imagenes/Aliados.png")
        axis_image_raw = PhotoImage(file="instrucciones/imagenes/Potencia del eje.png")

        # Ajustar el tamaño de las imágenes (ejemplo: zoom x2, subsample x4)
        self.allies_image = allies_image_raw.zoom(2, 2).subsample(20, 20)
        self.axis_image = axis_image_raw.zoom(2, 2).subsample(20, 20)

        self.buttons_frame = tk.Frame(self.player_choice_window)
        self.buttons_frame.pack()

        allies_frame = tk.Frame(self.buttons_frame)
        allies_frame.pack(side=tk.LEFT, padx=(10,20))

        # Crear y empaquetar la etiqueta "Aliados" en el Frame de los Aliados, asegurándose de que esté en la parte superior
        allies_label = tk.Label(allies_frame, text="Aliados", font=("Arial", 10))
        allies_label.pack(side=tk.TOP)

        # Crear y empaquetar el botón de los Aliados en el mismo Frame, debajo de la etiqueta
        allies_button = tk.Button(allies_frame, image=self.allies_image, command=self.choose_allies)
        allies_button.pack(side=tk.TOP)

        # Repetir el proceso para las Potencias del Eje

        # Crear un Frame para las Potencias del Eje
        axis_frame = tk.Frame(self.buttons_frame)
        axis_frame.pack(side=tk.LEFT, padx=(10,20))

        # Crear y empaquetar la etiqueta "Potencias del Eje" en el Frame de las Potencias del Eje, asegurándose de que esté en la parte superior
        axis_label = tk.Label(axis_frame, text="Potencias del Eje", font=("Arial", 10))
        axis_label.pack(side=tk.TOP)

        # Crear y empaquetar el botón de las Potencias del Eje en el mismo Frame, debajo de la etiqueta
        axis_button = tk.Button(axis_frame, image=self.axis_image, command=self.choose_axis)
        axis_button.pack(side=tk.TOP)
    
    
    def choose_allies(self):
        # Cerrar la ventana actual
        self.player_choice_window.destroy()
        # Abrir la ventana de los Aliados
        subprocess.Popen(['python', 'client_GUI_Aliados.py'])
    
    def choose_axis(self):
        # Cerrar la ventana actual
        self.player_choice_window.destroy()
        # Abrir la ventana de las Potencias del Eje
        subprocess.Popen(['python', 'client_GUI_PdE.py'])

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    battleship_menu = BattleshipMenu()
    battleship_menu.run()
