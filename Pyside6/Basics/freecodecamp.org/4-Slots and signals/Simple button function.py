from PySide6.QtWidgets import QApplication, QPushButton

def button1_clicked():
    print("button 1 pressed")

app = QApplication()
button = QPushButton("press for 1")

# The name of the variable (button), the signal that we want to respond to (clicked), and call the connect method that specifies the function called in parenthesis
button.clicked.connect(button1_clicked)

button.show()
app.exec()