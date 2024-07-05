import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QApplication, QMainWindow, 
    QPushButton, QVBoxLayout, QLabel, QWidget
    )
    # QApplication is required for the main python file.
    # QMainWindow only for the main window that will contain future widgets. 
        # The class can be separated further into another file.
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):  # We create a class, inheriting from QMainWindow
    def __init__(self): # The constructor
        super().__init__() 

        self.setWindowTitle("MainWindow App")

        central_widget = QWidget(self)  # Create a central widget that will contain other widgets
        self.setCentralWidget(central_widget)  # Set the central widget
        layout = QVBoxLayout(central_widget) # Create a vertical layout for the central widget

        # We create the the label and button
        title_label = QLabel("Test")
        button = QPushButton("button")

        # Adjust the label to the center
        title_label.setAlignment(Qt.AlignCenter)

        # Add widgets to the layout of the central widget
        layout.addWidget(title_label)
        layout.addWidget(button)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()  
