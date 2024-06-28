# Widgets are the basic components
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout

class RockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("poopoo")

        button1 = QPushButton("button1")
        button1.clicked.connect(self.button1_clicked)
        button2 = QPushButton("button2")
        button2.clicked.connect(self.button2_clicked)

        # A layout is required to add the button into the widget
        button_layout = QVBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)

        self.setLayout(button_layout)

    def button1_clicked(self):
            print("1 pressed")

    def button2_clicked(self):
            print("2 pressed")


    