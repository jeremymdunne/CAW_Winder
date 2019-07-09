from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
class InputLine(QWidget):
    def __init__(self, text, deafaultValue = None, validator = None):
        super().__init__()
        self.label = QLabel(text)
        self.edit = QLineEdit(str(deafaultValue))
        if validator is not None:
            self.edit.setValidator(validator)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)
        self.layout.addStretch(1)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.layout)


    def setLabel(self, text):
        self.label.text(text)

    def setValue(self, value):
        self.edit.text(value)

    def text(self):
        return self.edit.text()
