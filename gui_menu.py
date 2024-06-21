import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser

class BattleshipMenu:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Battleship Menu")
        self.window.geometry("400x450")
        self.window.resizable(False,False)

        # Load and resize the cover image
        cover_image = Image.open("battleship2.jpg")
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

        self.instructions_button = tk.Button(self.window, text="Instrucciones", command=self.show_instructions)
        self.instructions_button.pack(pady=10)

        self.quit_button = tk.Button(self.window, text="Salir", command=self.window.quit)
        self.quit_button.pack(pady=10)

        # Initialize instructions_window to None
        self.instructions_window = None

    def play_machine(self):
        # Add code to start playing against the machine
        print("Playing against the machine.")

    def play_player(self):
        # Add code to start playing against another player
        print("Playing against another player.")

    def show_instructions(self):
        if self.instructions_window is None:
            archivo_html = "instrucciones/index.html"
            abs_path = os.path.abspath(archivo_html)
            webbrowser.open(f"file://{abs_path}")

    def close_instructions(self):
        if self.instructions_window is not None:
            self.instructions_window.destroy()
            self.instructions_window = None

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    battleship_menu = BattleshipMenu()
    battleship_menu.run()
