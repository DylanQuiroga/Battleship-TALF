from tablero import BoardGUI
from ponerBarcos import colocarBarcos
from Random_pos_ship import posicionarShip_Machine
import tkinter as tk
from tkinter import messagebox  
from lexer_parser import analisis , analisisMaquina
from data_operaciones import comprobar_ganador, generar_comando_maquina
import random


class PartidaGUI:
    
    def __init__(self, master, tablero_jugador, tablero_maquina):
        self.master = master
        self.tablero_jugador = tablero_jugador
        self.tablero_maquina = tablero_maquina
        self.board_gui = BoardGUI(self.master, self.tablero_jugador)
        self.button_obtener_comando = tk.Button(self.master, text="Obtener Comando", command=self.jugador_ataca)
        self.button_obtener_comando.pack()
        self.jugador_turno = True
        self.juego_en_curso = True

    def jugador_ataca(self):
        if self.juego_en_curso and self.jugador_turno:
            comando = self.board_gui.process_command()
            resultado = analisis(comando, self.tablero_maquina)  # Asumiendo que tienes un método para atacar el tablero de la máquina
            print(resultado)
            
            if comprobar_ganador(self.tablero_maquina):
                self.juego_en_curso = False
                print("Ganaste")
                self.mostrar_mensaje("¡Felicidades! Has ganado.")
            else:
                self.jugador_turno = False
                print("Turno de la máquina")
                self.mostrar_mensaje("Turno de la máquina")
                self.maquina_ataca()
    
    def maquina_ataca(self):
        if self.juego_en_curso and not self.jugador_turno:
            comandoMaquina = generar_comando_maquina(self.tablero_jugador)  # Asumiendo que tienes un método para generar el ataque de la máquina
            resultado = analisisMaquina(comandoMaquina, self.tablero_jugador)  # Mostrar el resultado del ataque
            if comprobar_ganador(self.tablero_jugador):
                self.juego_en_curso = False
                print("Perdiste")
                self.mostrar_mensaje("La máquina ha ganado. Mejor suerte la próxima vez.")
            else:
                self.jugador_turno = True
                self.mostrar_mensaje("Tu turno")

    def mostrar_mensaje(self, mensaje):
        messagebox.showinfo("Resultado", mensaje)



def partida():
    colocarBarcos()
    posicionarShip_Machine()
    
    tablero_maquina = "machine_board.csv"
    tablero_jugador = "tablero.csv"

    # Crear la ventana principal y la interfaz de juego
    window = tk.Tk()
    window.title("Batalla Naval")
    window.resizable(False, False)
    
    partida_gui = PartidaGUI(window, tablero_jugador, tablero_maquina)
    
    # Iniciar la GUI
    window.mainloop()

if __name__ == "__main__":
    partida()