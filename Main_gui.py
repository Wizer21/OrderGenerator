from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from Data_dialog import *
from Item import *
from TableWidget import *
from Settings import *
from Mail_build import *
import json
from Utils import *

class Main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.current_table = "Default"
        self.current_mail_profile = "Default"
        self.item_list = []
        self.month_count = 0
        self.sustain_value = 2
        self.used_month = 6
        self.color_dict = {
            "Reference": "#546e7a",
            "Name": "#2A363B",
            "Sells": "#fb8c00",
            "Stock": "#1e88e5",
            "Average": "#5e35b1",
            "ToBuy": "#e53935"
        }
        self.name_columun_end = False
        self.show_ref = True

        self.menubar_main = QMenuBar(self)
        self.action_options = QAction("Settings")

        self.widget_main = QWidget(self)
        self.layout_main = QGridLayout(self)

        self.layout_top_panel = QGridLayout(self)
        self.label_selected_profile = QLabel(self.current_table, self)
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
        self.load_settings()
        self.load_tables()

        if len(self.item_list) != 0:
            self.build_table()
            self.calc_order()

        self.resize(1000, 800)

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
        self.setWindowTitle("Table")
        self.setWindowIcon(Utils.get_pixmap("logo"))
        Utils.resize_font(self.label_selected_profile, 2)
        Utils.set_icon(self.button_generate_mail, "mail", 2)
        Utils.set_icon(self.button_import_data, "import_data", 2)

        self.widget_main.setContentsMargins(10, 10, 10, 10)
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
        self.button_generate_mail.clicked.connect(self.mail_generation_clicked)

    @Slot()
    def import_data_clicked(self):
        dialog = Data_dialog()
        dialog.messager.send_table.connect(self.apply_new_list)
        dialog.exec_()

    @Slot()
    def apply_new_list(self, new_dict):
        push_if_new_item = new_dict["Add Items"]
        ref = new_dict["Reference"]
        names = new_dict["Name"]
        lists = new_dict["Sells"]
        stock = new_dict["Stock"]

        if len(stock) == 0:
            has_stock = False
        else:
            has_stock = True

        if len(ref) == 0:
            has_ref = False
        else:
            has_ref = True

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
                    if has_ref:
                        self.item_list[y].reference = ref[i]
                    new_item = True
                    continue

            if push_if_new_item and not new_item:  # IF NEW ITEMS IS NEW
                self.item_list.insert(0, Item(names[i], self.month_count))
                for z in lists:  # For every list
                    self.item_list[0].sells_history.append(z[i])  # Push the val at i
                if has_ref:
                    self.item_list[0].reference = ref[i]
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

        if self.name_columun_end:
            namepos = sells_count + 2
            sellspos = 0
        else:
            namepos = 0
            sellspos = 1
        if self.show_ref:
            ref_pos = 1
        else:
            ref_pos = 0
        stockpos = sellspos + sells_count + ref_pos
        averagepos = stockpos + 1
        buypos = sells_count + 3 + ref_pos

        position_dict = {
            "name": namepos + ref_pos,
            "startsells": sellspos + ref_pos,
            "stock": stockpos,
            "average": averagepos,
            "tobuy": buypos
        }

        self.table_widget_main.setColumnCount(sells_count + 4 + ref_pos)  # +4 for column name/stock/average/ordervalue

        for i in range(len(self.item_list)):  # EVERY ROW
            name = QTableWidgetItem(self.item_list[i].name)
            name.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
            name.setBackgroundColor(QColor(self.color_dict["Name"]))

            column = position_dict["startsells"]
            self.table_widget_main.setItem(i, position_dict["name"], name)  # FILL NAME COLUMN

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
            self.table_widget_main.setItem(i, position_dict["stock"], stock)

        headers = []
        if self.show_ref:
            headers.append("Reference")
        if not self.name_columun_end:
            headers.append("Name")
        for i in range(0, sells_count):
            headers.append("Sells")
        headers.append("Stock")
        headers.append("Average\nSells")
        if self.name_columun_end:
            headers.append("Name")
        headers.append("To Buy")
        self.table_widget_main.setHorizontalHeaderLabels(headers)
        self.table_widget_main.resizeColumnsToContents()

    def calc_order(self):
        calc_month = self.used_month

        column_count = self.table_widget_main.columnCount()
        if self.name_columun_end:
            pos_column_average = column_count - 3
        else:
            pos_column_average = column_count - 2

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
            self.table_widget_main.setItem(i, pos_column_average, value)

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

            self.item_list[i].to_buy = to_buy
            value.setBackgroundColor(QColor(self.color_dict["ToBuy"]))
            value.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
            self.table_widget_main.setItem(i, column_count - 1, value)
            self.table_widget_main.resizeColumnsToContents()

            self.table_widget_main.columnMoved(1, 0, column_count - 2)

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

        sett = Settings(self.color_dict, self.name_columun_end, self.show_ref)
        sett.messager.new_selected_profile.connect(self.apply_new_profile_selected)
        sett.messager.profile_created.connect(self.apply_created_profile)
        sett.messager.deleted_profile.connect(self.apply_deleted_profile)
        sett.messager.update_color_table.connect(self.update_color_table)
        sett.messager.send_name_position.connect(self.set_name_position)
        sett.messager.send_is_show_ref.connect(self.set_show_ref)
        sett.exec_()

    def load_settings(self):
        try:
            with open(".\\files\\settings.json", "r") as data_json:  # LOAD SETTINGS
                settings = json.load(data_json)
                self.current_table = settings["lasttable"]
                self.month_count = settings["monthcount"]
                self.sustain_value = settings["sustain"]
                self.used_month = settings["usedmonth"]
                self.color_dict = settings["colors"]
                self.current_mail_profile = settings["mailprofile"]
                self.name_columun_end = settings["nameend"]
                self.show_ref = settings["showref"]
                self.update_displayed_settings()
        except FileNotFoundError:  # DEFAULT SETTINGS
            self.save_settings()

    def load_tables(self):
        try:
            with open(".\\files\\tables.json", "r") as data_json:  # LOAD TABLES
                tables = json.load(data_json)
                self.import_items_list(tables)

        except FileNotFoundError:  # ELSE PUSH DEFAULT TABLE
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
            "usedmonth": self.used_month,
            "colors": self.color_dict,
            "mailprofile": self.current_mail_profile,
            "nameend": self.name_columun_end,
            "showref": self.show_ref
        }
        with open(".\\files\\settings.json", "w") as data_json:
            json.dump(settings, data_json)

    @Slot(str)
    def apply_new_profile_selected(self, new_profile_name):
        self.current_table = new_profile_name
        self.label_selected_profile.setText(new_profile_name)
        self.load_tables()

        if len(self.item_list) != 0:  # REFRESH TABLE
            self.build_table()
            self.calc_order()
        else:
            self.reset_table()

    @Slot(str)
    def apply_created_profile(self, new_profile_name):
        self.current_table = new_profile_name
        self.label_selected_profile.setText(new_profile_name)

        self.add_table_to_json(new_profile_name)
        self.load_tables()
        self.month_count = 0
        if len(self.item_list) != 0:  # REFRESH TABLE
            self.build_table()
            self.calc_order()
        else:
            self.reset_table()

    @Slot(str)
    def apply_deleted_profile(self, profile_name):
        with open(".\\files\\tables.json", "r") as data_json:
            tables_list = json.load(data_json)

        del tables_list[profile_name]

        if self.current_table == profile_name:
            self.item_list.clear()
            if len(tables_list) > 0:
                for key in tables_list:
                    self.current_table = key
                    break
                self.import_items_list(tables_list)
            else:
                items = {
                }
                tables_list = {
                    "Default": items
                }
                self.current_table = "Default"

        with open(".\\files\\tables.json", "w") as data_json:
            json.dump(tables_list, data_json)

        self.label_selected_profile.setText(self.current_table)
        if len(self.item_list) != 0:  # REFRESH TABLE
            self.build_table()
            self.calc_order()
        else:
            self.reset_table()

    def import_items_list(self, tables_list):
        self.item_list.clear()

        for key in tables_list[self.current_table]:  # PUSH ITEMS TO ITEM LIST
            item = Item(key, 0)
            item.sells_history = tables_list[self.current_table][key]["sells"]
            item.stock = tables_list[self.current_table][key]["stock"]
            self.item_list.append(item)

        for key in tables_list[self.current_table]:
            self.month_count = len(tables_list[self.current_table][key]["sells"])
            break

    def add_table_to_json(self, talbe_name):
        with open(".\\files\\tables.json", "r") as data_json:
            tables = json.load(data_json)

            items = {
            }
            tables[talbe_name] = items

            with open(".\\files\\tables.json", "w") as data_json:
                json.dump(tables, data_json)

    def update_displayed_settings(self):
        self.label_selected_profile.setText(self.current_table)
        self.line_edit_sustain.setText(str(self.sustain_value))
        self.line_edit_base_month.setText(str(self.used_month))

    @Slot(dict)
    def update_color_table(self, new_color_dict):
        self.color_dict = new_color_dict
        if len(self.item_list) != 0:  # REFRESH TABLE
            self.build_table()
            self.calc_order()

    @Slot()
    def mail_generation_clicked(self):
        mail = Mail_build(self.item_list, self.current_mail_profile)
        mail.messager.mail_used_changed.connect(self.apply_name_mail_profile)
        mail.exec_()

    @Slot(str)
    def apply_name_mail_profile(self, new_name):
        self.current_mail_profile = new_name

    def reset_table(self):
        self.table_widget_main.clear()
        self.table_widget_main.setColumnCount(0)
        self.table_widget_main.setRowCount(0)

    @Slot(bool)
    def set_name_position(self, is_name_at_the_end):
        self.name_columun_end = is_name_at_the_end
        if len(self.item_list) != 0:  # REFRESH TABLE
            self.build_table()
            self.calc_order()

    @Slot(bool)
    def set_show_ref(self, is_ref_show):
        self.show_ref = is_ref_show
        if len(self.item_list) != 0:  # REFRESH TABLE
            self.build_table()
            self.calc_order()

    def closeEvent(self, event):
        self.save_settings()
        self.save_table()


