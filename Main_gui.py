from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from Data_dialog import *
from Item import *
from TableWidget import *
from Settings import *
import json

class Main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.current_table = "Default"
        self.item_list = []
        self.month_count = 0
        self.sustain_value = 2
        self.used_month = 6
        self.color_dict = {
            "Name": "#2A363B",
            "Sells": "#E84A5F",
            "Reference": "",
            "Stock": "#FF847C",
            "Average": "#FECEA8",
            "ToBuy": "#99B989"
        }
        self.settings_changed = False

        self.menubar_main = QMenuBar(self)
        self.action_options = QAction("Options")

        self.widget_main = QWidget(self)
        self.layout_main = QGridLayout(self)

        self.layout_top_panel = QGridLayout(self)
        self.label_selected_profile = QLabel("Test Profile", self)
        self.button_import_data = QPushButton("Import\nData", self)
        self.button_generate_mail = QPushButton("Generate\nMail", self)
        self.label_sustain_wanted = QLabel("Buy for ", self)
        self.label_based_month = QLabel("Based on last ", self)
        self.line_edit_sustain = QLineEdit(str(self.sustain_value), self)
        self.line_edit_base_month = QLineEdit(str(self.used_month), self)
        self.label_sustain_step = QLabel("month", self)
        self.label_based_step = QLabel("month", self)

        self.table_widget_main = QTableWidget(self)

        self.build()
        self.load_files()


    def build(self):
        # STRUCTURE
        self.setMenuBar(self.menubar_main)
        self.menubar_main.addAction(self.action_options)

        self.setCentralWidget(self.widget_main)
        self.widget_main.setLayout(self.layout_main)

        self.layout_main.addLayout(self.layout_top_panel, 0, 0)
        self.layout_top_panel.addWidget(self.label_selected_profile, 0, 0, 2, 1)
        self.layout_top_panel.addWidget(self.button_import_data, 0, 1, 2, 1)
        self.layout_top_panel.addWidget(self.button_generate_mail, 0, 2, 2, 1)
        self.layout_top_panel.addWidget(self.label_sustain_wanted, 0, 3, 1, 1, Qt.AlignRight)
        self.layout_top_panel.addWidget(self.line_edit_sustain, 0, 4, 1, 1)
        self.layout_top_panel.addWidget(self.label_sustain_step, 0, 5, 1, 1)
        self.layout_top_panel.addWidget(self.label_based_month, 1, 3, 1, 1, Qt.AlignRight)
        self.layout_top_panel.addWidget(self.line_edit_base_month, 1, 4, 1, 1)
        self.layout_top_panel.addWidget(self.label_based_step, 1, 5, 1, 1)

        self.layout_main.addWidget(self.table_widget_main, 1, 0)

        # WIDGETS PARAMETERS
        self.table_widget_main.setSortingEnabled(True)
        self.button_import_data.setCursor(Qt.PointingHandCursor)
        self.button_generate_mail.setCursor(Qt.PointingHandCursor)
        self.button_import_data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_generate_mail.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        reg_exp = QRegExpValidator("[+-]?([0-9]*[.])?[0-9]+")
        self.line_edit_sustain.setValidator(reg_exp)
        int_only = QIntValidator()
        self.line_edit_base_month.setValidator(int_only)

        self.action_options.triggered.connect(self.open_options)
        self.button_import_data.clicked.connect(self.import_data_clicked)
        self.line_edit_sustain.textEdited.connect(self.apply_new_sustain_value)
        self.line_edit_base_month.textEdited.connect(self.apply_new_base_value)


    @Slot()
    def import_data_clicked(self):
        dialog = Data_dialog()
        dialog.messager.send_table.connect(self.apply_new_list)
        dialog.exec_()


    @Slot()
    def apply_new_list(self, new_dict):
        push_if_new_item = new_dict["Add Items"]
        names = new_dict["Name"]
        lists = new_dict["Sells"]
        stock = new_dict["Stock"]
        if len(stock) == 0:
            has_stock = False
        else:
            has_stock = True

        try:
            added_months = len(lists)
        except IndexError:
            added_months = 0

        new_item = False
        i = 0
        while i < len(names):  # CHECK EVERY NEW ITEMS
            new_item = False

            for y in range(len(self.item_list)):  # CHECK CURRENT ITEMS
                if self.item_list[y].name == names[i]:  # IF NEW ITEMS ALREADY EXIST
                    for z in lists:  # For every list
                        self.item_list[y].sells_history.append(z[i])  # Push the val at i
                    new_item = True
                    continue

            if push_if_new_item and not new_item:  # IF NEW ITEMS IS NEW
                self.item_list.insert(0, Item(names[i], self.month_count))
                for z in lists:  # For every list
                    self.item_list[0].sells_history.append(z[i])  # Push the val at i
            i += 1

        item_not_refreshed = False  # FIND ITEM THAT EXIST BUT ARE NOT ACTUALISED
        for i in range(len(self.item_list)):  # EVERY OLD ITEMS
            item_not_refreshed = False
            for y in range(len(names)):  # EVERY NEW ITEMS
                if self.item_list[i].name == names[y]:  # MATCH A NEW ONE
                    if has_stock:
                        self.item_list[i].stock = stock[y]  # SET STOCK
                    item_not_refreshed = True
                    break

            if not item_not_refreshed:  # PUSH NULL VALUES TO UNREFRESHED ITEMS
                for y in range(0, added_months):
                    self.item_list[i].sells_history.append(0)

        self.month_count += added_months
        self.build_table()
        self.calc_order()
        self.save_table()


    def build_table(self):
        self.table_widget_main.clear()

        sells_count = len(self.item_list[0].sells_history)
        self.table_widget_main.setRowCount(len(self.item_list))
        self.table_widget_main.setColumnCount(sells_count + 4)  # +4 for column name/stock/average/ordervalue

        for i in range(len(self.item_list)):  # EVERY ROW
            name = QTableWidgetItem(self.item_list[i].name)
            name.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
            name.setBackgroundColor(QColor(self.color_dict["Name"]))

            self.table_widget_main.setItem(i, 0, name)  # FILL NAME COLUMN
            column = 1

            for y in range(len(self.item_list[i].sells_history)):  # FILL SELLS COLUMN
                val = self.item_list[i].sells_history[y]
                if val == 0:
                    sells = QTableWidgetItem(str(val))
                else:
                    sells = TableWidgetItem(str(val))

                sells.setBackgroundColor(QColor(self.color_dict["Sells"]))
                sells.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
                self.table_widget_main.setItem(i, column, sells)
                column += 1

            stock = TableWidgetItem(str(self.item_list[i].stock))  # FILL STOCK COLUMN

            stock.setBackgroundColor(QColor(self.color_dict["Stock"]))
            stock.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
            self.table_widget_main.setItem(i, column, stock)

        headers = ["Name"]
        for i in range(0, sells_count):
            headers.append("Sells")
        headers.append("Stock")
        headers.append("Average\nSells")
        headers.append("To Buy")
        self.table_widget_main.setHorizontalHeaderLabels(headers)
        self.table_widget_main.resizeColumnsToContents()

    def calc_order(self):
        calc_month = self.used_month
        pos_column_average = self.table_widget_main.columnCount() - 1

        if self.month_count < calc_month:
            calc_month = self.month_count

        for i in range(len(self.item_list)):
            my_list = self.item_list[i].sells_history.copy()
            my_list.reverse()
            average = 0

            for y in range(0, calc_month):
                average += my_list[y]
            average = average / calc_month

            self.item_list[i].monthly_sells = average
            to_buy = (average * self.sustain_value) - self.item_list[i].stock

            if 0 < average < 1:
                average = round(average, 2)
            elif average < 0:
                average = 0
            else:
                average = int(average)

            if average == 0:
                value = QTableWidgetItem(str(average))
            else:
                value = TableWidgetItem(str(average))

            value.setBackgroundColor(QColor(self.color_dict["Average"]))
            value.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
            self.table_widget_main.setItem(i, pos_column_average - 1, value)

            if 0 < to_buy < 1:
                to_buy = round(to_buy, 2)
            elif to_buy < 0:
                to_buy = 0
            else:
                to_buy = int(to_buy)

            if to_buy == 0:
                value = QTableWidgetItem(str(to_buy))
            else:
                value = TableWidgetItem(str(to_buy))

            value.setBackgroundColor(QColor(self.color_dict["ToBuy"]))
            value.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
            self.table_widget_main.setItem(i, pos_column_average, value)
            self.table_widget_main.resizeColumnsToContents()

    @Slot(str)
    def apply_new_sustain_value(self, str_value):
        if str_value == "":
            self.sustain_value = 0
        else:
            self.sustain_value = float(str_value)

        if len(self.item_list) != 0:
            self.build_table()
            self.calc_order()

    @Slot(str)
    def apply_new_base_value(self, value):
        if value == "" or value == "0":
            self.used_month = 1
        else:
            self.used_month = int(value)

        if len(self.item_list) != 0:
            self.build_table()
            self.calc_order()

    @Slot()
    def open_options(self):
        self.save_settings()
        self.save_table()

        sett = Settings()
        sett.messager.new_selected_profile.connect(self.apply_new_profile_selected)
        sett.messager.profile_created.connect(self.apply_created_profile)
        sett.exec_()

        if self.settings_changed and len(self.item_list) != 0:
            self.build_table()
            self.calc_order()

        self.settings_changed = False

    def load_files(self):
        try:
            with open(".\\files\\settings.json", "r") as data_json:
                settings = json.load(data_json)
                self.current_table = settings["lasttable"]
                self.month_count = settings["monthcount"]
                self.sustain_value = settings["sustain"]
                self.used_month = settings["usedmonth"]
                self.label_selected_profile.setText(self.current_table)
        except FileNotFoundError:
            settings = {
                "lasttable": self.current_table,
                "monthcount": self.month_count,
                "sustain": self.sustain_value,
                "usedmonth": self.used_month
            }
            with open(".\\files\\settings.json", "w") as data_json:
                json.dump(settings, data_json)

        try:
            with open(".\\files\\tables.json", "r") as data_json:
                tables = json.load(data_json)

                for key in tables[self.current_table]:
                    item = Item(key, 0)
                    item.sells_history = tables[self.current_table][key]["sells"]
                    item.stock = tables[self.current_table][key]["stock"]
                    self.item_list.append(item)

                if len(self.item_list) != 0:
                    self.build_table()
                    self.calc_order()

        except FileNotFoundError:
            items = {
            }
            tables = {
                "Default": items
            }
            with open(".\\files\\tables.json", "w") as data_json:
                json.dump(tables, data_json)

    def save_table(self):
        with open(".\\files\\tables.json", "r") as data_json:
            tables = json.load(data_json)

        for i in range(len(self.item_list)):
            new_dict = {
                "sells": self.item_list[i].sells_history,
                "stock": self.item_list[i].stock
            }
            tables[self.current_table][self.item_list[i].name] = new_dict

        with open(".\\files\\tables.json", "w") as data_json:
            json.dump(tables, data_json)

    def save_settings(self):
        settings = {
            "lasttable": self.current_table,
            "monthcount": self.month_count,
            "sustain": self.sustain_value,
            "usedmonth": self.used_month
        }
        with open(".\\files\\settings.json", "w") as data_json:
            json.dump(settings, data_json)

    @Slot(str)
    def apply_new_profile_selected(self, new_profile_name):
        self.current_table = new_profile_name
        self.label_selected_profile.setText(new_profile_name)
        self.settings_changed = True

    @Slot(str)
    def apply_created_profile(self, new_profile_name):
        self.current_table = new_profile_name
        self.settings_changed = True
        self.label_selected_profile.setText(new_profile_name)

        with open(".\\files\\tables.json", "r") as data_json:
            tables = json.load(data_json)

            items = {
            }
            tables[new_profile_name] = items

            with open(".\\files\\tables.json", "w") as data_json:
                json.dump(tables, data_json)

    def closeEvent(self, event):
        self.save_settings()
        self.save_table()