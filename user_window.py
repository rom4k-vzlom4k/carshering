from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox, QHBoxLayout, 
                             QToolButton,QMenu,
                             QDialog, QTableWidget, QTableWidgetItem)
from PyQt6.QtGui import QAction
from models import (
    get_available_cars, create_rental, get_active_rental,
    cancel_rental, get_rental_history
)

class UserWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Пользователь")
        self.resize(600, 400)
        self.user = user
        self.active_rental = None

        self.layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.label = QLabel(f"Добро пожаловать, {user['name']}")

        self.burger_btn = QToolButton()
        self.burger_btn.setText("☰")
        self.burger_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.menu = QMenu()
        self.profile_action = QAction("Профиль")
        self.history_action = QAction("История поездок")
        self.menu.addAction(self.profile_action)
        self.menu.addAction(self.history_action)

        self.burger_btn.setMenu(self.menu)
        self.profile_action.triggered.connect(self.show_profile)
        self.history_action.triggered.connect(self.show_sessionRental)

        top_layout.addWidget(self.label)
        top_layout.addStretch()
        top_layout.addWidget(self.burger_btn)

        self.status_label = QLabel()
        self.list = QListWidget()

        self.book_btn = QPushButton("Забронировать")
        self.cancel_btn = QPushButton("Отменить аренду")
        self.book_btn.clicked.connect(self.book)
        self.cancel_btn.clicked.connect(self.cancel)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.book_btn)
        btn_layout.addWidget(self.cancel_btn)

        self.table = QTableWidget()
        self.table.hide()

        self.layout.addLayout(top_layout)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.list)
        self.layout.addLayout(btn_layout)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.refresh_ui()

    def refresh_ui(self):
        self.list.clear()
        self.active_rental = get_active_rental(self.user['userId'])
        if self.active_rental:
            self.status_label.setText(f"\nвы арендуете: {self.active_rental['model']}")
            self.list.setDisabled(True)
            self.book_btn.setDisabled(True)
            self.cancel_btn.setDisabled(False)
        else:
            self.status_label.setText("\nдоступные машины:")
            self.cars = get_available_cars()
            for car in self.cars:
                self.list.addItem(f"{car['model']} — {car['pricePerMinute']} ₽/мин")
            self.list.setDisabled(False)
            self.book_btn.setDisabled(False if self.cars else True)
            self.cancel_btn.setDisabled(True)
        self.table.hide()

    def book(self):
        i = self.list.currentRow()
        if i >= 0:
            car_id = self.cars[i]['carId']
            create_rental(self.user['userId'], car_id)
            QMessageBox.information(self, "Готово", "Машина забронирована")
            self.refresh_ui()

    def cancel(self):
        if self.active_rental:
            cancel_rental(self.active_rental['sessionId'], self.active_rental['carId'])
            QMessageBox.information(self, "Отмена", "Аренда отменена")
            self.refresh_ui()

    def show_profile(self):
        info = f"Телефон: {self.user['phone']}\nВУ: {self.user['licenseDriver']}"
        QMessageBox.information(self, "Профиль", info)

    def show_sessionRental(self):
        data = get_rental_history(self.user['userId'])
        self.table.setRowCount(len(data))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Авто", "Начало", "Конец", "Статус", "Расстояние (км)", "Стоимость (₽)"])
        for row, rental in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(rental['model']))
            self.table.setItem(row, 1, QTableWidgetItem(str(rental['startTime'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(rental['endTime'] or 'В процессе')))
            self.table.setItem(row, 3, QTableWidgetItem(rental['status']))
            self.table.setItem(row, 4, QTableWidgetItem(str(rental['distance'] or 0)))
            self.table.setItem(row, 5, QTableWidgetItem(str(rental['cost'] or 0)))
        
        self.table.show()

