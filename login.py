from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from models import login_user
from admin_window import AdminWindow
from user_window import UserWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.resize(300, 150)
        layout = QVBoxLayout()

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Телефон")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Пароль")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.try_login)

        layout.addWidget(QLabel("Телефон:"))
        layout.addWidget(self.phone_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)

    def try_login(self):
        phone = self.phone_input.text()
        password = self.pass_input.text()
        user = login_user(phone, password)
        if user:
            self.close()
            if user.get('isAdmin'):
                self.w = AdminWindow()
            else:
                self.w = UserWindow(user)
            self.w.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль.")