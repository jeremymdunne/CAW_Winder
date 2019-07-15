from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt

from InputLine import InputLine

class WrapSettings(QWidget):
    def __init__(self,parent):
        super(QWidget, self).__init__(parent)
        # go and init our text boxes
        self.grid = QVBoxLayout()
        self.setLayout(self.grid)

        self.onlyFloat = QDoubleValidator()
        self.onlyInt = QIntValidator()

        self.filament_width_input = InputLine("Filament Width (in): ", .1, self.onlyFloat)

        self.filament_overlap_input = InputLine("Filament Overlap Multiplier: ", .9, self.onlyFloat)

        self.extension_input = InputLine("Extension Distance (in): ", 1.5, self.onlyFloat)

        self.start_wrap_rotations_input = InputLine("Start Wrap Rotations: ", 1.5, self.onlyFloat)

        self.tie_down_wrap_feedrate_input = InputLine("Start Wrap Feedrate: ", 1500, self.onlyInt)

        # create a new widget that contains two buttons
        self.buttonHolder = QWidget(self)
        hbox = QHBoxLayout()
        self.addButton = QPushButton("Add Row")
        self.addButton.clicked.connect(self.addRowToTable)
        self.removeButton = QPushButton("Remove Row")
        self.removeButton.clicked.connect(self.removeRow)
        hbox.addWidget(self.addButton)
        hbox.addWidget(self.removeButton)
        hbox.addStretch(1)
        self.buttonHolder.setLayout(hbox)

        self.tube = QLabel()
        self.tube.setPixmap(QPixmap("./Graphics/WrappingDrawing.jpg"))

        self.grid.addWidget(self.filament_width_input)
        self.grid.addWidget(self.filament_overlap_input)
        self.grid.addWidget(self.extension_input)
        self.grid.addWidget(self.start_wrap_rotations_input)
        self.grid.addWidget(self.tie_down_wrap_feedrate_input)

        self.initTable()
        self.grid.addWidget(self.table,2)
        self.grid.addWidget(self.buttonHolder)
        self.grid.addWidget(self.tube)
        self.grid.setAlignment(self.tube,Qt.AlignHCenter)
        self.show()


    def removeRow(self):
        if(self.table.rowCount() > 0):
            self.table.setRowCount(self.table.rowCount() - 1)

    def initTable(self):
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        self.table_items = []
        self.table_items.append(QTableWidgetItem)
        self.horizontal_headers = ['Layers','Winding Angle','RPM']
        self.table.setHorizontalHeaderLabels(self.horizontal_headers)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.addRowToTable()
        #self.addRowToTable()


    def addRowToTable(self):
        self.table.setRowCount(self.table.rowCount() + 1)
        layer = QLineEdit("1")
        layer.setValidator(QIntValidator(1,100))
        windingAngle = QLineEdit("45")
        windingAngle.setValidator(QIntValidator(1,89))
        feedrate = QLineEdit("20")
        feedrate.setValidator(QIntValidator(1,20000))
        self.table.setCellWidget(self.table.rowCount() - 1, 0, layer)
        self.table.setCellWidget(self.table.rowCount() - 1, 1, windingAngle)
        self.table.setCellWidget(self.table.rowCount() - 1, 2, feedrate)
