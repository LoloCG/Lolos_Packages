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
    # uses a class to hold the main windows and all the widgets inside
    # it can still be separated further into more files (3-)
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys 

class mainwidget(QMainWindow):  # We create a class, inheriting from QMainWindow
    def __init__(self): # The constructor
        super().__init__() 

        #the same stuff in the version 1
        self.setWindowTitle("MainWindow App")
        button = QPushButton("button")
        self.setCentralWidget(button)
        
app = QApplication(sys.argv) # We set application object
window = mainwidget() # we create an instance of the class mainwidget
window.show()
app.exec()


