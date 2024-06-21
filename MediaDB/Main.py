# main_window.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from Palette import dark_palette
from Query import QueryWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        #self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Add buttons to open different windows
        self.query_access_button = QPushButton("Open Query Window")
        self.query_access_button.clicked.connect(self.open_query_window)
        
        # Set font for the button
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.query_access_button.setFont(font)
        
        layout.addWidget(self.query_access_button)

    def open_query_window(self):
        self.query_window = QueryWindow()
        self.query_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setPalette(dark_palette())

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
