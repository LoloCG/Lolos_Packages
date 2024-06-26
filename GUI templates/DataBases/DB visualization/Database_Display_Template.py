import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QTableView, QMessageBox, QHeaderView
)
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PySide6.QtCore import Qt, QAbstractTableModel
import os


class AlignCenterSqlTableModel(QSqlTableModel):
    def data(self, index, role=Qt.DisplayRole):
        value = super().data(index, role)
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return value


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Database Viewer")
        self.resize(600, 400)

        # Create main widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Set up layout
        self.layout = QVBoxLayout(self.main_widget)

        # Add input fields
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.age_label = QLabel("Age:")
        self.age_input = QLineEdit()
        self.layout.addWidget(self.age_label)
        self.layout.addWidget(self.age_input)

        self.submit_button = QPushButton("Add to Database")
        self.layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.add_to_db)

        # Add table view
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        # Initialize database and set up the model
        self.setup_database()

    def setup_database(self):
        # Set up the database connection
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, 'TestDB.db')

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_path)

        if not self.db.open():
            QMessageBox.critical(self, "Database Error", self.db.lastError().text())
            return

        self.model = AlignCenterSqlTableModel(self, self.db)
        self.model.setTable("TestDB")

        # Create table if it doesn't exist
        self.create_table_if_not_exists()

        self.model.select()
        self.table_view.setModel(self.model)

        # Hide the ID column
        self.table_view.setColumnHidden(0, True)
        
        # Set the section resize mode for all columns
        for column in range(1, self.model.columnCount()):  # Skip the hidden ID column
            self.table_view.horizontalHeader().setSectionResizeMode(column, QHeaderView.Stretch)

    def create_table_if_not_exists(self):
        query = QSqlQuery(self.db)
        query.exec('''
            CREATE TABLE IF NOT EXISTS TestDB (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        ''')

    def add_to_db(self):
        name = self.name_input.text()
        age = self.age_input.text()

        if not name or not age:
            QMessageBox.warning(self, "Input Error", "Name and age are required.")
            return

        try:
            age = int(age)  # Ensure age is an integer
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Age must be an integer.")
            return

        query = QSqlQuery(self.db)
        query.prepare('''
            INSERT INTO TestDB (name, age)
            VALUES (?, ?)
        ''')
        query.addBindValue(name)
        query.addBindValue(age)

        if not query.exec():
            QMessageBox.critical(self, "Database Error", query.lastError().text())
            return

        self.model.select()  # Refresh the model to show the new data
        self.refresh_model()  # Explicitly refresh the model

        self.name_input.clear()
        self.age_input.clear()

    def refresh_model(self):
        self.model.setTable("TestDB")
        self.model.select()
        self.table_view.setModel(self.model)
        self.table_view.setColumnHidden(0, True)
        for column in range(1, self.model.columnCount()):
            self.table_view.horizontalHeader().setSectionResizeMode(column, QHeaderView.Stretch)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
