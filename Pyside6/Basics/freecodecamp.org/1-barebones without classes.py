# From Learn Python GUI Development for Desktop – PySide6 and Qt Tutorial
# https://www.youtube.com/watch?v=Z1N9JzNax2k

from PySide6.QtWidgets import QApplication, QWidget

# module responsible for processing command line arguments.
import sys

# The wrapper responsible for running the application
# and waiting for things to happen while we interact with the application
app = QApplication(sys.argv)

window = QWidget()
window.show() # by default, widget are hidden unless shown

app.exec() # this starts the event loop
