from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox
from models import get_available_cars, update_car_status

class UserWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Пользователь")
        self.resize(400, 300)
        self.user = user

        layout = QVBoxLayout()
        self.list = QListWidget()
        self.load_cars()

        self.book_btn = QPushButton("Забронировать")
        self.book_btn.clicked.connect(self.book)

        layout.addWidget(QLabel(f"Добро пожаловать в каршэринг, {user['phone']}"))
        layout.addWidget(QLabel("Доступные машины:"))
        layout.addWidget(self.list)
        layout.addWidget(self.book_btn)
        self.setLayout(layout)

    def load_cars(self):
        self.list.clear()
        self.cars = get_available_cars()
        for car in self.cars:
            self.list.addItem(f"{car['model']} — {car['pricePerMinute']} ₽/мин")

    def book(self):
        i = self.list.currentRow()
        if i >= 0:
            car_id = self.cars[i]['carId']
            update_car_status(car_id, 'inUse')
            QMessageBox.information(self, "Готово", "Машина забронирована")
            self.load_cars()