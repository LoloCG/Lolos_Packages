import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from secondwidget import widgetholder1
     # The module QMainWindow provides the framework for building the application's user interface
        # allows to set up menu bars, toolbars, status bars...

app = QApplication(sys.argv)

window = widgetholder1()
window.show()
app.exec()
