import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nested Layout Example")

        # Create main widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Set up main layout
        self.main_layout = QVBoxLayout(self.main_widget)

        # Set up top layout with labels and line edits
        self.top_layout = QHBoxLayout()
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.age_label = QLabel("Age:")
        self.age_input = QLineEdit()

        self.top_layout.addWidget(self.name_label)
        self.top_layout.addWidget(self.name_input)
        self.top_layout.addWidget(self.age_label)
        self.top_layout.addWidget(self.age_input)

        # Add top layout to main layout
        self.main_layout.addLayout(self.top_layout)

        # Add a submit button
        self.submit_button = QPushButton("Submit")
        self.main_layout.addWidget(self.submit_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
