import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QStatusBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor, QPalette

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Top FileMenu test")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create the buttons before the menu bar is created
        ClearTheme_Button = QAction("Clear theme", self)
        ClearTheme_Button.setStatusTip("Change to Clear theme style")
        #ClearTheme_Button.setCheckable(True) #Used when you want permanent check of the button
        ClearTheme_Button.triggered.connect(self.ClearThemeSelect)

        DarkTheme_Button = QAction("Dark theme", self)
        DarkTheme_Button.setStatusTip("Change to Dark theme style")
        #DarkTheme_Button.setCheckable(True) #Used when you want permanent check of the button
        DarkTheme_Button.triggered.connect(self.DarkThemeSelect)

        # Create the menu bar and add the buttons
        menu = self.menuBar()

        file_menu = menu.addMenu("Settings")

        # file_menu.addSeparator() # Used when you want separation between buttons

        file_submenu = file_menu.addMenu("Themes")
        file_submenu.addAction(ClearTheme_Button)
        file_submenu.addAction(DarkTheme_Button)

        # this is used to show the status tip when hovering over the button
        self.setStatusBar(QStatusBar(self))

    def ClearThemeSelect(self):
        print("Clear theme selected")

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Base, QColor(240, 240, 240))
        palette.setColor(QPalette.AlternateBase, QColor(225, 225, 225))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(0, 0, 255))
        palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        app.setPalette(palette)


    def DarkThemeSelect(self):
        print("Dark theme selected")
        palette = QPalette()
        # Windows color
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.Base, QColor(42, 42, 42))
        palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        palette.setColor(QPalette.ToolTipBase, QColor(220, 220, 220))

        # Texts
        palette.setColor(QPalette.ToolTipText, QColor(220, 220, 220))
        palette.setColor(QPalette.Text, QColor(220, 220, 220))
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

        app.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


