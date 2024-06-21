import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QLabel, QListWidget, QStackedWidget, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dark Theme GUI with Side Tab")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QHBoxLayout()
        
        # Side tab
        self.side_tab = QListWidget()
        self.side_tab.addItem("Home")
        self.side_tab.addItem("Settings")
        self.side_tab.addItem("About")
        self.side_tab.setFixedWidth(150)  # Set the width of the side tab
        self.side_tab.currentRowChanged.connect(self.display_content)

        # Stacked widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_home_widget())
        self.stacked_widget.addWidget(self.create_settings_widget())
        self.stacked_widget.addWidget(self.create_about_widget())

        # Add side tab and stacked widget to main layout
        main_layout.addWidget(self.side_tab)
        main_layout.addWidget(self.stacked_widget)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Set the dark theme
        self.set_dark_theme()

    def set_dark_theme(self):
        dark_palette = QPalette()

        # Base colors
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(42, 42, 42))
        dark_palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)

        # Highlight colors
        dark_palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        # Set palette
        QApplication.instance().setPalette(dark_palette)

    def create_home_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the Home Page"))
        widget.setLayout(layout)
        return widget

    def create_settings_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings Page"))
        widget.setLayout(layout)
        return widget

    def create_about_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("About Page"))
        widget.setLayout(layout)
        return widget

    def display_content(self, index):
        self.stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply a dark theme style
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
