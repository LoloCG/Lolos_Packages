import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dynamic Loading Example")

        # Initialize QStackedWidget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create main menu widget
        self.main_menu_widget = QWidget()
        self.stack.addWidget(self.main_menu_widget)
        main_menu_layout = QVBoxLayout(self.main_menu_widget)

        # Add buttons to main menu
        self.Widget1_Button = QPushButton("Widget 1")
        main_menu_layout.addWidget(self.Widget1_Button)
        self.Widget1_Button.clicked.connect(self.show_widget1)
        
        self.Widget2_Button = QPushButton("Widget 2")
        main_menu_layout.addWidget(self.Widget2_Button)
        self.Widget2_Button.clicked.connect(self.show_widget2)

        # Variable to keep track of dynamically created widgets
        self.current_widget = None

    def show_main_menu(self):
        # Remove current widget if it exists
        if self.current_widget:
            self.stack.removeWidget(self.current_widget)
            self.current_widget.deleteLater()
            self.current_widget = None
        # Show the main menu widget
        self.stack.setCurrentWidget(self.main_menu_widget)

    def show_widget1(self):
        from TestWidget1 import SecondaryWidget1  # Import dynamically
        self.current_widget = SecondaryWidget1(self)
        self.stack.addWidget(self.current_widget)
        self.stack.setCurrentWidget(self.current_widget)

    def show_widget2(self):
        from TestWidget2 import SecondaryWidget2  # Import dynamically
        self.current_widget = SecondaryWidget2(self)
        self.stack.addWidget(self.current_widget)
        self.stack.setCurrentWidget(self.current_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
