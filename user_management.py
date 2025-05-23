from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,QApplication, QDialog, QListWidget, QHBoxLayout, QInputDialog)
from PyQt6.QtCore import Qt
import hashlib
import pickle
import os
from virus_spread_game import GameWindow
import save_manager

USUARIOS_FILE = "usuarios.pkl"

class LoadGameDialog(QDialog):
    """A class that allows to continue and delete a saved game

    Args:
        QDialog (object): Allows creating personalized dialogs
    """
    def __init__(self, usuario):
        """Initialize the class with an argument 'usuario'

        Args:
            usuario (str): user's name
        """
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Cargar Partida")
        self.setFixedSize(300, 300)
        layout = QVBoxLayout()

        self.lista = QListWidget()
        self.saves = save_manager.load_user_saves(usuario)
        self.lista.addItems(self.saves.keys())

        btn_layout = QHBoxLayout()
        btn_cargar = QPushButton("Cargar")
        btn_eliminar = QPushButton("Eliminar")

        btn_cargar.clicked.connect(self.cargar)
        btn_eliminar.clicked.connect(self.eliminar)

        btn_layout.addWidget(btn_cargar)
        btn_layout.addWidget(btn_eliminar)

        layout.addWidget(self.lista)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def cargar(self):
        """Continues a saved game select by the user"""
        seleccion = self.lista.currentItem()
        if seleccion:
            nombre = seleccion.text()
            datos = self.saves[nombre]
            self.close()
            self.game = GameWindow(datos['level'])
            self.game.load_game_state(datos)
            self.game.current_user = self.usuario

    def eliminar(self):
        """Allows the user to delete a selected game"""
        seleccion = self.lista.currentItem()
        if seleccion:
            nombre = seleccion.text()
            respuesta = QMessageBox.question(
                self,
                "Eliminar Partida",
                f"¿Estás seguro de que deseas eliminar la partida '{nombre}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if respuesta == QMessageBox.StandardButton.Yes:
                exito = save_manager.delete_game(self.usuario, nombre)
                if exito:
                    fila = self.lista.row(seleccion)
                    self.lista.takeItem(fila)
                    QMessageBox.information(self, "Eliminar Partida", "Partida eliminada correctamente.")
                else:
                    QMessageBox.warning(self, "Eliminar Partida", "No se pudo eliminar la partida.")
class LoginWindow(QWidget):
    """A class that initializes or displays a window to log into the game

    Args:
        QWidget (library): Allows the addition of widgets for better control of the window
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()

        self.label = QLabel("Usuario:")
        self.usuario_input = QLineEdit()

        self.label2 = QLabel("Contraseña:")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Iniciar Sesión")
        self.register_btn = QPushButton("Registrarse")

        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.register)

        layout.addWidget(self.label)
        layout.addWidget(self.usuario_input)
        layout.addWidget(self.label2)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def hash_pass(self, text):
        """This function encrypts the user's password

        Args:
            text (str): The user's password

        Returns:
            encrypt str : returns an encrypted password
        """
        return hashlib.sha256(text.encode()).hexdigest()

    def load_users(self):
        """A function that checks if the user was created previously

        Returns:
            str : if the user was create it returns the user's name, otherwize nothing is returned
        """
        if os.path.exists(USUARIOS_FILE):
            with open(USUARIOS_FILE, 'rb') as f:
                return pickle.load(f)
        return {}

    def save_users(self, users):
        """This function is responsible for creating new users.

        Args:
            users (str): new user 
        """
        with open(USUARIOS_FILE, 'wb') as f:
            pickle.dump(users, f)

    def login(self):
        """This function is responsible to checks if the user was create and checks if the password its correct depending on the user"""
        user = self.usuario_input.text()
        pwd = self.pass_input.text()
        users = self.load_users()

        if user in users and users[user] == self.hash_pass(pwd):
            self.menu_window = MenuWindow(user)
            self.menu_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

    def register(self):
        """This function is responsible for checking if there is another user with the same username and preventing it"""
        user = self.usuario_input.text()
        pwd = self.pass_input.text()
        users = self.load_users()

        if user in users:
            QMessageBox.warning(self, "Error", "Usuario ya registrado")
            return

        users[user] = self.hash_pass(pwd)
        self.save_users(users)
        QMessageBox.information(self, "Registro", "Usuario registrado exitosamente")

class MenuWindow(QWidget):
    """This class displays the main window that contains some functions like 'play', 'load game' and 'logout'

    Args:
        QWidget (library): allows to adding widget for better control of the window
    """
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.current_user = usuario
        self.setWindowTitle("Menú Principal")
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()

        self.label = QLabel(f"Bienvenido {usuario}")

        self.jugar_btn = QPushButton("Jugar")
        self.cargar_btn = QPushButton("Cargar Partida")
        self.logout_btn = QPushButton("Cerrar Sesión")

        self.jugar_btn.clicked.connect(self.jugar)
        self.cargar_btn.clicked.connect(self.cargar_partida)
        self.logout_btn.clicked.connect(self.logout)

        layout.addWidget(self.label)
        layout.addWidget(self.jugar_btn)
        layout.addWidget(self.cargar_btn)
        layout.addWidget(self.logout_btn)

        self.setLayout(layout)

    def jugar(self):
        """Function responsible to display a window with the difficulty of the levels"""
        niveles = ["Fácil", "Medio", "Difícil"]
        nivel, ok = QInputDialog.getItem(self, "Seleccionar Dificultad", "Elige un nivel:", niveles, 0, False)
        if ok and nivel:
            nivel_map = {"Fácil": 1, "Medio": 2, "Difícil": 3}
            nivel_seleccionado = nivel_map[nivel]
            self.game = GameWindow(nivel_seleccionado)
            self.game.current_user = self.usuario
            self.close()

    def cargar_partida(self):
        """Continue a saved game"""
        self.dialog = LoadGameDialog(self.usuario)
        self.dialog.exec()
        self.close()

    def logout(self):
        """Function to log out from the main window"""
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
