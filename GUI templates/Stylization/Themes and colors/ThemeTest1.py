import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt
#from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtGui import QPalette, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Themes Test")
        self.resize(300, 250)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        label = QLabel("Theme Test")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button = QPushButton("Sample Button")
        #button.setAlignment(Qt.AlignCenter)
        layout.addWidget(button)


    def create_dark_palette():
        palette = QPalette()

        # Setting dark colors for different roles
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(20, 20, 20))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        
        return palette
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

'''
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

app = QApplication([])

# Applying the dark palette to the application
app.setPalette(create_dark_palette())

layout = QVBoxLayout()
button = QPushButton("Sample Button")
layout.addWidget(button)
window.setLayout(layout)
window.show()

app.exec()

'''