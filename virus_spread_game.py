import PyQt6
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import Qt
import random
import sys

app = QApplication(sys.argv)
ventana = QWidget()
ventana.setWindowTitle("Virus Spread Game")
ventana.setGeometry(400, 200, 500, 300)

grid_layout = QGridLayout()
matriz_botones = [] 

def generate_virus(x:int = None, y:int = None, level:int = 1)->None: # x and y receive the size of the matrix
    """Function that generates a virus in the matrix.

    Args:
        x (int): coordinate x of the button
        y (int): coordinate y of the button
    """
    cont = 0
    while cont < level: #Create the amount of viruses in the matrix
        origin_x = random.randint(0, x-1)
        origin_y = random.randint(0, y-1)
        matriz_botones[origin_y][origin_x].setText("🦠")
        matriz_botones[origin_y][origin_x].valor = 1
        cont += 1
    
def spread_virus(x: int, y: int) -> None:
    """
    Function that spreads the virus in the matrix.
    Randomly selects a position that already has a virus (valor == 1),
    then spreads it in a random direction if the neighboring block is empty (valor == 0).

    Args:
        x (int): number of columns in the matrix
        y (int): number of rows in the matrix
    """
    while True:
        origin_x = random.randint(0, x - 1)
        origin_y = random.randint(0, y - 1)

        if matriz_botones[origin_y][origin_x].valor != 1:
            continue

        new_virus = random.randint(0, 3)

        if new_virus == 0 and origin_y > 0:  # Arriba
            if matriz_botones[origin_y - 1][origin_x].valor == 0:
                matriz_botones[origin_y - 1][origin_x].setText("🦠")
                matriz_botones[origin_y - 1][origin_x].valor = 1
                return

        elif new_virus == 1 and origin_y < y - 1:  # Abajo
            if matriz_botones[origin_y + 1][origin_x].valor == 0:
                matriz_botones[origin_y + 1][origin_x].setText("🦠")
                matriz_botones[origin_y + 1][origin_x].valor = 1
                return

        elif new_virus == 2 and origin_x > 0:  # Izquierda
            if matriz_botones[origin_y][origin_x - 1].valor == 0:
                matriz_botones[origin_y][origin_x - 1].setText("🦠")
                matriz_botones[origin_y][origin_x - 1].valor = 1
                return

        elif new_virus == 3 and origin_x < x - 1:  # Derecha
            if matriz_botones[origin_y][origin_x + 1].valor == 0:
                matriz_botones[origin_y][origin_x + 1].setText("🦠")
                matriz_botones[origin_y][origin_x + 1].valor = 1
                return
    
def generate_barrier(x:int, y:int)->None:
    """Function that generates a barrier in the matrix clicked by the user.

    Args:
        x (int): coordinate x of the button
        y (int): coordinate y of the button
    """
    matriz_botones[y][x].setText("🧱")
    matriz_botones[y][x].valor = 2
            
def game_matrix(x:int = None, y:int= None, level:int = 1)->None:
    """Fuction that creates the game matrix with YxX buttons.
    """
    for y in range(10):
        fila= []
        for x in range(10):
            
            boton = QPushButton("⬜") 
            boton.valor = 0
            boton.setFixedSize(50, 50) 
            boton.setStyleSheet("font-size: 40px; border: none; background-color: transparent;")
            boton.clicked.connect(lambda _, px=x, py=y: generate_barrier( px, py)) 
            grid_layout.addWidget(boton, x, y) 
            fila.append(boton)
        matriz_botones.append(fila)
    generate_virus(10, 10, level)
game_matrix()

ventana.setLayout(grid_layout) 
ventana.show()
sys.exit(app.exec())