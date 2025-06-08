from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox, QHBoxLayout, 
                             QToolButton,QMenu,
                             QDialog, QTableWidget, QTableWidgetItem)
from PyQt6.QtGui import QAction
from models import get_available_cars, update_car_status, get_rental_history

class UserWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Пользователь")
        self.resize(600, 400)
        self.user = user
        self.userId = user['userId']

        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        
        menu_btn = QToolButton()
        menu_btn.setText("☰")

        menu_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        
        menu = QMenu(self)
        profile_action = QAction("Профиль", self)
        profile_action.triggered.connect(self.show_profile)
        menu.addAction(profile_action)

        session_action = QAction("История", self)
        session_action.triggered.connect(self.show_sessionRental)
        menu.addAction(session_action)
        
        menu_btn.setMenu(menu)
        
        header_layout.addWidget(menu_btn)
        header_layout.addWidget(QLabel(f"Добро пожаловать, {user['phone']}"))
        header_layout.addStretch() 
        
        main_layout.addLayout(header_layout)
        
        self.list = QListWidget()
        self.load_cars()
        
        self.book_btn = QPushButton("Забронировать")
        self.book_btn.clicked.connect(self.book)
        
        main_layout.addWidget(QLabel("Доступные машины:"))
        main_layout.addWidget(self.list)
        main_layout.addWidget(self.book_btn)
        
        self.setLayout(main_layout)

    def show_profile(self):
        QMessageBox.information(self, "Профиль", 
                               f"Телефон: {self.user['phone']}\n"
                               f"Номер вод. удостоверения: {self.user.get('licenseDriver', 'не указана')}")
        
    def show_sessionRental(self):
        try:
            history = get_rental_history(self.userId)
            
            if not history:
                QMessageBox.information(self, "История аренд", "Еще нет завершенных аренд")
                return
                
            dialog = QDialog(self)
            dialog.setWindowTitle("История аренд")
            dialog.resize(800, 400)
            
            layout = QVBoxLayout()
            
            table = QTableWidget()
            table.setColumnCount(6)
            table.setHorizontalHeaderLabels([
                "ID сессии", 
                "Начало аренды", 
                "Окончание аренды", 
                "Пройдено (км)", 
                "Стоимость (₽)", 
                "Автомобиль"
            ])
            
            table.setRowCount(len(history))
            for row, session in enumerate(history):
                table.setItem(row, 0, QTableWidgetItem(str(session['sessionId'])))
                table.setItem(row, 1, QTableWidgetItem(str(session['startTime'])))  
                table.setItem(row, 2, QTableWidgetItem(
                    str(session['endTime']) if session['endTime'] else "В процессе"
                ))
                table.setItem(row, 3, QTableWidgetItem(str(session['distance'])))
                table.setItem(row, 4, QTableWidgetItem(str(session['cost'])))
                table.setItem(row, 5, QTableWidgetItem(session['model']))
            
            table.resizeColumnsToContents()
            table.setAlternatingRowColors(True)
            
            layout.addWidget(table)
            dialog.setLayout(layout)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить историю: {str(e)}")


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