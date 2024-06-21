import sys
import sqlite3
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QPushButton, QLabel, QLineEdit, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("---Starting---")
        self.setWindowTitle("Event driven buttons")

        # Create a central widget and set it as the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create a vertical layout
        self.layout = QVBoxLayout(central_widget)

        self.DBTest1_label = QLabel("input1:")
        self.DBTest1_input = QLineEdit()
        
        self.DBTest2_label = QLabel("input2:")
        self.DBTest2_input = QLineEdit()

        self.Add2DB_Button = QPushButton("Add to db")

        self.layout.addWidget(self.DBTest1_label)
        self.layout.addWidget(self.DBTest1_input)
        self.layout.addWidget(self.DBTest2_label)
        self.layout.addWidget(self.DBTest2_input)
        self.layout.addWidget(self.Add2DB_Button)
        self.Add2DB_Button.clicked.connect(self.Add2DB_function)

        # Setup the database
        self.setup_database()

    def setup_database(self):
        # Connect to the SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('SQLite_test_table.db')
        self.cursor = self.conn.cursor()

        # Check if the test_table already exists
        self.cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name='test_table';
        ''')
        table_exists = self.cursor.fetchone()

        if not table_exists:
            print("Database created.")

        # Create the test_table table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input1 TEXT NOT NULL,
                input2 TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def Add2DB_function(self):
        input1 = self.DBTest1_input.text()
        input2 = self.DBTest2_input.text()

        # Check if any input field is empty
        if not input1 or not input2:
            # Display an error message box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("All fields are required.")
            msg.setWindowTitle("Input Error")
            msg.exec()
            return

        # Check if the item already exists in the database
        self.cursor.execute('''
            SELECT * FROM test_table WHERE input1 = ? AND input2 = ?
        ''', (input1, input2))
        existing_item = self.cursor.fetchone()

        if existing_item:
            # Display an error message box if the item already exists
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("This item already exists in the database.")
            msg.setWindowTitle("Duplicate Entry")
            msg.exec()
            return
    
        print("New item added:")
        print(f"input1: {input1}")
        print(f"input2: {input2}")

        # Save the data to the database
        self.cursor.execute('''
            INSERT INTO test_table (input1, input2)
            VALUES (?, ?)
        ''', (input1, input2))
        self.conn.commit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())