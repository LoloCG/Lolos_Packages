from PySide6 import QtCore, QtWidgets
from PySide6.QtUiTools import QUiLoader
import os

script_dir = os.path.dirname(__file__)
ui_file_path = os.path.join(script_dir, "widget.ui")

print("Current working directory:", os.getcwd())
print("UI file path:", ui_file_path)

loader = QUiLoader()

class UserInterface(QtCore.QObject): #An object wrapping around our ui
    def __init__(self):
        super().__init__()
        self.ui = loader.load(ui_file_path, None)   # this was originally the widget.ui, but as it is located within folders, it requires this
            # it is still loading at run time
        self.ui.setWindowTitle("User Data")
        self.ui.submit_button.clicked.connect(self.do_something)
    def show(self):
        self.ui.show()
    def do_something(self):
        print(self.ui.full_name_line_edit.text()," is a ",self.ui.occupation_line_edit.text())