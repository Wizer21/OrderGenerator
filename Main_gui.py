from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from Data_dialog import *


class Main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.widget_main = QWidget(self)
        self.layout_main = QGridLayout(self)

        self.layout_top_panel = QHBoxLayout(self)
        self.label_selected_profile = QLabel("Test Profile", self)
        self.button_import_data = QPushButton("Import Data", self)
        self.button_generate_mail = QPushButton("Generate Mail", self)
        self.label_sustain_wanted = QLabel("Sustain", self)
        self.line_edit_sustain = QLineEdit(self)

        self.table_widget_main = QTableWidget(self)

        self.build()


    def build(self):
        self.setCentralWidget(self.widget_main)
        self.widget_main.setLayout(self.layout_main)

        self.layout_main.addLayout(self.layout_top_panel, 0, 0)
        self.layout_top_panel.addWidget(self.label_selected_profile)
        self.layout_top_panel.addWidget(self.button_import_data)
        self.layout_top_panel.addWidget(self.button_generate_mail)
        self.layout_top_panel.addWidget(self.label_sustain_wanted)
        self.layout_top_panel.addWidget(self.line_edit_sustain)

        self.layout_main.addWidget(self.table_widget_main, 1, 0)

        self.button_import_data.clicked.connect(self.import_data_clicked)


    @Slot()
    def import_data_clicked(self):
        dialog = Data_dialog()
        dialog.exec_()
