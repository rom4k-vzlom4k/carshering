from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QLineEdit, QMessageBox
from models import get_all_cars, add_car, delete_car

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Админ")
        self.resize(400, 300)

        layout = QVBoxLayout()
        self.list = QListWidget()
        self.load_cars()

        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Модель")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Цена за минуту")
        self.loc_input = QLineEdit()
        self.loc_input.setPlaceholderText("ID локации")

        self.add_btn = QPushButton("Добавить машину")
        self.del_btn = QPushButton("Удалить выбранную")

        self.add_btn.clicked.connect(self.add_car)
        self.del_btn.clicked.connect(self.delete_car)

        layout.addWidget(QLabel("Список машин:"))
        layout.addWidget(self.list)
        layout.addWidget(self.model_input)
        layout.addWidget(self.price_input)
        layout.addWidget(self.loc_input)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.del_btn)
        self.setLayout(layout)

    def load_cars(self):
        self.list.clear()
        self.cars = get_all_cars()
        for car in self.cars:
            self.list.addItem(f"{car['carId']}: {car['model']} — {car['status']}")

    def add_car(self):
        try:
            add_car(self.model_input.text(), float(self.price_input.text()), int(self.loc_input.text()))
            self.load_cars()
        except:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить машину")

    def delete_car(self):
        i = self.list.currentRow()
        if i >= 0:
            car_id = self.cars[i]['carId']
            delete_car(car_id)
            self.load_cars()