from PySide6.QtWidgets import QApplication, QPushButton

def button1_clicked(data):
    print("button 1 pressed")
    print("Checked: ", data)

app = QApplication()
button = QPushButton("Button")
# this makes the button checkable, which is not by default.
    # if doing so, we can add data as seen above to show the state of the button
button.setCheckable(True) 

# The name of the variable (button), the signal that we want to respond to (clicked), and call the connect method that specifies the function called in parenthesis
    # other signals are pressed, released, toggled...
    # some allow more arguments such as "checked"
button.clicked.connect(button1_clicked)


button.show()
app.exec()