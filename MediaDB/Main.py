import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
)
#from PySide6.QtCore import Qt
from Query import QueryWindow
from Palette import dark_paletteClass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")

        # Create a central widget and set it as the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the main window
        self.layout = QVBoxLayout(central_widget)
        
        # Set dark theme
        self.set_dark_theme()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
