from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from Widgets.UI_MWindow import Ui_MainWindow
from Widgets.UI_VideoQuery import Ui_VideoForm

class MainWindow(QWidget, Ui_MainWindow): 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Media Database")

        self.actionMovie.triggered.connect(self.ShowVideoQuery)  # .connect(self.ShowVideoQuery)

    def ShowVideoQuery(self):
        print("showing video query")
        self.video_query_window = VideoQuery()
        self.video_query_window.show()
        self.video_query_window.raise_()  # Bring the window to the front

class VideoQuery(QWidget, Ui_VideoForm):
       def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.setWindowTitle("Video Query")