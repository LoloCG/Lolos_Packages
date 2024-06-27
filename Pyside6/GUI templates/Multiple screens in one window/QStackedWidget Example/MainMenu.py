# This opens a single window, from where 2 other screens can be accessed back and forth
# Allows not requiting to open new windows

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QVBoxLayout, QPushButton, QLabel, QStackedWidget
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stacked Widget Example")

        # Initialize QStackedWidget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create main menu widget
        self.main_menu_widget = QWidget()
        self.stack.addWidget(self.main_menu_widget)
        main_menu_layout = QVBoxLayout(self.main_menu_widget)
 
        # Create the buttons and add them to widget
        self.Widget1_Button = QPushButton("Widget 1")
        main_menu_layout.addWidget(self.Widget1_Button)
        self.Widget1_Button.clicked.connect(self.show_widget1)
        
        self.Widget2_Button = QPushButton("Widget 2")
        main_menu_layout.addWidget(self.Widget2_Button)
        self.Widget2_Button.clicked.connect(self.show_widget2)

        # Import secondary widgets
        from TestWidget1 import SecondaryWidget1
        from TestWidget2 import SecondaryWidget2

        # Create secondary widgets
        self.secondary_widget1 = SecondaryWidget1(self)
        self.secondary_widget2 = SecondaryWidget2(self)

        # Add secondary widgets to the stack
        self.stack.addWidget(self.secondary_widget1)
        self.stack.addWidget(self.secondary_widget2)

    def show_main_menu(self):
        self.stack.setCurrentWidget(self.main_menu_widget)

    def show_widget1(self):
        self.stack.setCurrentWidget(self.secondary_widget1)

    def show_widget2(self):
        self.stack.setCurrentWidget(self.secondary_widget2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
