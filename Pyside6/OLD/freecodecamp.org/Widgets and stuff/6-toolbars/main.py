
from PySide6.QtWidgets import QApplication
from mainWindow import MainWindow
import sys

app = QApplication(sys.argv)

window = MainWindow(app)
window.show()
app.exec()

'''
        

        toolbar.addSeparator()
        toolbar.addWidget(QPushButton("Click here"))

        # Statusbar
        self.setStatusBar(QStatusBar(self)) # we set the status bar on the main window

        button1 = QPushButton("BUTTON1") # we add a button
        button1.clicked.connect(self.button1_clicked)
        self.setCentralWidget(button1) # we set it up as the central button


# methods:


    def toolbar_button_click(self):
        self.statusBar().showMessage("Some message ...", 3000)


        
''' 