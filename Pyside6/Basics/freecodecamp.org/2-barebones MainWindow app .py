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
