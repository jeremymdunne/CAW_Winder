from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QVBoxLayout
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt
from InputLine import InputLine

class HeatGunSettings(QWidget):
    def __init__(self,parent):
        super(QWidget, self).__init__(parent)
        # go and init our text boxes
        self.grid = QVBoxLayout()
        self.setLayout(self.grid)

        self.onlyFloat = QDoubleValidator()
        self.onlyInt = QIntValidator()

        self.passes_input = InputLine("Heat Gun Passes: ", 20, self.onlyInt)

        self.rotation_per_pass_input = InputLine("Rotations Per Pass: ", 10, self.onlyFloat)

        self.feedrate_input = InputLine("Feedrate: ", 2000, self.onlyInt)

        self.grid.addWidget(self.passes_input)
        self.grid.addWidget(self.rotation_per_pass_input)
        self.grid.addWidget(self.feedrate_input)
        self.grid.addStretch(1)
