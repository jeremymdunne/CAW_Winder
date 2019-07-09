from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QVBoxLayout
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt
from InputLine import InputLine

class HeatShrinkSettings(QWidget):
    def __init__(self,parent):
        super(QWidget, self).__init__(parent)
        # go and init our text boxes
        self.grid = QVBoxLayout()
        self.setLayout(self.grid)

        self.onlyFloat = QDoubleValidator()
        self.onlyInt = QIntValidator()

        self.heat_shrink_width_input = InputLine("Heat Shrink Width (in): ", .5, self.onlyFloat)

        self.heat_shrink_overlap_input = InputLine("Heat Shrink Overlap Multiplier: ", .9, self.onlyFloat)

        self.feedrate_input = InputLine("Feedrate: ", 2000, self.onlyInt)

        self.layers_input = InputLine("Heat Shrink Layers: ", 1, self.onlyInt)

        self.grid.addWidget(self.heat_shrink_width_input)
        self.grid.addWidget(self.heat_shrink_overlap_input)
        self.grid.addWidget(self.feedrate_input)
        self.grid.addWidget(self.layers_input)
        self.grid.setAlignment(Qt.AlignTop)
