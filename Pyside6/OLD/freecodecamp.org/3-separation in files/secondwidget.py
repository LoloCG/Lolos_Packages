from PySide6.QtWidgets import QMainWindow, QPushButton

class widgetholder1(QMainWindow): # it calls from QMainWindow, thus having access to methods located in it, such as window titles
    def __init__(self):
        super().__init__()

        self.setWindowTitle("button holder")
        button = QPushButton("button")
        self.setCentralWidget(button) # Tells the window (QMainWindow) to use the button as the central widget 

        