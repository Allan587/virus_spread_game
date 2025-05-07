import json
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt
from hashlib import sha256
import virus_spread_game as game

USERS_FILE = "usuarios.json"

# ---------------- Funciones auxiliares ---------------- #
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def hash_password(password):
    return sha256(password.encode()).hexdigest()

# ---------------- Ventanas ---------------- #
class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de sesión")
        self.setGeometry(100, 100, 300, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Iniciar sesión")
        self.register_button = QPushButton("Registrarse")

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

        layout.addWidget(QLabel("Bienvenido al juego"))
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        users = load_users()
        user = self.user_input.text()
        password = hash_password(self.pass_input.text())

        if user in users and users[user] == password:
            self.hide()
            self.menu_window = MainMenuWindow()
            self.menu_window.show()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

    def register(self):
        users = load_users()
        user = self.user_input.text()
        password = hash_password(self.pass_input.text())

        if user in users:
            QMessageBox.warning(self, "Error", "El usuario ya existe")
        else:
            users[user] = password
            save_users(users)
            QMessageBox.information(self, "Registro", "Usuario registrado con éxito")

class MainMenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 300, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.play_button = QPushButton("Jugar")
        self.load_button = QPushButton("Cargar Juego")
        self.logout_button = QPushButton("Cerrar sesión")

        self.play_button.clicked.connect(self.open_difficulty_selection)
        self.logout_button.clicked.connect(self.logout)

        layout.addWidget(self.play_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def open_difficulty_selection(self):
        self.hide()
        self.difficulty_window = DifficultyWindow(self)
        self.difficulty_window.show()

    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

class DifficultyWindow(QWidget):
    def __init__(self, parent_menu):
        super().__init__()
        self.parent_menu = parent_menu
        self.setWindowTitle("Seleccionar Dificultad")
        self.setGeometry(100, 100, 300, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        easy_btn = QPushButton("Fácil")
        medium_btn = QPushButton("Medio")
        hard_btn = QPushButton("Difícil")
        back_btn = QPushButton("Volver")

        easy_btn.clicked.connect(lambda: self.start_game("facil"))
        medium_btn.clicked.connect(lambda: self.start_game("medio"))
        hard_btn.clicked.connect(lambda: self.start_game("dificil"))
        back_btn.clicked.connect(self.go_back)

        layout.addWidget(easy_btn)
        layout.addWidget(medium_btn)
        layout.addWidget(hard_btn)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def start_game(self, dificultad):
        self.close()
        game.matriz_botones.clear()
        game.iniciar_juego()
        game.definir_dificultad(dificultad)

    def go_back(self):
        self.close()
        self.parent_menu.show()

# ---------------- Inicio del programa ---------------- #
if __name__ == "__main__":
    app = QApplication([])
    login_window = LoginWindow()
    login_window.show()
    app.exec()


def selected_mode(x:int=None, y:int=None)->None:
    matrix_modes = [] #Se define con los botones, lo botones estaran contenidos en matrix_modes

    modes= []

    if 0 == y and 0 == x: #Modo facil
        import virus_spread_game as game
        level = 1
]
        game.game_matrix()
