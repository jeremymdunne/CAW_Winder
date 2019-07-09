from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap, QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt
from InputLine import InputLine

class PreWrapSettings(QWidget):
    def __init__(self,parent):
        super(QWidget, self).__init__(parent)
        # go and init our text boxes
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.onlyFloat = QDoubleValidator()
        self.onlyInt = QIntValidator()

        self.home_checkbox = QCheckBox("Home Before Winding")
        self.home_checkbox.setChecked(True)

        self.manual_home_checkbox = QCheckBox("Manual Home (DON'T DO THIS IF YOU DON'T KNOW WHAT IT IS)")

        self.check_locations_checkbox = QCheckBox("Check Holder Location")
        self.check_locations_checkbox.setChecked(True)

        self.feedrate_input = InputLine("Move Feedrate: " , 2000, self.onlyInt)

        self.tube = QLabel()
        self.tube.setPixmap(QPixmap("./graphics/PreWrapDrawing.jpg"))

        self.grid.addWidget(self.home_checkbox, 0,0)
        self.grid.addWidget(self.manual_home_checkbox, 1,0)
        self.grid.addWidget(self.check_locations_checkbox, 2,0)
        self.grid.addWidget(self.feedrate_input, 4,0)
        self.grid.setAlignment(self.feedrate_input,Qt.AlignTop)
        self.grid.addWidget(self.tube, 6, 0, 1, 2)
        self.grid.setAlignment(self.tube, Qt.AlignHCenter)
