from PySide6.QtWidgets import QApplication, QWidget
import sys
from widgets1 import RockWidget

app = QApplication(sys.argv)

window = RockWidget()
window.show()

app.exec()