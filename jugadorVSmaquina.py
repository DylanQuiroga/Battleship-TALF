from tablero import BoardGUI
from ponerBarcos import colocarBarcos
from Random_pos_ship import posicionarShip_Machine
import tkinter as tk
from lexer_parser import analisis
from data_operaciones import comprobar_ganador

def partida():
    colocarBarcos()
    posicionarShip_Machine()
    
    tablero_maquina = "machine_board.csv"
    tablero_jugador = "tablero.csv"

    # Crear la ventana principal y la interfaz de juego
    window = tk.Tk()
    window.title("Batalla Naval")
    window.resizable(False, False)
    
    class PartidaGUI:
        def __init__(self, master):
            self.master = master
            self.board_gui = BoardGUI(self.master, tablero_jugador)
            self.button_obtener_comando = tk.Button(self.master, text="Obtener Comando", command=self.jugador_ataca)
            self.button_obtener_comando.pack()
            self.jugador_turno = True
            self.juego_en_curso = True

        def jugador_ataca(self):
            if self.juego_en_curso and self.jugador_turno:
                comando = self.board_gui.process_command()
                resultado = analisis(comando)  # Asumiendo que tienes un método para atacar el tablero de la máquina
                print(resultado)
                if comprobar_ganador(tablero_maquina):
                    self.juego_en_curso = False
                    print("Ganaste")
                    self.mostrar_mensaje("¡Felicidades! Has ganado.")
                else:
                    self.jugador_turno = False
                    print("turno de la maquina")
                    self.mostrar_mensaje("Turno de la maquina")
                    self.maquina_ataca()
        
        def maquina_ataca(self):
            if self.juego_en_curso and not self.jugador_turno:
                comando = self.board_gui.generar_comando_ataque()  # Asumiendo que tienes un método para generar el ataque de la máquina
                resultado = self.board_gui.atacar_jugador(comando)  # Asumiendo que tienes un método para atacar el tablero del jugador
                self.board_gui.mostrar_resultado_ataque(resultado)  # Mostrar el resultado del ataque

                if self.verificar_ganador(self.board_gui.board, self.board_gui.load_board_from_csv(tablero_jugador)):
                    self.juego_en_curso = False
                    self.mostrar_mensaje("La máquina ha ganado. Mejor suerte la próxima vez.")
                else:
                    self.jugador_turno = True

        
       

        def mostrar_mensaje(self, mensaje):
            tk.messagebox.showinfo("Resultado", mensaje)

    partida_gui = PartidaGUI(window)
    
    # Iniciar la GUI
    window.mainloop()

if __name__ == "__main__":
    partida()
