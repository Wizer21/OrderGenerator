from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class Data_dialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.add_new_items = True
        self.list_combobox = []
        self.table = [[]]

        # self.widget_main = QWidget(self)
        self.layout_main = QGridLayout(self)
        self.label_new_item = QLabel("New Items:", self)
        self.button_add_clear = QPushButton("Add", self)
        self.button_push = QPushButton("Push Data", self)
        self.button_paste = QPushButton("Paste table from clipboard")

        self.table_import_view = QTableWidget(self)

        self.build()
        self.resize(1000, 1000)


    def build(self):
        # STRUCTURE
        self.setLayout(self.layout_main)

        self.layout_main.addWidget(self.label_new_item, 0, 0)
        self.layout_main.addWidget(self.button_add_clear, 1, 0)
        self.layout_main.addWidget(self.button_push, 0, 1, 2, 1)
        self.layout_main.addWidget(self.button_paste, 2, 0, 2, 2)

        # WIDGETS PARAMETERS
        self.layout_main.setRowStretch(0, 0)
        self.layout_main.setRowStretch(1, 1)
        self.button_push.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_paste.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_import_view.setVisible(False)

        self.button_paste.clicked.connect(self.import_clicked)
        self.button_push.clicked.connect(self.push_button_clicked)

    @Slot()
    def import_clicked(self):
        clipboard = QGuiApplication.clipboard()
        mime_data = clipboard.mimeData()

        if not mime_data.hasText():
            self.button_paste.setText("Paste table from clipboard \n EMPTY CLIPBOARD")
            return
        else:
            self.layout_main.removeWidget(self.button_paste)
            self.button_paste.setVisible(False)
            del self.button_paste

            self.layout_main.addWidget(self.table_import_view, 2, 0, 2, 2)
            self.table_import_view.setVisible(True)

        text = mime_data.text()
        current_item = ""
        rows = 0
        str_size = len(text)
        i = 0
        while i < str_size:  # BUILD STRING DATA IN TABLE
            if text[i] == "\t":
                self.table[rows].append(current_item)
                current_item = ""

            elif text[i] == "\n":
                self.table[rows].append(current_item)
                current_item = ""
                rows += 1
                if i + 1 < str_size:
                    self.table.append([])

            else:
                current_item += text[i]
            i += 1

        self.table_import_view.setColumnCount(len(self.table[0]))  # SET ROW/COLUMN COUNT
        self.table_import_view.setRowCount(len(self.table) + 1)

        for i in range(len(self.table[0])):  # SET TOP BUTTONS
            combo = QComboBox(self)
            combo.addItems(["Delete", "Name", "Stock", "Reference"])

            self.table_import_view.setCellWidget(0, i, combo)
            self.list_combobox.append(combo)

        for i in range(len(self.table)):  # PUSH DATA
            for y in range(len(self.table[i])):
                item = QTableWidgetItem(self.table[i][y])

                self.table_import_view.setItem(i + 1, y, item)


    @Slot()
    def push_button_clicked(self):
        final_data = {
            "Name": [],
            "Stock": [],
            "Reference": []
        }

        my_list = []

        for i in range(len(self.list_combobox)):

            if self.list_combobox[i].currentText() == "Name":
                my_list.clear()
                for y in self.table:
                    my_list.append(self.table[y][i])
                final_data["Name"].append(my_list)

            if self.list_combobox[i].currentText() == "Stock":
                my_list.clear()
                for y in self.table:
                    my_list.append(self.table[y][i])
                final_data["Stock"].append(my_list)







