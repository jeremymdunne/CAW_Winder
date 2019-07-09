from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QDoubleValidator
from PyQt5.QtCore import Qt
from InputLine import InputLine

class TubeTab(QWidget):
    def __init__(self,parent):
        super(QWidget, self).__init__(parent)
        # go and init our text boxes
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.onlyFloat = QDoubleValidator()

        # now the data in the graphic at the bottom
        self.length_input = InputLine("Length (in): ",10,self.onlyFloat)

        self.od_input = InputLine("O.D. (in): ",2.716,self.onlyFloat)

        self.start_offset_input = InputLine("Start Offset (in): ", 1.5, self.onlyFloat)

        self.head_offset_input = InputLine("Head Offset (in): ", 1, self.onlyFloat)

        self.tube = QLabel()
        self.tube.setPixmap(QPixmap("./graphics/BodyTubeDrawing.jpg"))

        vbox = QVBoxLayout()

        vbox.addWidget(self.length_input)
        vbox.addWidget(self.od_input)
        vbox.addWidget(self.start_offset_input)
        vbox.addWidget(self.head_offset_input)
        vbox.setAlignment(Qt.AlignTop)
        tempWidget = QWidget()
        tempWidget.setLayout(vbox)
        #self.grid.addWidget(self.head_offset_textbox, 5,1)
        self.grid.addWidget(tempWidget,0,0)
        self.grid.addWidget(self.tube, 6, 0, 1, 2)
        self.grid.setAlignment(self.tube, Qt.AlignHCenter)
        self.show()
