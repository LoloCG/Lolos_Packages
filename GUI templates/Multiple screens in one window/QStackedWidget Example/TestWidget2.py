from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class SecondaryWidget2(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Secondary Widget 2")
        layout = QVBoxLayout(self)
        label = QLabel("This is the content of Widget 2")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.back_button = QPushButton("Back to Main Menu")
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.go_back)

    def go_back(self):
        self.main_window.show_main_menu()
