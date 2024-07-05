from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from ui_widget import Ui_Widget

class Widget(QWidget, Ui_Widget): # the Ui_Widget derives from the top level widget created in Qt Designer, not from the file itself.
    def __init__(self):
        super().__init__()
        self.setupUi(self) # it allows access to anyhting in the ui file that was compiled to python
        self.setWindowTitle("User data")
        self.submit_button.clicked.connect(self.do_something)
        
    def do_something(self):
        print(self.full_name_line_edit.text()," is a ",self.occupation_line_edit.text())


