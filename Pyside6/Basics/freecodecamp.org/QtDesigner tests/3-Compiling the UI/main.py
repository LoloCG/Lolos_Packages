# uses the line "pyside6-uic widget.ui > ui_widget.py" on the terminal
     # it requires in "widget.ui" the exact location of the file. here for example is not being located in any folder

     # When the ui is compiled to python, to run it along the rest of the other files it requires
     # changing the encoding. VSCode uses UTF-16. 
     # This can be changed in the bottom right of VSCode when inside the ui_widget.py that was compiled, 
     # and click to "save with encoding" to change to UTF-8

import sys
from PySide6 import QtWidgets
from widget import Widget

app = QtWidgets.QApplication(sys.argv)

window = Widget()
window.show()

app.exec()