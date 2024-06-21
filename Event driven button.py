import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QPushButton, QLabel


class SecondaryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secondary Window")
        
        # Create a label to display in the secondary window
        layout = QVBoxLayout()
        label = QLabel("This is the secondary window")
        layout.addWidget(label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Event driven buttons")

        # Create a central widget and set it as the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create a vertical layout
        self.layout = QVBoxLayout(central_widget)

        # create and add the buttons
        self.TerminalButton = QPushButton("Terminal print")
        self.layout.addWidget(self.TerminalButton)

        self.PopupButton = QPushButton("Open Secondary Window")
        self.layout.addWidget(self.PopupButton)

       # Connect the buttons click events to whatever it should be connected
        self.TerminalButton.clicked.connect(self.TerminalPrint)

        self.PopupButton.clicked.connect(self.open_secondary_window)

        # Store the reference to the secondary window
        self.secondary_window = None
        
    def TerminalPrint(self):
        print("Button was clicked!")

    def open_secondary_window(self):
        # Create an instance of SecondaryWindow if it doesn't already exist
        if self.secondary_window is None:
            self.secondary_window = SecondaryWindow() 
        
        # Show the secondary window
        self.secondary_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())