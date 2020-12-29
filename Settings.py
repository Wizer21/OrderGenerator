from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class Settings(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        self.layout_main = QGridLayout(self)
        self.label_title = QLabel("Settings", self)

        self.layout_left = QGridLayout(self)
        self.label_preset = QLabel("Profiles", self)
        self.combobox_profiles = QComboBox(self)
        self.button_new_profile = QPushButton("New", self)
        self.button_delete_profile = QPushButton("Delete", self)
        self.label_table_theme = QLabel("Table Theme", self)
        self.combobox_table_theme = QComboBox(self)

        self.layout_right = QVBoxLayout(self)
        self.label_font = QLabel("Font", self)
        self.button_font_chooser = QPushButton("Open Font Chooser", self)

        self.layout_mail = QGridLayout(self)
        self.label_mail_preset = QLabel("Mail presets", self)
        self.combobox_mail = QComboBox(self)
        self.button_edit_mail = QPushButton("Edit", self)
        self.button_create_mail = QPushButton("Create", self)
        self.button_delete_mail = QPushButton("Delete", self)

        self.build()


    def build(self):
        # STRUCTURE
        self.setLayout(self.layout_main)

        self.layout_main.addWidget(self.label_title, 0, 0, 1, 2)

        self.layout_main.addLayout(self.layout_left, 1, 0)
        self.layout_left.addWidget(self.label_preset, 0, 0, 1, 2)
        self.layout_left.addWidget(self.combobox_profiles, 1, 0, 1, 2)
        self.layout_left.addWidget(self.button_new_profile, 2, 0)
        self.layout_left.addWidget(self.button_delete_profile, 2, 1)
        self.layout_left.addWidget(self.label_table_theme, 3, 0, 1, 2)
        self.layout_left.addWidget(self.combobox_table_theme, 4, 0, 1, 2)

        self.layout_main.addLayout(self.layout_right, 1, 1)
        self.layout_right.addWidget(self.label_font)
        self.layout_right.addWidget(self.button_font_chooser)

        self.layout_main.addLayout(self.layout_mail, 2, 0, 1, 2)
        self.layout_mail.addWidget(self.label_mail_preset, 0, 0)
        self.layout_mail.addWidget(self.combobox_mail, 1, 0)
        self.layout_mail.addWidget(self.button_edit_mail, 0, 1, 2, 1)
        self.layout_mail.addWidget(self.button_create_mail, 0, 2, 2, 1)
        self.layout_mail.addWidget(self.button_delete_mail, 0, 3, 2, 1)

        # WIDGETS PARAMETERS
        self.button_edit_mail.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_create_mail.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_delete_mail.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout_right.setAlignment(Qt.AlignTop)



