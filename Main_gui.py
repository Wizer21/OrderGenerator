from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from Data_dialog import *
from Item import *
from TableWidget import *

class Main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.item_list = []
        self.month_count = 0
        self.sustain_value = 2

        self.widget_main = QWidget(self)
        self.layout_main = QGridLayout(self)

        self.layout_top_panel = QHBoxLayout(self)
        self.label_selected_profile = QLabel("Test Profile", self)
        self.button_import_data = QPushButton("Import Data", self)
        self.button_generate_mail = QPushButton("Generate Mail", self)
        self.label_sustain_wanted = QLabel("Sustain - Months", self)
        self.line_edit_sustain = QLineEdit(str(self.sustain_value), self)

        self.table_widget_main = QTableWidget(self)

        self.build()


    def build(self):
        # STRUCTURE
        self.setCentralWidget(self.widget_main)
        self.widget_main.setLayout(self.layout_main)

        self.layout_main.addLayout(self.layout_top_panel, 0, 0)
        self.layout_top_panel.addWidget(self.label_selected_profile)
        self.layout_top_panel.addWidget(self.button_import_data)
        self.layout_top_panel.addWidget(self.button_generate_mail)
        self.layout_top_panel.addWidget(self.label_sustain_wanted)
        self.layout_top_panel.addWidget(self.line_edit_sustain)

        self.layout_main.addWidget(self.table_widget_main, 1, 0)

        # WIDGETS PARAMETERS
        self.table_widget_main.setSortingEnabled(True)
        self.button_import_data.setCursor(Qt.PointingHandCursor)
        self.button_generate_mail.setCursor(Qt.PointingHandCursor)

        self.button_import_data.clicked.connect(self.import_data_clicked)
        self.line_edit_sustain.textEdited.connect(self.apply_new_sustain_value)


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


    def build_table(self):
        self.table_widget_main.clear()

        sells_count = len(self.item_list[0].sells_history)
        self.table_widget_main.setRowCount(len(self.item_list))
        self.table_widget_main.setColumnCount(sells_count + 4)  # +4 for column name/stock/average/ordervalue

        for i in range(len(self.item_list)):  # EVERY ROW
            name = QTableWidgetItem(self.item_list[i].name)
            name.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)

            self.table_widget_main.setItem(i, 0, name)  # FILL NAME COLUMN
            column = 1

            for y in range(len(self.item_list[i].sells_history)):  # FILL SELLS COLUMN
                val = self.item_list[i].sells_history[y]
                if val == 0:
                    sells = QTableWidgetItem(str(val))
                else:
                    sells = TableWidgetItem(str(val))

                sells.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)
                self.table_widget_main.setItem(i, column, sells)
                column += 1

            stock = TableWidgetItem(str(self.item_list[i].stock))  # FILL STOCK COLUMN
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

        self.calc_order()


    def calc_order(self):
        calc_month = 6
        pos_column_average = self.table_widget_main.columnCount() - 1

        if self.month_count < calc_month:
            calc_month = self.month_count

        for i in range(len(self.item_list)):
            my_list = self.item_list[i].sells_history
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
            self.table_widget_main.setItem(i, pos_column_average, value)


    @Slot(str)
    def apply_new_sustain_value(self, str_value):
        if str_value == "":
            self.sustain_value = 0
        else:
            self.sustain_value = float(str_value)
        self.build_table()