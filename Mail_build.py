from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import json
from NewNameDialog import *
from Utils import *


class Communication(QObject):
    mail_used_changed = Signal(str)


class Mail_build(QDialog):
    def __init__(self, new_item_list, new_mail_profile):
        QDialog.__init__(self)
        self.mail_pattern_list = {}
        self.mail_profile = new_mail_profile
        self.item_list = new_item_list
        self.is_side_display = False
        self.qsize_base = self.size()
        self.messager = Communication()

        self.layout_main = QGridLayout(self)

        self.layout_top = QGridLayout(self)
        self.label_title = QLabel("Mail", self)
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
        Utils.resize_from_resolution(self, 0.40, 0.50)

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
        self.setWindowIcon(Utils.get_pixmap("mail_dark"))
        self.setAttribute(Qt.WA_DeleteOnClose)

        Utils.resize_font(self.label_title, 2.5)

        self.button_clipboard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_new.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        Utils.set_icon(self.button_clipboard, "copy", 2)
        Utils.set_icon(self.button_edit, "edit_mail", 2)
        Utils.set_icon(self.button_new, "create_mail", 2)
        Utils.set_icon(self.button_delete, "trash", 2)
        Utils.style_click_button(self.button_clipboard, "#1976d2")
        Utils.style_click_button(self.button_edit, "#ffa000")
        Utils.style_click_button(self.button_new, "#689f38")
        Utils.style_click_button(self.button_delete, "#d32f2f")
        Utils.style_click_button(self.button_validate, "#689f38")

        self.combo_profiles_mail.setCursor(Qt.PointingHandCursor)
        self.button_clipboard.setCursor(Qt.PointingHandCursor)
        self.button_edit.setCursor(Qt.PointingHandCursor)
        self.button_new.setCursor(Qt.PointingHandCursor)
        self.button_delete.setCursor(Qt.PointingHandCursor)
        self.button_validate.setCursor(Qt.PointingHandCursor)

        self.combo_profiles_mail.setItemDelegate(QStyledItemDelegate())

        for key in self.mail_pattern_list:
            self.combo_profiles_mail.addItem(key)
        self.combo_profiles_mail.setCurrentText(self.mail_profile)

        self.text_key_list.setText("<r> Reference\n<n> Name\n<b> Quantity to buy")
        self.text_key_list.setReadOnly(True)
        self.widget_side.setVisible(False)
        self.text_key_list.setStyleSheet("border: 0px solid white;")
        self.text_header.setStyleSheet("border: 0px solid white;")
        self.text_body.setStyleSheet("border: 0px solid white;")
        self.text_foot.setStyleSheet("border: 0px solid white;")

        self.combo_profiles_mail.currentTextChanged.connect(self.profile_changed)
        self.text_header.textChanged.connect(self.update_header)
        self.text_body.textChanged.connect(self.update_body)
        self.text_foot.textChanged.connect(self.update_foot)
        self.button_validate.clicked.connect(self.validate_clicked)
        self.button_new.clicked.connect(self.new_button_clicked)
        self.button_delete.clicked.connect(self.button_delete_clicked)
        self.button_clipboard.clicked.connect(self.clipboard_clicked)

        self.button_edit.clicked.connect(self.edit_clicked)

    def load_pattern(self):
        try:
            with open(".\\files\\mail_pattern.json", "r") as data_file:
                self.mail_pattern_list = json.load(data_file)
        except FileNotFoundError:
            self.mail_pattern_list["Default"] = self.default_mail()
            self.save_patterns()

    def save_patterns(self):
        with open(".\\files\\mail_pattern.json", "w") as data_file:
            json.dump(self.mail_pattern_list, data_file)

    def display_mail_from_pattern(self):
        mail = ""
        mail += self.mail_pattern_list[self.mail_profile]["header"]
        body = self.mail_pattern_list[self.mail_profile]["body"]

        for i in self.item_list:
            if i.to_buy > 1:
                new_body = body

                new_body = new_body.replace("<r>", i.reference)
                new_body = new_body.replace("<n>", i.name)
                new_body = new_body.replace("<b>", str(i.to_buy))

                mail += new_body

        mail += self.mail_pattern_list[self.mail_profile]["foot"]
        self.text_mail.setText(mail)

    def edit_clicked(self):
        self.toggle_side()

        if self.is_side_display:
            self.text_header.setText(self.mail_pattern_list[self.mail_profile]["header"])
            self.text_body.setText(self.mail_pattern_list[self.mail_profile]["body"])
            self.text_foot.setText(self.mail_pattern_list[self.mail_profile]["foot"])

    def toggle_side(self):
        if self.is_side_display:
            self.is_side_display = False
            self.widget_side.setVisible(False)
            self.resize(0, self.qsize_base.height())
        else:
            self.is_side_display = True
            self.widget_side.setVisible(True)

            self.qsize_base = self.size()
            self.resize(int(self.qsize_base.width() * 1.5), self.qsize_base.height())

    @Slot()
    def update_header(self):
        self.mail_pattern_list[self.mail_profile]["header"] = self.text_header.toPlainText()
        self.display_mail_from_pattern()

    @Slot()
    def update_body(self):
        self.mail_pattern_list[self.mail_profile]["body"] = self.text_body.toPlainText()
        self.display_mail_from_pattern()

    @Slot()
    def update_foot(self):
        self.mail_pattern_list[self.mail_profile]["foot"] = self.text_foot.toPlainText()
        self.display_mail_from_pattern()

    @Slot()
    def validate_clicked(self):
        self.save_patterns()
        self.toggle_side()

    @Slot()
    def new_button_clicked(self):
        new_name = NewNameDialog("mail")
        new_name.messager.name_new_profile.connect(self.apply_new_preset)
        new_name.exec_()

    @Slot(str)
    def apply_new_preset(self, profile_name):
        self.mail_profile = profile_name

        self.mail_pattern_list[profile_name] = self.default_mail()
        self.combo_profiles_mail.addItem(profile_name)
        self.combo_profiles_mail.setCurrentText(profile_name)

        self.save_patterns()

    @Slot(str)
    def profile_changed(self, name):
        self.mail_profile = name
        self.display_mail_from_pattern()
        self.messager.mail_used_changed.emit(name)

    @Slot()
    def button_delete_clicked(self):
        box = QMessageBox(QMessageBox.Warning, "Delete {0}".format(self.mail_profile), "Do you really want to delete {0} ?".format(self.mail_profile)
                          , QMessageBox.Yes)
        box.addButton(QMessageBox.No)
        rep = box.exec_()
        if rep == QMessageBox.Yes:
            del self.mail_pattern_list[self.mail_profile]

            if len(self.mail_pattern_list) == 0:
                self.mail_pattern_list["Default"] = self.default_mail()
                self.mail_profile = "Default"
            else:
                for key in self.mail_pattern_list:
                    self.mail_profile = key
                    break

            self.combo_profiles_mail.blockSignals(True)
            self.combo_profiles_mail.clear()
            for i in self.mail_pattern_list:
                self.combo_profiles_mail.addItem(i)
            self.combo_profiles_mail.blockSignals(False)
            self.combo_profiles_mail.setCurrentText(self.mail_profile)
            self.profile_changed(self.mail_profile)

            self.save_patterns()

    def default_mail(self):
        mail = {
            "header": "Hello!\n\nI'm sending you from this mail a new order.\n\n",
            "body": "<n> x <b>, Ref <r>.\n",
            "foot": "\nThank you in advance.\nI wish you a pleasant day.\n\nCordially."
        }
        return mail

    def clipboard_clicked(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.text_mail.toPlainText())

