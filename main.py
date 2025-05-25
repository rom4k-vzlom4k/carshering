import sys
from PyQt6.QtWidgets import QApplication, QLabel

class MainWindow(QApplication, QLabel):
    app = QApplication(sys.argv)
    label = QLabel("<font color=red size=40>Hello World!</font>")
    label.show()
    app.exec()