from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import json
from NewNameDialog import *
from Utils import *

class Communication(QObject):
    new_selected_profile = Signal(str)
    profile_created = Signal(str)
    update_color_table = Signal(dict)
    deleted_profile = Signal(str)
    send_is_show_ref = Signal(bool)
    send_is_show_buyp = Signal(bool)
    send_is_show_sellp = Signal(bool)


class Settings(QDialog):
    def __init__(self, new_color_dict, is_show_ref, is_show_buyp, is_show_sellp):
        QDialog.__init__(self)
        self.color_dict = new_color_dict
        self.current_table = "Default"
        self.profile_list = {}
        self.messager = Communication()
        self.color_list = ["#000000", "#2A363B", "#546e7a", "#757575", "#6d4c41", "#f4511e", "#fb8c00", "#ffb300",
                           "#fdd835", "#c0ca33", "#7cb342", "#43a047", "#00897b", "#00acc1",
                           "#039be5", "#1e88e5", "#3949ab", "#5e35b1", "#8e24aa", "#d81b60",
                           "#e53935"]
        self.show_ref = is_show_ref
        self.show_buyp = is_show_buyp
        self.show_sellp = is_show_sellp

        self.layout_main = QGridLayout(self)
        self.label_title = QLabel("Settings", self)

        self.layout_left = QGridLayout(self)
        self.label_preset = QLabel("Profiles", self)
        self.combobox_profiles = QComboBox(self)
        self.button_new_profile = QPushButton("New", self)
        self.button_delete_profile = QPushButton("Delete", self)
        self.label_show_ref = QLabel("Show reference", self)
        self.button_show_ref = QPushButton(self)

        self.layout_right = QVBoxLayout(self)
        self.label_buyp = QLabel("Show buy price", self)
        self.button_show_buyp = QPushButton(self)
        self.label_sellp = QLabel("Show sell price", self)
        self.button_show_sellp = QPushButton(self)

        self.group_color = QGroupBox("Table Theme", self)
        self.layout_colors = QGridLayout(self)
        self.combo_color_reference = QComboBox(self)
        self.combo_color_text = QComboBox(self)
        self.combo_color_sells = QComboBox(self)
        self.combo_color_stock = QComboBox(self)
        self.combo_color_buyp = QComboBox(self)
        self.combo_color_sellp = QComboBox(self)
        self.combo_color_average = QComboBox(self)
        self.combo_color_to_buy = QComboBox(self)

        self.build()
        Utils.resize_from_resolution(self, 0.25, 0.3)


    def build(self):
        # STRUCTURE
        self.setLayout(self.layout_main)

        self.layout_main.addWidget(self.label_title, 0, 0, 1, 2)

        self.layout_main.addLayout(self.layout_left, 1, 0)
        self.layout_left.addWidget(self.label_preset, 0, 0, 1, 2)
        self.layout_left.addWidget(self.combobox_profiles, 1, 0, 1, 2)
        self.layout_left.addWidget(self.button_new_profile, 2, 0)
        self.layout_left.addWidget(self.button_delete_profile, 2, 1)

        self.layout_main.addLayout(self.layout_right, 1, 1)
        self.layout_right.addWidget(self.label_buyp)
        self.layout_right.addWidget(self.button_show_buyp)
        self.layout_right.addWidget(self.label_sellp)
        self.layout_right.addWidget(self.button_show_sellp)
        self.layout_right.addWidget(self.label_show_ref)
        self.layout_right.addWidget(self.button_show_ref)

        self.layout_main.addWidget(self.group_color, 2, 0, 1, 2)
        self.group_color.setLayout(self.layout_colors)
        self.layout_colors.addWidget(self.combo_color_reference, 0, 0)
        self.layout_colors.addWidget(self.combo_color_text, 0, 1)
        self.layout_colors.addWidget(self.combo_color_sells, 0, 2)
        self.layout_colors.addWidget(self.combo_color_stock, 0, 3)
        self.layout_colors.addWidget(self.combo_color_buyp, 1, 0)
        self.layout_colors.addWidget(self.combo_color_sellp, 1, 1)
        self.layout_colors.addWidget(self.combo_color_average, 1, 2)
        self.layout_colors.addWidget(self.combo_color_to_buy, 1, 3)

        # WIDGETS PARAMETERS
        self.setWindowTitle("Settings")
        self.setWindowIcon(Utils.get_pixmap("settings_dark"))
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setContentsMargins(10, 10, 10, 10)
        self.layout_left.setAlignment(Qt.AlignTop)
        self.layout_right.setAlignment(Qt.AlignTop)
        self.layout_left.setContentsMargins(15, 15, 15, 15)
        self.layout_right.setContentsMargins(15, 15, 15, 15)

        Utils.resize_font(self.label_title, 2)
        Utils.set_icon(self.button_new_profile, "add_profile", 1)
        Utils.set_icon(self.button_delete_profile, "trash", 1)
        Utils.style_click_button(self.button_new_profile, "#689f38")
        Utils.style_click_button(self.button_delete_profile, "#d32f2f")

        self.combobox_profiles.setCursor(Qt.PointingHandCursor)
        self.button_new_profile.setCursor(Qt.PointingHandCursor)
        self.button_delete_profile.setCursor(Qt.PointingHandCursor)
        self.button_show_ref.setCursor(Qt.PointingHandCursor)
        self.button_show_buyp.setCursor(Qt.PointingHandCursor)
        self.button_show_sellp.setCursor(Qt.PointingHandCursor)
        self.combo_color_reference.setCursor(Qt.PointingHandCursor)
        self.combo_color_text.setCursor(Qt.PointingHandCursor)
        self.combo_color_sells.setCursor(Qt.PointingHandCursor)
        self.combo_color_stock.setCursor(Qt.PointingHandCursor)
        self.combo_color_buyp.setCursor(Qt.PointingHandCursor)
        self.combo_color_sellp.setCursor(Qt.PointingHandCursor)
        self.combo_color_average.setCursor(Qt.PointingHandCursor)
        self.combo_color_to_buy.setCursor(Qt.PointingHandCursor)

        for i in range(len(self.color_list)):
            self.combo_color_reference.addItem("Reference")
            self.combo_color_text.addItem("Name")
            self.combo_color_sells.addItem("Sells")
            self.combo_color_stock.addItem("Stock")
            self.combo_color_buyp.addItem("Buyp")
            self.combo_color_sellp.addItem("Sellp")
            self.combo_color_average.addItem("Average")
            self.combo_color_to_buy.addItem("To buy")

            self.combo_color_reference.setItemData(i, QColor(self.color_list[i]), Qt.BackgroundRole)
            self.combo_color_text.setItemData(i, QColor(self.color_list[i]), Qt.BackgroundRole)
            self.combo_color_sells.setItemData(i, QColor(self.color_list[i]), Qt.BackgroundRole)
            self.combo_color_stock.setItemData(i, QColor(self.color_list[i]), Qt.BackgroundRole)
            self.combo_color_buyp.setItemData(i, QColor(self.color_list[i]), Qt.BackgroundRole)
            self.combo_color_sellp.setItemData(i, QColor(self.color_list[i]), Qt.BackgroundRole)
            self.combo_color_average.setItemData(i, QColor(self.color_list[i]), Qt.BackgroundRole)
            self.combo_color_to_buy.setItemData(i, QColor(self.color_list[i]), Qt.BackgroundRole)

        self.combo_color_reference.setObjectName("Reference")
        self.combo_color_text.setObjectName("Name")
        self.combo_color_sells.setObjectName("Sells")
        self.combo_color_stock.setObjectName("Stock")
        self.combo_color_buyp.setObjectName("Buyp")
        self.combo_color_sellp.setObjectName("Sellp")
        self.combo_color_average.setObjectName("Average")
        self.combo_color_to_buy.setObjectName("ToBuy")

        self.combo_color_reference.setStyleSheet("background-color: {0};".format(self.color_dict["Reference"]))
        self.combo_color_text.setStyleSheet("background-color: {0};".format(self.color_dict["Name"]))
        self.combo_color_sells.setStyleSheet("background-color: {0};".format(self.color_dict["Sells"]))
        self.combo_color_stock.setStyleSheet("background-color: {0};".format(self.color_dict["Stock"]))
        self.combo_color_buyp.setStyleSheet("background-color: {0};".format(self.color_dict["Buyp"]))
        self.combo_color_sellp.setStyleSheet("background-color: {0};".format(self.color_dict["Sellp"]))
        self.combo_color_average.setStyleSheet("background-color: {0};".format(self.color_dict["Average"]))
        self.combo_color_to_buy.setStyleSheet("background-color: {0};".format(self.color_dict["ToBuy"]))

        if self.show_ref:
            self.button_show_ref.setText("Show")
            Utils.style_click_button(self.button_show_ref, "#ffa000")
            Utils.set_icon(self.button_show_ref, "eyeopen", 1)
        else:
            self.button_show_ref.setText("Hide")
            Utils.style_click_button(self.button_show_ref, "#455a64")
            Utils.set_icon(self.button_show_ref, "eyeclose", 1)

        if self.show_buyp:
            self.button_show_buyp.setText("Show")
            Utils.style_click_button(self.button_show_buyp, "#ffa000")
            Utils.set_icon(self.button_show_buyp, "eyeopen", 1)
        else:
            self.button_show_buyp.setText("Hide")
            Utils.style_click_button(self.button_show_buyp, "#455a64")
            Utils.set_icon(self.button_show_buyp, "eyeclose", 1)

        if self.show_sellp:
            self.button_show_sellp.setText("Show")
            Utils.style_click_button(self.button_show_sellp, "#ffa000")
            Utils.set_icon(self.button_show_sellp, "eyeopen", 1)
        else:
            self.button_show_sellp.setText("Hide")
            Utils.style_click_button(self.button_show_sellp, "#455a64")
            Utils.set_icon(self.button_show_sellp, "eyeclose", 1)

        self.combo_color_reference.activated.connect(self.combo_activated)
        self.combo_color_text.activated.connect(self.combo_activated)
        self.combo_color_sells.activated.connect(self.combo_activated)
        self.combo_color_stock.activated.connect(self.combo_activated)
        self.combo_color_buyp.activated.connect(self.combo_activated)
        self.combo_color_sellp.activated.connect(self.combo_activated)
        self.combo_color_average.activated.connect(self.combo_activated)
        self.combo_color_to_buy.activated.connect(self.combo_activated)

        self.button_show_ref.clicked.connect(self.toggle_show_ref)
        self.button_show_buyp.clicked.connect(self.toggle_show_buyp)
        self.button_show_sellp.clicked.connect(self.toggle_show_sellp)
        self.button_delete_profile.clicked.connect(self.delete_clicked)
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
            self.profile_list = tables

        self.combobox_profiles.setCurrentText(self.current_table)

    @Slot(str)
    def profile_selected(self, profile_name):
        self.current_table = profile_name
        self.messager.new_selected_profile.emit(profile_name)

    @Slot()
    def new_profile_clicked(self):
        dialog = NewNameDialog("profile")
        dialog.messager.name_new_profile.connect(self.apply_new_profile_name)
        dialog.exec_()

    @Slot(str)
    def apply_new_profile_name(self, name):
        self.messager.profile_created.emit(name)
        self.current_table = name

        self.combobox_profiles.addItem(name)
        self.combobox_profiles.setCurrentText(name)

    def combo_activated(self, id_color):
        combo = self.sender()
        combo.setStyleSheet("background-color: {0};".format(self.color_list[id_color]))

        self.color_dict[combo.objectName()] = self.color_list[id_color]
        self.messager.update_color_table.emit(self.color_dict)

    @Slot()
    def delete_clicked(self):
        box = QMessageBox(QMessageBox.Warning, "Delete {0}".format(self.current_table), "Do you really want to delete {0} ?".format(self.current_table)
                          , QMessageBox.Yes)
        box.addButton(QMessageBox.No)
        rep = box.exec_()
        if rep == QMessageBox.Yes:
            self.messager.deleted_profile.emit(self.current_table)

            del self.profile_list[self.current_table]

            self.combobox_profiles.clear()
            if len(self.profile_list) == 0:
                self.current_table = "Default"
                self.combobox_profiles.addItem("Default")
            else:
                for key in self.profile_list:
                    self.combobox_profiles.addItem(key)
                for key in self.profile_list:
                    self.current_table = key
                    break

    @Slot()
    def toggle_show_ref(self):
        if self.show_ref:
            self.show_ref = False
            self.button_show_ref.setText("Hide")
            Utils.style_click_button(self.button_show_ref, "#455a64")
            Utils.set_icon(self.button_show_ref, "eyeclose", 1)
        else:
            self.show_ref = True
            self.button_show_ref.setText("Show")
            Utils.style_click_button(self.button_show_ref, "#ffa000")
            Utils.set_icon(self.button_show_ref, "eyeopen", 1)

        self.messager.send_is_show_ref.emit(self.show_ref)

    @Slot()
    def toggle_show_buyp(self):
        if self.show_buyp:
            self.show_buyp = False
            self.button_show_buyp.setText("Hide")
            Utils.style_click_button(self.button_show_buyp, "#455a64")
            Utils.set_icon(self.button_show_buyp, "eyeclose", 1)
        else:
            self.show_buyp = True
            self.button_show_buyp.setText("Show")
            Utils.style_click_button(self.button_show_buyp, "#ffa000")
            Utils.set_icon(self.button_show_buyp, "eyeopen", 1)

        self.messager.send_is_show_buyp.emit(self.show_buyp)

    @Slot()
    def toggle_show_sellp(self):
        if self.show_sellp:
            self.show_sellp = False
            self.button_show_sellp.setText("Hide")
            Utils.style_click_button(self.button_show_sellp, "#455a64")
            Utils.set_icon(self.button_show_sellp, "eyeclose", 1)
        else:
            self.show_sellp = True
            self.button_show_sellp.setText("Show")
            Utils.style_click_button(self.button_show_sellp, "#ffa000")
            Utils.set_icon(self.button_show_sellp, "eyeopen", 1)

        self.messager.send_is_show_sellp.emit(self.show_sellp)
