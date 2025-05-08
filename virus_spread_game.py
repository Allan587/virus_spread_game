from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox
from PyQt6.QtGui import QGuiApplication 
from PyQt6.QtCore import Qt
import sys
import random
from collections import deque
import user_management as user_mng

app = QApplication(sys.argv)
ventana = QWidget()
ventana.setWindowTitle("Virus Spread Game")
ventana.resize(500, 300)
ventana.move(QGuiApplication.primaryScreen().availableGeometry().center() - ventana.rect().center())
grid_layout = QGridLayout()
matriz_botones = [] 

def messages(i: int) -> None:
    """
    Function that shows a message box with a title and text.
    The message box icon is determined by the index provided for examople:
    0 = Winner, 1 = Loser, 2 = Invalid Move, 3 = Game Rules.
    """
    msg_data = {
        0: ("Winner", "You win!", QMessageBox.Icon.Information),
        1: ("Game Over", "You lose!", QMessageBox.Icon.Critical),
        2: ("Invalid Move", "You cannot create an isolated island!", QMessageBox.Icon.Warning),
        3: ("Game Rules","Welcome to the Virus Spread Game!\n\nYour goal is to place barriers to prevent the virus from spreading.\nClick on a button to place a barrier and stop the virus.\nIf you create an isolated island, you lose your turn!\nGood luck!",QMessageBox.Icon.Information),
    }
    title, text, icon = msg_data.get(i, ("Error", "Unknown message", QMessageBox.Icon.Warning))
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)
    msg.exec()

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
        origin_x = random.randint(0, x - 1); origin_y = random.randint(0, y - 1)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if matriz_botones[origin_y][origin_x].valor != 1:
            continue
        
        def add_virus(x:int, y:int)->None:
            """
            Function that adds a virus to the matrix at the given coordinates.

            Args:
                x (int): position of the column in the matrix
                y (int): position of the row in the matrix
            """
            if matriz_botones[y][x].valor == 0:
                matriz_botones[y][x].setText("🦠")
                matriz_botones[y][x].valor = 1
                
        new_virus = random.randint(0, len(directions) - 1)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
        dy, dx = directions[new_virus]
        ny, nx = origin_y + dy, origin_x + dx

        if 0 <= ny < y and 0 <= nx < x and matriz_botones[ny][nx].valor == 0:
            add_virus(nx, ny)
            return

def limit_islands(m:list, x:int, y:int)->bool:
    """
    Function that checks if the user is creating an isolated island.

    Args:
        m list: matrix of buttons
        x int: coordinate x of the button or matrix column
        y int: coordinate y of the button or matrix row

    Returns:
       bool : True if the user is not creating an isolated island, False otherwise.
    """
    rows, col = len(m), len(m[0])
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    if m[y][x].valor != 0:
        return True  

    m[y][x].valor = 2
    visited = [[False] * col for _ in range(rows)]

    def bfs():
        """
        Breadth-First Search (BFS) to find all reachable cells from the edges.
        If any cell is not accessible, it means that an attempt is being made to create an isolated island
        """
        queue = []
    
        for i in range(rows):
            for j in range(col):
                if (i == 0 or i == rows-1 or j == 0 or j == col-1) and m[i][j].valor == 0:
                    queue.append((i, j))
                    visited[i][j] = True

        while queue:
            cy, cx = queue.pop(0)
            for dy, dx in dirs:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < rows and 0 <= nx < col and not visited[ny][nx]:
                    if m[ny][nx].valor == 0:  
                        visited[ny][nx] = True
                        queue.append((ny, nx))
                        
    bfs()
    for i in range(rows):
        for j in range(col):
            if m[i][j].valor == 0 and not visited[i][j]:
                m[y][x].valor = 0 
                messages(2)  
                return False
            
    m[y][x].valor = 0
    return True

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
            boton.clicked.connect(lambda _, px=x,py=y: turn( px, py)) 
            grid_layout.addWidget(boton, x, y) 
            fila.append(boton)
        matriz_botones.append(fila)
    generate_virus(x, y, level)

ventana.setLayout(grid_layout) 
ventana.show()
sys.exit(app.exec())

if __name__ == "__main__":
    game_matrix(10, 10, 1) 
