import PyQt6
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt
import sys
import random
from collections import deque

app = QApplication(sys.argv)
ventana = QWidget()
ventana.setWindowTitle("Virus Spread Game")
ventana.setGeometry(400, 200, 500, 300)

grid_layout = QGridLayout()
matriz_botones = [] 

def messages(i:int)->None:
    """
    Function that shows a message depending on the value of the function called.
    """
    messages = [["Winner", "You win!", QMessageBox.Icon.Information],["Game Over", "Game Over!", QMessageBox.Icon.Critical],["Invalid Move", "You cannot create an isolated island!", QMessageBox.Icon.Warning],["Game Rules", "Welcome to the Virus Spread Game!\n\n""Your goal is to place barriers to prevent the virus from spreading.\n""Click on a button to place a barrier and stop the virus.\n""If you create an isolated island, you lose!\n""Good luck!", QMessageBox.Icon.Information],]
    msg = QMessageBox()
    msg.setWindowTitle(messages[i][0])
    msg.setText(messages[i][1])
    msg.setIcon(messages[i][2])
    msg.exec()

def generate_virus(x:int = None, y:int = None, level:int = 1)->None: 
    """
    Function that generates a virus in the matrix.

    Args:
        x (int): coordinate x of the button
        y (int): coordinate y of the button
    """
    cont = 0
    while cont < level: 
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
    if winner() == True:
        messages(0)
    else:
        messages(1)
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
        if new_virus == 0 and origin_y > 0:  # Up
            if matriz_botones[origin_y - 1][origin_x].valor == 0:
                matriz_botones[origin_y - 1][origin_x].setText("🦠")
                matriz_botones[origin_y - 1][origin_x].valor = 1
                return 
        elif new_virus == 1 and origin_y < y - 1:  # Down
            if matriz_botones[origin_y + 1][origin_x].valor == 0:
                matriz_botones[origin_y + 1][origin_x].setText("🦠")
                matriz_botones[origin_y + 1][origin_x].valor = 1
                return 
        elif new_virus == 2 and origin_x > 0:  # Left
            if matriz_botones[origin_y][origin_x - 1].valor == 0:
                matriz_botones[origin_y][origin_x - 1].setText("🦠")
                matriz_botones[origin_y][origin_x - 1].valor = 1
                return 
        elif new_virus == 3 and origin_x < x - 1:  # Right
            if matriz_botones[origin_y][origin_x + 1].valor == 0:
                matriz_botones[origin_y][origin_x + 1].setText("🦠")
                matriz_botones[origin_y][origin_x + 1].valor = 1
                return 
    
def generate_barrier(x:int, y:int)->None:
    """
    Function that generates a barrier in the matrix clicked by the user.

    Args:
        x (int): coordinate x of the button
        y (int): coordinate y of the button
    """
    if not limit_islands(matriz_botones, x, y):
        return
    matriz_botones[y][x].setText("🧱")
    matriz_botones[y][x].valor = 2
    
def limit_islands(button_matrix, x, y):
    """
    Verifies if the barrier creates an isolated island in the matrix. Then blocks the button.
    If it does, it shows a message and returns False.
    """
    rows = len(button_matrix)
    cols = len(button_matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    button_matrix[y][x].valor = 2  

    def is_island(start_y, start_x):
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        queue = deque([(start_y, start_x)])
        visited[start_y][start_x] = True
        has_border = False

        while queue:
            cy, cx = queue.popleft()
            for dy, dx in directions:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < rows and 0 <= nx < cols:
                    if not visited[ny][nx] and button_matrix[ny][nx].valor == 0:
                        visited[ny][nx] = True
                        queue.append((ny, nx))
                else:
                    has_border = True  
        return not has_border  

    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if 0 <= ny < rows and 0 <= nx < cols:
            if button_matrix[ny][nx].valor == 0:
                if is_island(ny, nx):
                    button_matrix[y][x].valor = 0  
                    messages(2)  
                    return False

    button_matrix[y][x].valor = 0  
    return True
            
def turn(x: int, y: int) -> None:
    """
    Function that alternates turns between the user and the computer.
    The user places a barrier, and the computer spreads the virus.

    Args:
        x (int): coordinate x of the button
        y (int): coordinate y of the button
    """
    if matriz_botones[y][x].valor == 0: 
        generate_barrier(x, y)  
        spread_virus(len(matriz_botones[0]), len(matriz_botones))

def winner()->None:
    """
    Function that checks if the user has won the game.
    If there are no empty spaces left in the matrix, the user wins.
    """
    for row in matriz_botones:
        for boton in row:
            if boton.valor == 0:  
                return True
    return False

def game_matrix(x:int = None, y:int= None, level:int = 1)->None:
    """
    Fuction that creates game's matrix with nxn buttons.

    Args:
        x (int, optional): Number of columns in the matrix. Defaults to None.
        y (int, optional): Number of rows in the matrix. Defaults to None.
        level (int, optional): Difficulty level, while higher its harder. Defaults to 1.
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