from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import json
from NewNameDialog import *


class Communication(QObject):
    new_selected_profile = Signal(str)
    profile_created = Signal(str)


class Settings(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.current_table = "Default"
        self.messager = Communication()

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

        self.button_new_profile.clicked.connect(self.new_profile_clicked)
        self.combobox_profiles.textActivated.connect(self.profile_selected)

        self.load_files()

    def load_files(self):
        with open(".\\files\\settings.json", "r") as data_json:
            settings = json.load(data_json)
            self.current_table = settings["lasttable"]

        with open(".\\files\\tables.json", "r") as data_json:
            tables = json.load(data_json)
            for key in tables:
                self.combobox_profiles.addItem(key)

        self.combobox_profiles.setCurrentText(self.current_table)

    @Slot(str)
    def profile_selected(self, profile_name):
        self.current_table = profile_name
        self.messager.new_selected_profile.emit(profile_name)

    @Slot()
    def new_profile_clicked(self):
        dialog = NewNameDialog()
        dialog.messager.name_new_profile.connect(self.apply_new_profile_name)
        dialog.exec_()

    @Slot(str)
    def apply_new_profile_name(self, name):
        self.messager.profile_created.emit(name)
        self.current_table = name

        self.combobox_profiles.addItem(name)
        self.combobox_profiles.setCurrentText(name)


