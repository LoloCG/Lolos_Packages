# From Learn Python GUI Development for Desktop – PySide6 and Qt Tutorial
# https://www.youtube.com/watch?v=Z1N9JzNax2k


''' # Version 1: Code without mainwidget class
    # It doesnt use a class to hold the widget, thus is less scalable and maintainable
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys 

app = QApplication(sys.argv) # it is a command line argument

window = QMainWindow()
window.setWindowTitle("MainWindow App")

button = QPushButton()
button.setText("button")

window.setCentralWidget(button)

window.show()
app.exec()
'''
    #Version 2: Code with mainwidget class
