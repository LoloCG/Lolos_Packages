import sys
import os
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

# Get the directory of the current script
    # This is provided by GPT4o. Used due to the original example using the path without any folders
script_dir = os.path.dirname(__file__)
# Construct the full path to the .ui file
ui_file_path = os.path.join(script_dir, "widget.ui")

print("Current working directory:", os.getcwd())
print("UI file path:", ui_file_path)

loader = QUiLoader()  # Set up a loader object

app = QtWidgets.QApplication(sys.argv)
window = loader.load(ui_file_path, None)  # Load the ui - happens at run time
    # with this method, the .ui is transformed into python by the client, thus being inefficient. 

    # the object names such as "lineEdit1" are stablished in the Qt Designer app
def do_something():
    print("data:",window.lineEdit1.text(), "and",window.lineEdit2.text())

# Changing the properties in the form
window.setWindowTitle("User data")

# Accessing widgets in the form
window.pushButton.clicked.connect(do_something)
window.show()
app.exec()