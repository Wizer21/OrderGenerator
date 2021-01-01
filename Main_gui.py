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
            "Buyp": "#7cb342",
            "Sellp": "#00897b",
            "Average": "#5e35b1",
            "ToBuy": "#e53935"
        }
        self.name_columun_end = False
        self.show_ref = True
        self.show_buyp = True
        self.show_sellp = True

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

        self.widget_foot = QWidget(self)
        self.layout_foot = QGridLayout(self)
        self.label_total_buyp = QLabel("BuyP", self)
        self.label_display_buyp = QLabel("0", self)
        self.label_total_sellP = QLabel("SellP", self)
        self.label_display_sellP = QLabel("0", self)
        self.label_margin = QLabel("Margin", self)
        self.label_display_margin = QLabel("0", self)

        self.table_widget_main = QTableWidget(self)
        self.headers = self.table_widget_main.horizontalHeader()

        self.build()
        self.load_settings()
        self.load_tables()
        if len(self.item_list) != 0:
            self.build_table()
            self.calc_order()
            self.refresh_prices_values()

        Utils.resize_from_resolution(self, 0.6, 0.6)

    def build(self):
        # STRUCTURE
        self.setMenuBar(self.menubar_main)
        self.menubar_main.addAction(self.action_options)

        self.setCentralWidget(self.widget_main)
        self.widget_main.setLayout(self.layout_main)

        self.layout_main.addLayout(self.layout_top_panel, 0, 0)
        self.layout_top_panel.addWidget(self.label_selected_profile, 0, 0, 2, 1, Qt.AlignLeft)
        self.layout_top_panel.addWidget(self.button_import_data, 0, 1, 2, 1, Qt.AlignRight)
        self.layout_top_panel.addWidget(self.button_generate_mail, 0, 2, 2, 1, Qt.AlignRight)
        self.layout_top_panel.addWidget(self.label_sustain_wanted, 0, 3, 1, 1, Qt.AlignRight)
        self.layout_top_panel.addWidget(self.line_edit_sustain, 0, 4, 1, 1, Qt.AlignRight)
        self.layout_top_panel.addWidget(self.label_sustain_step, 0, 5, 1, 1, Qt.AlignRight)
        self.layout_top_panel.addWidget(self.label_based_month, 1, 3, 1, 1, Qt.AlignRight)
        self.layout_top_panel.addWidget(self.line_edit_base_month, 1, 4, 1, 1, Qt.AlignRight)
        self.layout_top_panel.addWidget(self.label_based_step, 1, 5, 1, 1, Qt.AlignRight)

        self.layout_main.addWidget(self.table_widget_main, 1, 0)

        self.layout_main.addWidget(self.widget_foot, 2, 0)
        self.widget_foot.setLayout(self.layout_foot)
        self.layout_foot.addWidget(self.label_total_buyp, 0, 0, Qt.AlignRight)
        self.layout_foot.addWidget(self.label_display_buyp, 0, 1, Qt.AlignLeft)
        self.layout_foot.addWidget(self.label_total_sellP, 0, 2, Qt.AlignRight)
        self.layout_foot.addWidget(self.label_display_sellP, 0, 3, Qt.AlignLeft)
        self.layout_foot.addWidget(self.label_margin, 0, 4, Qt.AlignRight)
        self.layout_foot.addWidget(self.label_display_margin, 0, 5, Qt.AlignLeft)

        # WIDGETS PARAMETERS
        self.setWindowTitle("Table")
        self.setWindowIcon(Utils.get_pixmap("logo"))
        self.layout_top_panel.setColumnStretch(0, 1)
        self.widget_main.setContentsMargins(10, 10, 10, 10)

        Utils.resize_font(self.label_selected_profile, 2.5)
        Utils.set_icon(self.button_generate_mail, "mail", 2)
        Utils.set_icon(self.button_import_data, "import_data", 2)
        Utils.style_click_button(self.button_import_data, "#ffa000")
        Utils.style_click_button(self.button_generate_mail, "#1976d2")
        Utils.main_menu_button_size(self.button_import_data, 0.08)
        Utils.main_menu_button_size(self.button_generate_mail, 0.08)
        Utils.resize_font(self.label_display_buyp, 2)
        Utils.resize_font(self.label_display_sellP, 2)
        Utils.resize_font(self.label_display_margin, 2)

        self.headers.setCursor(Qt.PointingHandCursor)
        self.button_import_data.setCursor(Qt.PointingHandCursor)
        self.button_generate_mail.setCursor(Qt.PointingHandCursor)

        self.table_widget_main.setSortingEnabled(True)
        self.headers.setSectionsMovable(True)

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
        dialog = Data_dialog(self.color_dict)
        dialog.messager.send_table.connect(self.apply_new_list)
        dialog.exec_()

    @Slot()
    def apply_new_list(self, new_dict):
        push_if_new_item = new_dict["Add Items"]
        ref = new_dict["Reference"]
        names = new_dict["Name"]
        lists = new_dict["Sells"]
        stock = new_dict["Stock"]
        buyp = new_dict["Buyprice"]
        sellp = new_dict["Sellprice"]

        if len(stock) == 0:
            has_stock = False
        else:
            has_stock = True

        if len(ref) == 0:
            has_ref = False
        else:
            has_ref = True

        if len(buyp) == 0:
            has_buyp = False
        else:
            has_buyp = True

        if len(sellp) == 0:
            has_sellp = False
        else:
            has_sellp = True

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
                    if has_buyp:
                        self.item_list[y].buy_price = buyp[i]
                    if has_sellp:
                        self.item_list[y].sell_price = sellp[i]
                    new_item = True
                    continue

            if push_if_new_item and not new_item:  # IF NEW ITEMS IS NEW
                self.item_list.insert(0, Item(names[i], self.month_count))
                for z in lists:  # For every list
                    self.item_list[0].sells_history.append(z[i])  # Push the val at i
                if has_ref:
                    self.item_list[0].reference = ref[i]
                if has_buyp:
                    self.item_list[0].buy_price = buyp[i]
                if has_sellp:
                    self.item_list[0].sell_price = sellp[i]
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
        self.reset_table()
        self.save_table()

    def build_table(self):
        self.table_widget_main.clear()

        sells_count = len(self.item_list[0].sells_history)
        self.table_widget_main.setRowCount(len(self.item_list))

        count = 0
        if self.show_ref:
            count += 1
        if self.show_buyp:
            count += 1
        if self.show_sellp:
            count += 1

        self.table_widget_main.setColumnCount(sells_count + count + 4)  # +4 for column name/stock/average/ordervalue

        for i in range(len(self.item_list)):  # EVERY ROW
            column = 0
            if self.show_ref:
                ref = QTableWidgetItem(self.item_list[i].reference)
                ref.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
                ref.setBackgroundColor(QColor(self.color_dict["Reference"]))

                self.table_widget_main.setItem(i, column, ref)
                column += 1

            name = QTableWidgetItem(self.item_list[i].name)
            name.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
            name.setBackgroundColor(QColor(self.color_dict["Name"]))

            self.table_widget_main.setItem(i, column, name)  # FILL NAME COLUMN
            column += 1

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
            column += 1

            if self.show_buyp:
                buy = QTableWidgetItem(str(self.item_list[i].buy_price))
                buy.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
                buy.setBackgroundColor(QColor(self.color_dict["Buyp"]))

                self.table_widget_main.setItem(i, column, buy)
                column += 1

            if self.show_sellp:
                sell = QTableWidgetItem(str(self.item_list[i].sell_price))
                sell.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
                sell.setBackgroundColor(QColor(self.color_dict["Sellp"]))

                self.table_widget_main.setItem(i, column, sell)
                column += 1

        headers = []
        if self.show_ref:
            headers.append("Reference")
        headers.append("Name")
        for i in range(0, sells_count):
            headers.append("Sells")
        headers.append("Stock")
        if self.show_buyp:
            headers.append("Buy P.")
        if self.show_sellp:
            headers.append("Sell P.")
        headers.append("Average\nSells")
        headers.append("To Buy")
        self.table_widget_main.setHorizontalHeaderLabels(headers)
        self.table_widget_main.resizeColumnsToContents()

    def calc_order(self):
        calc_month = self.used_month

        column_count = self.table_widget_main.columnCount()

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
            self.table_widget_main.setItem(i, column_count - 2, value)

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

        self.reset_table()

    @Slot(str)
    def apply_new_base_value(self, value):
        if value == "" or value == "0":
            self.used_month = 1
        else:
            self.used_month = int(value)

        self.reset_table()

    @Slot()
    def open_options(self):
        self.save_settings()
        self.save_table()

        sett = Settings(self.color_dict, self.show_ref, self.show_buyp, self.show_sellp)
        sett.messager.new_selected_profile.connect(self.apply_new_profile_selected)
        sett.messager.profile_created.connect(self.apply_created_profile)
        sett.messager.deleted_profile.connect(self.apply_deleted_profile)
        sett.messager.update_color_table.connect(self.update_color_table)
        sett.messager.send_is_show_ref.connect(self.set_show_ref)
        sett.messager.send_is_show_buyp.connect(self.set_show_buyp)
        sett.messager.send_is_show_sellp.connect(self.set_show_sellp)
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
                self.show_ref = settings["showref"]
                self.show_buyp = settings["showbuy"]
                self.show_sellp = settings["showsell"]
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
                "stock": self.item_list[i].stock,
                "ref": self.item_list[i].reference,
                "buyp": self.item_list[i].buy_price,
                "sellp": self.item_list[i].sell_price
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
            "showref": self.show_ref,
            "showbuy": self.show_buyp,
            "showsell": self.show_sellp
        }
        with open(".\\files\\settings.json", "w") as data_json:
            json.dump(settings, data_json)

    @Slot(str)
    def apply_new_profile_selected(self, new_profile_name):
        self.current_table = new_profile_name
        self.label_selected_profile.setText(new_profile_name)
        self.load_tables()

        self.reset_table()

    @Slot(str)
    def apply_created_profile(self, new_profile_name):
        self.current_table = new_profile_name
        self.label_selected_profile.setText(new_profile_name)

        self.add_table_to_json(new_profile_name)
        self.load_tables()
        self.month_count = 0
        self.reset_table()

    @Slot(str)
    def apply_deleted_profile(self, profile_name):
        with open(".\\files\\tables.json", "r") as data_json:
            tables_list = json.load(data_json)

        del tables_list[profile_name]

        if self.current_table == profile_name:
            self.month_count = 0
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
        self.reset_table()

    def import_items_list(self, tables_list):
        self.item_list.clear()

        for key in tables_list[self.current_table]:  # PUSH ITEMS TO ITEM LIST
            item = Item(key, 0)
            item.sells_history = tables_list[self.current_table][key]["sells"]
            item.stock = tables_list[self.current_table][key]["stock"]
            item.reference = tables_list[self.current_table][key]["ref"]
            item.buy_price = tables_list[self.current_table][key]["buyp"]
            item.sell_price = tables_list[self.current_table][key]["sellp"]
            self.item_list.append(item)

        self.month_count = 0
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
        self.reset_table()

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
        if len(self.item_list) != 0:  # REFRESH TABLE
            self.build_table()
            self.calc_order()
            self.refresh_prices_values()

    @Slot(bool)
    def set_name_position(self, is_name_at_the_end):
        self.name_columun_end = is_name_at_the_end
        self.reset_table()

    @Slot(bool)
    def set_show_ref(self, is_ref_show):
        self.show_ref = is_ref_show
        self.reset_table()

    @Slot(bool)
    def set_show_buyp(self, is_buyp_show):
        self.show_buyp = is_buyp_show
        self.reset_table()

    @Slot(bool)
    def set_show_sellp(self, is_sellp_show):
        self.show_sellp = is_sellp_show
        self.reset_table()

    def refresh_prices_values(self):
        if self.show_buyp or self.show_sellp:
            self.widget_foot.setVisible(True)
            total_buyp = 0
            total_sellp = 0

            for i in self.item_list:
                total_buyp += i.buy_price * i.to_buy
                total_sellp += i.sell_price * i.to_buy

            self.label_display_buyp.setText(str(round(total_buyp, 2)))
            self.label_display_sellP.setText(str(round(total_sellp, 2)))
            self.label_display_margin.setText(str(round(total_sellp - total_buyp, 2)))
        else:
            self.widget_foot.setVisible(False)

    def closeEvent(self, event):
        self.save_settings()
        self.save_table()


