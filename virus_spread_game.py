import PyQt6
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import Qt
import sys
import random

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

def can_virus_spread(x: int, y: int) -> bool:
    """
    Function to check if the virus can spread further in the matrix.

    Args:
        x (int): number of columns in the matrix
        y (int): number of rows in the matrix

    Returns:
        bool: True if the virus can spread, False otherwise
    """
    for row in range(y):
        for col in range(x):
            if matriz_botones[row][col].valor == 1:  
                
                if row > 0 and matriz_botones[row - 1][col].valor == 0:  
                    return True
                if row < y - 1 and matriz_botones[row + 1][col].valor == 0:  
                    return True
                if col > 0 and matriz_botones[row][col - 1].valor == 0:
                    return True
                if col < x - 1 and matriz_botones[row][col + 1].valor == 0:
                    return True
    for row in matriz_botones:
                for boton in row:
                    boton.setEnabled(False)
    return False
    
def spread_virus(x: int, y: int) -> None: 
    """
    Function that spreads the virus in the matrix.
    Randomly selects a position that already has a virus (valor == 1),
    then spreads it in a random direction if the neighboring block is empty (valor == 0).

    Args:
        x (int): number of columns in the matrix
        y (int): number of rows in the matrix
    """
        
    while can_virus_spread(x, y) == True:
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
    
            
def turn(x: int, y: int) -> None:
    """Function that alternates turns between the user and the computer.
    The user places a barrier, and the computer spreads the virus.

    Args:
        x (int): coordinate x of the button
        y (int): coordinate y of the button
    """
    if matriz_botones[y][x].valor == 0:  # Ensure the user clicks on an empty cell
        generate_barrier(x, y)  # User's turn: place a barrier
        spread_virus(len(matriz_botones[0]), len(matriz_botones))  # Computer's turn: spread the virus
    
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
            boton.clicked.connect(lambda _, px=x, py=y: turn( px, py)) 
            grid_layout.addWidget(boton, x, y) 
            fila.append(boton)
        matriz_botones.append(fila)
    generate_virus(x, y, level)

game_matrix(10, 10)

ventana.setLayout(grid_layout) 
ventana.show()
sys.exit(app.exec())