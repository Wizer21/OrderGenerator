from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import json

class Mail_build(QDialog):
    def __init__(self, new_item_list, new_mail_profile):
        QDialog.__init__(self)
        self.mail_pattern_list = {}
        self.mail_profile = new_mail_profile
        self.item_list = new_item_list
        self.is_side_display = False

        self.layout_main = QGridLayout(self)

        self.layout_top = QGridLayout(self)
        self.label_title = QLabel("Mail generator", self)
        self.combo_profiles_mail = QComboBox(self)
        self.button_clipboard = QPushButton("Copy to\nclipboard", self)
        self.button_edit = QPushButton("Edit\npattern", self)
        self.button_new = QPushButton("New", self)
        self.button_delete = QPushButton("Delete", self)

        self.text_mail = QTextEdit(self)

        self.widget_side = QWidget(self)
        self.layout_side = QGridLayout(self)
        self.label_edited_profile = QLabel("Default", self)

        self.group_keys = QGroupBox("Body keys", self)
        self.layout_key = QVBoxLayout(self)
        self.text_key_list = QTextEdit(self)

        self.group_header = QGroupBox("Header", self)
        self.layout_header = QVBoxLayout(self)
        self.text_header = QTextEdit(self)

        self.group_body = QGroupBox("Body", self)
        self.layout_body = QVBoxLayout(self)
        self.text_body = QTextEdit(self)

        self.group_foot = QGroupBox("Foot", self)
        self.layout_foot = QVBoxLayout(self)
        self.text_foot = QTextEdit(self)

        self.button_validate = QPushButton("Validate", self)

        self.load_pattern()
        self.build()
        self.display_mail_from_pattern()
        self.resize(1000, 1000)

    def build(self):
        # STRUCTURE
        self.setLayout(self.layout_main)
        self.layout_main.addLayout(self.layout_top, 0, 0)
        self.layout_top.addWidget(self.label_title, 0, 0)
        self.layout_top.addWidget(self.combo_profiles_mail, 1, 0)
        self.layout_top.addWidget(self.button_clipboard, 0, 1, 2, 1)
        self.layout_top.addWidget(self.button_edit, 0, 2, 2, 1)
        self.layout_top.addWidget(self.button_new, 0, 3, 2, 1)
        self.layout_top.addWidget(self.button_delete, 0, 4, 2, 1)

        self.layout_main.addWidget(self.text_mail, 1, 0)

        self.layout_main.addWidget(self.widget_side, 0, 1, 2, 1)
        self.widget_side.setLayout(self.layout_side)
        self.layout_side.addWidget(self.label_edited_profile, 0, 0)

        self.layout_side.addWidget(self.group_keys, 0, 1)
        self.group_keys.setLayout(self.layout_key)
        self.layout_key.addWidget(self.text_key_list)

        self.layout_side.addWidget(self.group_header, 1, 0, 1, 2)
        self.group_header.setLayout(self.layout_header)
        self.layout_header.addWidget(self.text_header)

        self.layout_side.addWidget(self.group_body, 2, 0, 1, 2)
        self.group_body.setLayout(self.layout_body)
        self.layout_body.addWidget(self.text_body)

        self.layout_side.addWidget(self.group_foot, 3, 0, 1, 2)
        self.group_foot.setLayout(self.layout_foot)
        self.layout_foot.addWidget(self.text_foot)

        self.layout_side.addWidget(self.button_validate, 4, 0, 1, 2)

        # WIDGETS PARAMETERS
        self.setWindowTitle("Mail")
        self.button_clipboard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_new.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for key in self.mail_pattern_list:
            self.combo_profiles_mail.addItem(key)

        self.text_key_list.setText("<r> REFERENCE\n<n> NAME\n<b> QUANTITY TO BUY")
        self.text_key_list.setReadOnly(True)

    def load_pattern(self):
        try:
            with open(".\\files\\mail_pattern.json", "r") as data_file:
                self.mail_pattern_list = json.load(data_file)

        except FileNotFoundError:
            mail = {
                "header": "Hello!\n\nI'm sending you from this mail a new order.\n\n",
                "body": "<n> x <b>, Ref <r>.\n",
                "foot": "\nThank you in advance.\nI wish you a pleasant day.\n\nCordially."
            }
            self.mail_pattern_list["Default"] = mail

            with open(".\\files\\mail_pattern.json", "w") as data_file:
                json.dump(self.mail_pattern_list, data_file)

    def display_mail_from_pattern(self):
        mail = ""
        mail += self.mail_pattern_list[self.mail_profile]["header"]

        body = self.mail_pattern_list[self.mail_profile]["body"]

        for i in self.item_list:
            if i.to_buy != 0:
                new_body = body

                new_body = new_body.replace("<r>", i.reference)
                new_body = new_body.replace("<n>", i.name)
                new_body = new_body.replace("<b>", str(i.to_buy))

                mail += new_body

        mail += self.mail_pattern_list[self.mail_profile]["foot"]
        self.text_mail.setText(mail)

