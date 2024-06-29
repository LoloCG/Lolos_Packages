from PySide6.QtCore import QSize
from PySide6.QtGui import QAction 
from PySide6.QtWidgets import QMainWindow, QToolBar

class MainWindow(QMainWindow): #inhetirs from QMainWindow
    # makes the constructor
    def __init__(self, app):
        super().__init__()

        self.app = app #declare an app member, which is the application instance that can be exited later
        self.setWindowTitle("Main Window")

        # For Menus:

        #Add different menus
        menu_bar = self.menuBar() # calls the menu bar function on QMainWindow, giving menu_bar object 
        file_menu = menu_bar.addMenu("&File") # adds a "file" menu. the "addMenu" adss another menu.
        quit_action = file_menu.addAction("Quit") # An Action is an object that can be added to the toolbar and/or the menubar, that  both controls the same action
        quit_action.triggered.connect(self.quit) # stablishes the connection of the action of "quit" action object.

        # Adds other menu options in QMainWindow, with options
        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Cut")
        edit_menu.addAction("Paste")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")

        # For toolbars:
        toolbar = QToolBar("My main toolbar") # we set up a toolbar object
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar) # we add it to the main window

        # Adds the quit action to the toolbar
        toolbar.addAction(quit_action) 

        # Create a new action
        action1 = QAction("button1", self) # we can pass an icon.
        action1.setStatusTip("Status message for some action")
        action1.triggered.connect(self.button1_clicked)
        toolbar.addAction(action1) # we add an action1 to the toolbar
        
        '''
        action2 = QAction(QIcon("start.png"), "Some other action", self)
        action2.setStatusTip("Status message for some other action")
        action2.triggered.connect(self.toolbar_button_click)
        action2.setCheckable(True)
        toolbar.addAction(action2)
        '''
    def quit(self):
        self.app.quit()

    def button1_clicked(self):
        print("Clicked on button1")