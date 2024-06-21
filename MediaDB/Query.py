import sys
import sqlite3
import os
from PySide6.QtWidgets import (
    QComboBox, 
    QApplication, 
    QMainWindow, 
    QPushButton, 
    QLabel, 
    QLineEdit, 
    QVBoxLayout, 
    QWidget, 
    QMessageBox
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
    
class QueryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("---Starting---")
        self.setWindowTitle("Media DB")

        # Create a central widget and set it as the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout
        self.layout = QVBoxLayout(central_widget)

        # Create and add data entry form label
        self.title_label = QLabel("Data Entry Form")
        self.title_label.setAlignment(Qt.AlignCenter)
        font = self.title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        self.layout.addWidget(self.title_label)

        # create the inputs for the database entry and their labels
        self.media_name_label = QLabel("Name:")
        self.media_name_input = QLineEdit()

        self.media_type_label = QLabel("Type of media:")
        self.media_type_input = QComboBox()
        self.media_type_input.addItems(["Film", "Short", "Series", "Documentary", "Other"])

        self.recommendedby_label = QLabel("Recommended by:")
        self.recommendedby_input = QLineEdit()

        self.tags_label = QLabel("Tags:")
        self.tags_input = QLineEdit()

        # add the inputs and others into the window
        self.layout.addWidget(self.media_name_label)
        self.layout.addWidget(self.media_name_input)

        self.layout.addWidget(self.media_type_label)
        self.layout.addWidget(self.media_type_input)

        self.layout.addWidget(self.recommendedby_label)
        self.layout.addWidget(self.recommendedby_input)

        self.layout.addWidget(self.tags_label)
        self.layout.addWidget(self.tags_input)

        # create and add the submit button
        self.submit_button = QPushButton("Submit to DataBase")
        self.layout.addWidget(self.submit_button)

        # connect the button click event to the function
        self.submit_button.clicked.connect(self.Add2DB)

        # Setup the database
        self.setup_database()

    def setup_database(self):
        # Get the path of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, 'Media_DataBase.db')
        print("Script direction")
        print(script_dir)
        print("Database location")
        print(db_path)

        # Connect to the SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Check if the Media_DataBase already exists
        self.cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name='Media_DataBase';
        ''')
        table_exists = self.cursor.fetchone()

        if not table_exists:
            print("Database created.")

        # Create the Media_DataBase table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Media_DataBase (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_name TEXT NOT NULL,
                media_type TEXT NOT NULL,
                recommended_by TEXT NOT NULL,
                media_tags TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def Add2DB(self):
        # get the data from the input fields
        media_name = self.media_name_input.text()
        media_type = self.media_type_input.currentText()
        recommended_by = self.recommendedby_input.text()
        media_tags = self.tags_input.text()

        # Check if any input field is empty
        if not media_name or not media_type:
            # Display an error message box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Name and type are required.")
            msg.setWindowTitle("Input Error")
            msg.exec()
            return

        # Check if the item already exists in the database
        self.cursor.execute('''
            SELECT * FROM Media_DataBase WHERE media_name = ? AND media_type = ?
        ''', (media_name, media_type))
        existing_item = self.cursor.fetchone()

        if existing_item:
            # Display an error message box if the item already exists
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("This item already exists in the database.")
            msg.setWindowTitle("Duplicate Entry")
            msg.exec()
            return

        # Save the data to the database
        self.cursor.execute('''
            INSERT INTO Media_DataBase (media_name, media_type, recommended_by, media_tags)
            VALUES (?, ?, ?, ?)
        ''', (media_name, media_type, recommended_by, media_tags))
        self.conn.commit()

        # print the data to the terminal
        print("New item added:")
        print(f"Name: {media_name}")
        print(f"Type of Media: {media_type}")
        print(f"Recommended by: {recommended_by}")
        print(f"Tags: {media_tags}")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QueryWindow()
    window.show()
    sys.exit(app.exec())
