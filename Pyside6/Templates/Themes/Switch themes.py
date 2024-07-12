import sys
from PySide6.QtCore import Qt
#from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtWidgets import (
    QApplication, QMainWindow, 
    QVBoxLayout, QLabel, QWidget,
    QGroupBox, QCheckBox, QButtonGroup
    )

class MainWindow(QMainWindow):  # We create a class, inheriting from QMainWindow
    def __init__(self): # The constructor
        super().__init__() 

        self.setWindowTitle("MainWindow App")
    # Create the central widget, set it as central and set the layout from it
        central_widget = QWidget(self)  # Create a central widget that will contain other widgets
        self.setCentralWidget(central_widget)  # Set the central widget
        layout = QVBoxLayout(central_widget) # Create a vertical layout for the central widget

    # We create the the label and test buttons
        title_label = QLabel("Theme test")
        title_label.setAlignment(Qt.AlignCenter) # Adjust the label to the center
        layout.addWidget(title_label)
        
    # Create the checkboxes, their layout and connections
        # First we set the GroupBox, that will contain the CheckBoxes, along the checkboxes.
        Theme_Checkboxes = QGroupBox("Choose style")
        Checkbox1 = QCheckBox("Windows vista")
        Checkbox2 = QCheckBox("Fusion dark")
        Checkbox3 = QCheckBox("Default windows")
        Checkbox4 = QCheckBox("test")
        Checkbox1.setChecked(True) # we set up the first option checked by default
        
        # Connect them to their function
        Checkbox1.toggled.connect(self.WinVis_ThemeChange)
        Checkbox2.toggled.connect(self.Fus_ThemeChange)
        Checkbox3.toggled.connect(self.Def_ThemeChange)
        Checkbox4.toggled.connect(self.Test_ThemeChange)

        # We select the group of buttons that is exclusive, adding them to a QButtonGroup
        ex_button_group = QButtonGroup(self)
        ex_button_group.addButton(Checkbox1)
        ex_button_group.addButton(Checkbox2)
        ex_button_group.addButton(Checkbox3)
        ex_button_group.addButton(Checkbox4)
        
        # We add them to the layout
        Theme_Checkboxes_Layout = QVBoxLayout() # Create a vertical box layout for boxes and the container
        Theme_Checkboxes_Layout.addWidget(Checkbox1)
        Theme_Checkboxes_Layout.addWidget(Checkbox2)
        Theme_Checkboxes_Layout.addWidget(Checkbox3)
        Theme_Checkboxes_Layout.addWidget(Checkbox4)
        Theme_Checkboxes.setLayout(Theme_Checkboxes_Layout)

        layout.addWidget(Theme_Checkboxes) # add that second layout to the first

    def Def_ThemeChange(self,checked):
        if(checked):
            print("theme changed to Windows Default")
            app.setStyle('Windows')

    def Fus_ThemeChange(self,checked):
        if(checked):
            print("theme changed to Fusion dark")            
            app.setStyle('Fusion')

    def WinVis_ThemeChange(self,checked):
        if(checked):
            print("theme changed to Windows Vista")            
            app.setStyle('windowsvista')

    def Test_ThemeChange(self,checked):
        if(checked):
            print("theme changed to basic")            
            app.setStyle('') 
        # Those that dont work... basic, Basic, default, imagine, Material, universal, Universal
        
app = QApplication(sys.argv)
app.setStyle('windowsvista')  # Start with Fusion style
window = MainWindow()
window.show()
app.exec()

'''
        self.is_fusion = True

    def toggle_style(self):
        if self.is_fusion:
            app.setStyle('Breeze')  # Switch to Windows style or any other available style
            print("Changed to default")
        else:
            app.setStyle('Fusion')  # Switch back to Fusion style
            print("Changed to Fusion")
        self.is_fusion = not self.is_fusion
'''