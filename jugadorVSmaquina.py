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
            comando_valido = False
            while not comando_valido:
                comando = self.board_gui.process_command()
                resultado = analisis(comando, self.tablero_maquina)
                if "error" in resultado.lower():
                    self.mostrar_mensaje("Comando inválido. Inténtalo de nuevo.")
                    self.board_gui.entry.delete(0, tk.END)
                    return  # Salir del método para permitir que el jugador ingrese un nuevo comando
                else:
                    comando_valido = True
                    print(resultado)
                    self.mostrar_mensaje(resultado)
                    self.board_gui.entry.delete(0, tk.END)
                    self.board_gui.board = self.board_gui.load_board_from_csv(self.tablero_jugador)
                    self.board_gui.draw_board()
                    
                    if comprobar_ganador(self.tablero_maquina):
                        self.juego_en_curso = False
                        print("Ganaste")
                        self.mostrar_mensaje("¡Felicidades! Has ganado.")
                        self.master.destroy
                        
                    else:
                        self.jugador_turno = False
                        print("Turno de la máquina")
                        self.mostrar_mensaje("Turno de la máquina")
                        # Desactivar el botón mientras la máquina está atacando
                        self.button_obtener_comando.config(state=tk.DISABLED)
                        self.maquina_ataca()
                        
                        # Volver a activar el botón después de que la máquina ha atacado
                        self.button_obtener_comando.config(state=tk.NORMAL)
        
    def maquina_ataca(self):
        if self.juego_en_curso and not self.jugador_turno:
            comandoMaquina = generar_comando_maquina(self.tablero_jugador, self.tablero_maquina)  
            resultadoMaquina = analisisMaquina(comandoMaquina, self.tablero_jugador)  # Mostrar el resultado del ataque
            print(resultadoMaquina)
            self.board_gui.board = self.board_gui.load_board_from_csv(self.tablero_jugador)
            self.board_gui.draw_board()
            self.mostrar_mensaje(resultadoMaquina)
            if comprobar_ganador(self.tablero_jugador):
                self.juego_en_curso = False
                print("Perdiste")
                self.mostrar_mensaje("La máquina ha ganado. Mejor suerte la próxima vez.")
                self.master.destroy
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
    
    window.mainloop()

if __name__ == "__main__":
    partida()