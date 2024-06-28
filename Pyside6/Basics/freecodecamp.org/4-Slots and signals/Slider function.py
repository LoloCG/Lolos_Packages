from PySide6.QtWidgets import QApplication, QSlider
from PySide6.QtCore import Qt

# QtSlider has many signals such as valueChanged, sliderPressed, sliderMoved and sliderReleased

def respond_to_slider():
    print("slider moved to: ", slider.value())

app = QApplication()

slider = QSlider(Qt.Horizontal)
slider.setMinimum(1)
slider.setMaximum(100)
slider.setValue(25)

#slider.valueChanged.connect(respond_to_slider) # This shows real time change of slider
slider.sliderReleased.connect(respond_to_slider) # This shows the ending position of the slider

slider.show()
app.exec()