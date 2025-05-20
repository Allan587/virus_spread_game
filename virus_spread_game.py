from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QMessageBox, QInputDialog
from PyQt6.QtGui import QGuiApplication, QCloseEvent
import random
import save_manager

game_modes = {
    1: {"matrix": 10, "virus_spread": 1, "bot_moves": 1},
    2: {"matrix": 11, "virus_spread": 2, "bot_moves": 2},
    3: {"matrix": 12, "virus_spread": 4, "bot_moves": 2},
}

class GameWindow(QWidget):
    def __init__(self, level,saved_state=None):
        super().__init__()
        self.level = level
        self.matriz_botones = []
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.current_user = None

        self.setWindowTitle("Virus Spread Game")
        self.resize(500, 300)
        self.move(QGuiApplication.primaryScreen().availableGeometry().center() - self.rect().center())

        if saved_state:
            self.load_game_state(saved_state)  # CAMBIO: Cargar estado guardado si existe
        else:
            self.setup_game()
        self.show()
    
    def save_game_prompt(self):
        if not hasattr(self, 'current_user'):
            self.messages(2)
            return
        slot, ok = QInputDialog.getText(self, "Guardar Partida", "Nombre para esta partida:")
        if ok and slot:
            state = self.get_game_state()
            success, msg = save_manager.save_game(self.current_user, slot, state)
            QMessageBox.information(self, "Guardar Partida", msg)

    def closeEvent(self, event: QCloseEvent):
        if not self.current_user:
            event.accept()
            return

        reply = QMessageBox.question(
            self,
            "Guardar partida",
            "¿Deseas guardar la partida antes de salir?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
        )

        if reply == QMessageBox.StandardButton.Yes:
            slot, ok = QInputDialog.getText(self, "Guardar Partida", "Nombre para esta partida:")
            if ok and slot:
                state = self.get_game_state()
                success, msg = save_manager.save_game(self.current_user, slot, state)
                QMessageBox.information(self, "Guardar Partida", msg)
                event.accept()
            else:
                event.ignore()
        elif reply == QMessageBox.StandardButton.No:
            event.accept()
        else:
            event.ignore()

    def messages(self, i: int):
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

    def setup_game(self):
        self.messages(3)
        size = game_modes[self.level]["matrix"]
        for y in range(size):
            fila = []
            for x in range(size):
                boton = QPushButton("⬜")
                boton.valor = 0
                boton.setFixedSize(50, 50)
                boton.setStyleSheet("font-size: 40px; border: none; background-color: transparent;")
                boton.clicked.connect(lambda _, px=x, py=y: self.turn(px, py))
                self.grid_layout.addWidget(boton, x, y)
                fila.append(boton)
            self.matriz_botones.append(fila)
        self.generate_virus(size, size)

    def winner(self):
        for row in self.matriz_botones:
            for boton in row:
                if boton.valor == 0:
                    return True
        return False

    def can_virus_spread(self, x, y):
        for row in range(y):
            for col in range(x):
                if self.matriz_botones[row][col].valor == 1:
                    if row > 0 and self.matriz_botones[row - 1][col].valor == 0:
                        return True
                    if row < y - 1 and self.matriz_botones[row + 1][col].valor == 0:
                        return True
                    if col > 0 and self.matriz_botones[row][col - 1].valor == 0:
                        return True
                    if col < x - 1 and self.matriz_botones[row][col + 1].valor == 0:
                        return True
        for row in self.matriz_botones:
            for boton in row:
                boton.setEnabled(False)
        self.messages(0 if self.winner() else 1)
        return False

    def spread_virus(self):
        size = len(self.matriz_botones)
        virus = game_modes[self.level]["bot_moves"]
        spread_count = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while spread_count < virus:
            if not self.can_virus_spread(size, size):
                break
            ox, oy = random.randint(0, size - 1), random.randint(0, size - 1)
            if self.matriz_botones[oy][ox].valor != 1:
                continue
            random.shuffle(directions)
            for dy, dx in directions:
                ny, nx = oy + dy, ox + dx
                if 0 <= ny < size and 0 <= nx < size and self.matriz_botones[ny][nx].valor == 0:
                    self.matriz_botones[ny][nx].setText("🦠")
                    self.matriz_botones[ny][nx].valor = 1
                    spread_count += 1
                    break

    def limit_islands(self, x, y):
        rows, cols = len(self.matriz_botones), len(self.matriz_botones[0])
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        if self.matriz_botones[y][x].valor != 0:
            return True

        self.matriz_botones[y][x].valor = 2

        visited = [[False]*cols for _ in range(rows)]
        queue = []

        for i in range(rows):
            for j in range(cols):
                if (i == 0 or i == rows - 1 or j == 0 or j == cols - 1) and \
                   self.matriz_botones[i][j].valor in [0, 1]:
                    queue.append((i, j))
                    visited[i][j] = True

        while queue:
            cy, cx = queue.pop(0)
            for dy, dx in dirs:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < rows and 0 <= nx < cols and not visited[ny][nx]:
                    if self.matriz_botones[ny][nx].valor in [0, 1]:
                        visited[ny][nx] = True
                        queue.append((ny, nx))

        for i in range(rows):
            for j in range(cols):
                if self.matriz_botones[i][j].valor == 0 and not visited[i][j]:
                    self.matriz_botones[y][x].valor = 0  
                    self.messages(2)
                    return False

        self.matriz_botones[y][x].valor = 0
        return True

    def generate_barrier(self, x, y):
        
        if not self.limit_islands(x, y):
            return
        self.matriz_botones[y][x].setText("🧱")
        self.matriz_botones[y][x].valor = 2

    def turn(self, x, y):
        if self.matriz_botones[y][x].valor == 0:
            self.generate_barrier(x, y)
            self.spread_virus()

    def generate_virus(self, x, y):
        count = 0
        gen = game_modes[self.level]["virus_spread"]
        while count < gen:
            ox, oy = random.randint(0, x-1), random.randint(0, y-1)
            if self.matriz_botones[oy][ox].valor == 0:
                self.matriz_botones[oy][ox].setText("🦠")
                self.matriz_botones[oy][ox].valor = 1
                count += 1
                
    def get_game_state(self):
        state = {
            'level': self.level,
            'matrix': [[btn.valor for btn in row] for row in self.matriz_botones]
        }
        return state
    def load_game_state(self, saved_state):
        matrix = saved_state['matrix']
        size = len(matrix)
        for y in range(size):
            fila = []
            for x in range(size):
                boton = QPushButton()
                valor = matrix[y][x]
                boton.valor = valor
                if valor == 0:
                    boton.setText("⬜")
                elif valor == 1:
                    boton.setText("🦠")
                elif valor == 2:
                    boton.setText("🧱")
                boton.setFixedSize(50, 50)
                boton.setStyleSheet("font-size: 40px; border: none; background-color: transparent;")
                boton.clicked.connect(lambda _, px=x, py=y: self.turn(px, py))
                self.grid_layout.addWidget(boton, x, y)
                fila.append(boton)
            self.matriz_botones.append(fila)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = GameWindow(1)
    sys.exit(app.exec())
