import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QTabWidget, QWidget, QCheckBox,
                    QHBoxLayout, QLabel, QPushButton, QGroupBox, QFileDialog)

from TubeTab import TubeTab
from PreWrapSettings import PreWrapSettings
from WrapSettings import WrapSettings
from HeatShrinkSettings import HeatShrinkSettings
from HeatGunSettings import HeatGunSettings
from TubeWinder import TubeWinder

class CAW_UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAW: Computer Aided Winding")
        self.initUI()

    def initUI(self):
        # two main widgets for now: a tabs widget and a side options
        self.main_widget = QWidget(self)
        self.init_tabs_widget()
        self.init_side_settings_widget()
        hbox = QHBoxLayout()
        hbox.addWidget(self.tabs_widget)
        hbox.addWidget(self.side_group)
        self.main_widget.setLayout(hbox)
        self.setCentralWidget(self.main_widget)
        #self.showMaximized()
        self.wrap_button.clicked.connect(self.on_click)
        self.show()


    def init_tabs_widget(self):
        self.tabs_widget = QTabWidget(self.main_widget)
        self.tube_tab = TubeTab(self.main_widget)
        self.pre_wrap_tab = PreWrapSettings(self.main_widget)
        self.wrap_tab = WrapSettings(self.main_widget)
        self.heat_shrink_tab = HeatShrinkSettings(self.main_widget)
        self.heat_gun_tab = HeatGunSettings(self.main_widget)
        self.tabs_widget.addTab(self.tube_tab, "Tube Settings")
        self.tabs_widget.addTab(self.pre_wrap_tab, "Pre Wrap Settings")
        self.tabs_widget.addTab(self.wrap_tab, "Wrap Settings")
        self.tabs_widget.addTab(self.heat_shrink_tab, "Heat Shrink Settings")
        self.tabs_widget.addTab(self.heat_gun_tab, "Heat Gun Settings")

    def init_side_settings_widget(self):
        self.side_group = QGroupBox("Wrap Settings")
        #self.side_settings_widget = QWidget(self.main_widget)
        vbox = QVBoxLayout()
        self.pre_wrap_checkbox = QCheckBox("Pre Wrap")
        self.pre_wrap_checkbox.setChecked(True)
        self.wrap_checkbox = QCheckBox("Wrap")
        self.wrap_checkbox.setChecked(True)
        self.heat_shrink_checkbox = QCheckBox("Heat Shrink")
        self.heat_shrink_checkbox.setChecked(True)
        self.heat_gun_checkbox = QCheckBox("Heat Gun")
        self.heat_gun_checkbox.setChecked(True)
        self.wrap_button = QPushButton("Wrap")

        vbox.addWidget(self.pre_wrap_checkbox)
        vbox.addWidget(self.wrap_checkbox)
        vbox.addWidget(self.heat_shrink_checkbox)
        vbox.addWidget(self.heat_gun_checkbox)
        vbox.addWidget(self.wrap_button)
        vbox.addStretch(1)
        self.side_group.setLayout(vbox)


    def on_click(self):
        # Yay! Wrap!
        # ask for a file
        name = QFileDialog.getSaveFileName(self, 'Save File')[0]
        if name is None or name == "":
            self.showError("File","Must specify name of file to save as")
            return
        if name.find(".") < 0:
            name += ".gcode"
        file = open(name,'w')
        tubeWrapper = TubeWinder(file,float(self.tube_tab.od_input.text()) * 25.4,float(self.tube_tab.length_input.text())*25.4,float(self.tube_tab.start_offset_input.text())*25.4,float(self.tube_tab.head_offset_input.text()) * 25.4)
        if(self.pre_wrap_checkbox.isChecked()):
            # do a pre wrap!
            # TODO check settingsS
            tubeWrapper.pre_wrap(self.pre_wrap_tab.home_checkbox.isChecked(), self.pre_wrap_tab.manual_home_checkbox.isChecked(), self.pre_wrap_tab.check_locations_checkbox.isChecked(),int(self.pre_wrap_tab.feedrate_input.text()))
        if(self.wrap_checkbox.isChecked()):
            # first execute the tie down wrap
            tubeWrapper.tie_down_wrap(float(self.wrap_tab.extension_input.text()) * 25.4,float(self.wrap_tab.start_wrap_rotations_input.text()),float(self.wrap_tab.tie_down_wrap_feedrate_input.text()))
            # now go and handle each row
            for i in range(0, self.wrap_tab.table.rowCount()):
                tubeWrapper.wrap(float(self.wrap_tab.filament_width_input.text()) * 25.4,float(self.wrap_tab.filament_overlap_input.text()),float(self.wrap_tab.table.cellWidget(i,1).text()),float(self.wrap_tab.table.cellWidget(i,0).text()),int(self.wrap_tab.table.cellWidget(i,2).text()),float(self.wrap_tab.extension_input.text())*25.4)
        if(self.heat_shrink_checkbox.isChecked()):
            tubeWrapper.shrink_tape(float(self.heat_shrink_tab.heat_shrink_width_input.text())*25.4,float(self.heat_shrink_tab.heat_shrink_overlap_input.text()), int(self.heat_shrink_tab.feedrate_input.text()))
        if(self.heat_gun_checkbox.isChecked()):
            tubeWrapper.heat_gun(float(self.heat_gun_tab.rotation_per_pass_input.text()), int(self.heat_gun_tab.passes_input.text()), int(self.heat_gun_tab.feedrate_input.text()))
        file.close()


    def showError(self, title, message, more_info = None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setText(message)
        if more_info is not None:
            msg.setInformativeText(more_info)
        msg.setWindowTitle(title)
        msg.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = CAW_UI()
    sys.exit(app.exec_())
