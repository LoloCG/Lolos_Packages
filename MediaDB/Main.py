# Main.py
import sys
from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow,
    QWidget, 
    QStatusBar,
    QVBoxLayout,
    QStackedWidget,
    QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction
from Query import QueryWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Media DB")

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # Create a stacked widget
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Create and add different widgets to the stacked widget
        self.main_menu_widget = QWidget()
        self.main_menu_layout = QVBoxLayout(self.main_menu_widget)
        self.main_menu_label = QLabel("Main Menu")
        self.main_menu_layout.addWidget(self.main_menu_label)
        self.stacked_widget.addWidget(self.main_menu_widget)

        # Initialize query widget but do not add to stacked widget until needed
        self.query_widget = None

        # Create menu actions
        self.create_actions()

        # Set initial widget to main menu
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)

        # Create status bar
        self.setStatusBar(QStatusBar(self))

    def create_actions(self):
        query_menu_button = QAction("Import new", self)
        query_menu_button.setStatusTip("Open query to import new Media")
        query_menu_button.triggered.connect(self.open_query)

        main_menu_button = QAction("Main menu", self)
        main_menu_button.setStatusTip("Return to main menu")
        main_menu_button.triggered.connect(self.open_main_menu)

        menu = self.menuBar()
        file_menu = menu.addMenu("Import")
        file_menu.addAction(query_menu_button)

        return_menu = menu.addMenu("Return to menu")
        return_menu.addAction(main_menu_button)

    def open_query(self):
        if self.query_widget is None:
            self.query_widget = QueryWindow()
            self.stacked_widget.addWidget(self.query_widget.centralWidget())
        self.stacked_widget.setCurrentWidget(self.query_widget.centralWidget())
        print("query button clicked")

    def open_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)
        print("menu button clicked")

        '''
        self.query_widget = QueryWindow()
        self.stacked_widget.addWidget(self.query_widget.centralWidget())
        self.main_menu_widget = QWidget()
        self.stacked_widget.addWidget(self.main_menu_widget)

        # __________Menu Buttons__________
    
        # Create the buttons before the menu bar is created
        Query_Menu_Button = QAction("Import new", self)
        Query_Menu_Button.setStatusTip("Open query to import new Media")
        Query_Menu_Button.triggered.connect(self.Open_query)

        MainScreen_Menu_Button = QAction("Main menu", self)
        MainScreen_Menu_Button.setStatusTip("Return to main menu")
        MainScreen_Menu_Button.triggered.connect(self.Open_main_menu)
        
        # Create the menu bar, add the buttons and add status bar
        menu = self.menuBar()

        file_menu = menu.addMenu("Import")
        file_menu.addAction(Query_Menu_Button)

        file_menu = menu.addMenu("Return to menu")
        file_menu.addAction(MainScreen_Menu_Button)

        self.setStatusBar(QStatusBar(self))

    # Define functions for opening different widgets
    def Open_query(self):
        self.stacked_widget.setCurrentWidget(self.query_widget.centralWidget())
        print("query button clicked")

    def Open_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)
        print("menu button clicked")
    '''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

    '''
    from Palette import dark_palette, get_registered_palettes

    # Set default palette to dark
    app.setPalette(dark_palette())
    '''

    '''
        # Create and add different widgets to the stacked widget
        self.query_widget = QueryWindow()
        self.main_menu_widget = QWidget()  # Placeholder for the main menu widget
        self.main_menu_layout = QVBoxLayout(self.main_menu_widget)
        self.main_menu_layout.addWidget(QLabel("Main Menu"))

        self.stacked_widget.addWidget(self.main_menu_widget)
        self.stacked_widget.addWidget(self.query_widget.centralWidget())

        # Create the actions for the menu
        self.create_actions()

        self.setStatusBar(QStatusBar(self))
        '''
    '''
        def create_actions(self):
            button_action = QAction("Import new", self)
            button_action.setStatusTip("Open query")
            button_action.triggered.connect(self.show_query_widget)

            button_action2 = QAction("Main menu", self)
            button_action2.setStatusTip("Return to main menu")
            button_action2.triggered.connect(self.show_main_menu_widget)
        '''
    '''

        # Add a placeholder widget for QueryWindow content
        self.query_widget = QueryWindow()
        self.layout.addWidget(self.query_widget.centralWidget())

        # Load registered palettes before creating the toolbar
        self.palette_map = get_registered_palettes()

        self.create_toolbar()
        '''
    '''
    def ButtonClick1(self):
        

    def ButtonClick2(self):
        
    '''
'''
    def change_palette(self, palette_name):
        palette_func = self.palette_map.get(palette_name)
        if palette_func:
            app.setPalette(palette_func())
'''
