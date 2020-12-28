from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from Data_dialog import *
from Item import *


class Main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.item_list = []
        self.month_count = 0

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
        self.button_import_data.clicked.connect(self.import_data_clicked)
        self.button_import_data.setCursor(Qt.PointingHandCursor)
        self.button_generate_mail.setCursor(Qt.PointingHandCursor)


    @Slot()
    def import_data_clicked(self):
        dialog = Data_dialog()
        dialog.messager.send_table.connect(self.apply_new_list)
        dialog.exec_()


    @Slot()
    def apply_new_list(self, new_dict):
        push_if_new_item = new_dict["Add Items"]
        names = new_dict["Name"][0]
        lists = new_dict["Sells"]

        try:
            added_months = len(lists[0][0])
        except IndexError:
            added_months = 0

        new_item = False
        i = 0
        while i < len(names):  # CHECK EVERY NEW ITEMS
            new_item = False

            for y in range(len(self.item_list)):  # CHECK CURRENT ITEMS
                if self.item_list[y].name == names[i]:  # IF NEW ITEMS ALREADY EXIST
                    for z in lists:  # For every list
                        self.item_list[y].add_month(z[i])  # Push the val at i
                    new_item = True
                    continue

            if push_if_new_item and not new_item:  # IF NEW ITEMS IS NEW
                self.item_list.insert(0, Item(names[i], self.month_count))
                for z in lists:  # For every list
                    self.item_list[0].add_month(z[i])  # Push the val at i
            i += 1

        item_not_refreshed = False
        for i in range(len(self.item_list)):
            item_not_refreshed = False
            for y in range(len(names)):
                if self.item_list[i].name == names[y]:
                    item_not_refreshed = True
                    break

            if not item_not_refreshed:
                for y in range(0, added_months):
                    self.item_list[i].add_month(0)

        self.month_count += added_months
        self.build_table()


    def build_table(self):
        self.table_widget_main.clear()

        self.table_widget_main.setRowCount(len(self.item_list))
        self.table_widget_main.setColumnCount(len(self.item_list[0].sells_history) + 1)  # +1 for column name

        for i in range(len(self.item_list)):  # EVERY ROW
            name = QTableWidgetItem(self.item_list[i].name)

            self.table_widget_main.setItem(i, 0, name)
            column = 1
            for y in range(len(self.item_list[i].sells_history)):
                val = QTableWidgetItem(str(self.item_list[i].sells_history[y]))
                self.table_widget_main.setItem(i, column, val)
                column += 1
