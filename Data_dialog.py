from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from Utils import *

class Connection(QObject):
    send_table = Signal(dict)


class Data_dialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.messager = Connection()
        self.add_new_items = True
        self.list_combobox = []
        self.table = [[]]
        self.update_clip = True

        self.layout_main = QGridLayout(self)

        self.layout_header = QGridLayout(self)
        self.label_new_item = QLabel("New Items:", self)
        self.button_add_clear = QPushButton("Add", self)
        self.label_error = QLabel(self)
        self.button_push = QPushButton("Push table", self)

        self.group_clipboard = QGroupBox("Clipboard", self)
        self.layout_clipboard = QGridLayout(self)
        self.rich_clipboard = QTextEdit(self)
        self.button_paste = QPushButton("Paste table from clipboard")

        self.table_import_view = QTableWidget(self)

        self.build()
        self.resize(1200, 700)


    def build(self):
        # STRUCTURE
        self.setLayout(self.layout_main)

        self.layout_main.addLayout(self.layout_header, 0, 0)
        self.layout_main.addWidget(self.label_new_item, 0, 0)
        self.layout_main.addWidget(self.button_add_clear, 1, 0)
        self.layout_main.addWidget(self.label_error, 0, 1)
        self.layout_main.addWidget(self.button_push, 1, 1)

        self.layout_main.addWidget(self.group_clipboard, 2, 0, 1, 2)
        self.group_clipboard.setLayout(self.layout_clipboard)
        self.layout_clipboard.addWidget(self.rich_clipboard, 0, 0)
        self.layout_clipboard.addWidget(self.button_paste, 0, 1)

        # WIDGETS PARAMETERS
        self.setWindowTitle("Import Table")
        self.setWindowIcon(Utils.get_pixmap("import_data_dark"))
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.layout_main.setAlignment(Qt.AlignTop)
        self.layout_main.setRowStretch(0, 0)
        self.layout_main.setRowStretch(1, 0)

        self.button_paste.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_import_view.setVisible(False)
        self.button_add_clear.setCursor(Qt.PointingHandCursor)
        self.button_push.setCursor(Qt.PointingHandCursor)
        self.button_paste.setCursor(Qt.PointingHandCursor)

        Utils.set_icon(self.button_add_clear, "add_items", 1.5)
        Utils.set_icon(self.button_push, "pushtable", 1.5)
        Utils.set_icon(self.button_paste, "paste_clipboard", 2)

        self.button_paste.clicked.connect(self.import_clicked)
        self.button_push.clicked.connect(self.push_button_clicked)
        self.button_add_clear.clicked.connect(self.add_items_clicked)

    @Slot()
    def import_clicked(self):
        clipboard = QGuiApplication.clipboard()
        mime_data = clipboard.mimeData()

        if not mime_data.hasText():
            self.label_error.setText("Empty Clipboard")
            return
        else:
            self.layout_main.removeWidget(self.group_clipboard)
            self.group_clipboard.setVisible(False)
            del self.group_clipboard
            self.update_clip = False

            self.layout_main.addWidget(self.table_import_view, 2, 0, 1, 2)
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
            combo.addItems(["Skip", "Name", "Reference", "Sells", "Stock"])

            self.table_import_view.setCellWidget(0, i, combo)
            combo.setCursor(Qt.PointingHandCursor)
            combo.setObjectName(str(i))
            combo.setCurrentIndex(3)

            combo.textActivated.connect(self.combo_top_changed)
            self.list_combobox.append(combo)

        self.list_combobox[0].setCurrentIndex(1)
        self.list_combobox[len(self.list_combobox) - 1].setCurrentIndex(4)

        for i in range(len(self.table)):  # PUSH DATA
            for y in range(len(self.table[i])):
                item = QTableWidgetItem(self.table[i][y])
                item.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)

                self.table_import_view.setItem(i + 1, y, item)

    @Slot()
    def push_button_clicked(self):
        if self.update_clip:
            self.label_error.setText("No table copied")
            return

        name_count = 0  # Check if there is not only one column 'Name'
        for i in range(len(self.list_combobox)):
            if self.list_combobox[i].currentText() == "Name":
                name_count += 1
                continue
        if name_count < 1:
            self.label_error.setText("Need at least one column name")
            return

        final_data = {
            "Name": [],
            "Sells": [],
            "Reference": [],
            "Stock": [],
            "Add Items": self.add_new_items
        }

        for i in range(len(self.list_combobox)):
            if self.list_combobox[i].currentText() == "Name":
                my_list = []
                for y in self.table:
                    my_list.append(y[i])
                final_data["Name"] = my_list

            elif self.list_combobox[i].currentText() == "Sells":
                my_list = []
                for y in self.table:
                    my_list.append(int(y[i]))
                final_data["Sells"].append(my_list)

            elif self.list_combobox[i].currentText() == "Reference":
                my_list = []
                for y in self.table:
                    my_list.append(y[i])
                final_data["Reference"].append(my_list)

            elif self.list_combobox[i].currentText() == "Stock":
                my_list = []
                for y in self.table:
                    my_list.append(int(y[i]))
                final_data["Stock"] = my_list

        self.messager.send_table.emit(final_data)
        self.close()

    def enterEvent(self, event):
        if self.update_clip:
            self.update_clipboard()

    def update_clipboard(self):
        clipboard = QGuiApplication.clipboard()
        mime_data = clipboard.mimeData()
        self.rich_clipboard.setText(mime_data.text())

    def add_items_clicked(self):
        if self.add_new_items:
            self.add_new_items = False
            self.button_add_clear.setText("Skip")
            Utils.set_icon(self.button_add_clear, "skip_items", 1.5)
        else:
            self.add_new_items = True
            self.button_add_clear.setText("Add")
            Utils.set_icon(self.button_add_clear, "add_items", 1.5)

    # @Slot(str)  # SLOT BLOCK OBJECT NAME ???
    def combo_top_changed(self, combo_text):
        sender_id = self.sender().objectName()

        for i in range(len(self.list_combobox)):
            if sender_id == self.list_combobox[i].objectName():
                continue
            if self.list_combobox[i].currentText() == "Name" and combo_text == "Name":
                self.list_combobox[i].setCurrentText("Skip")
                has_name = True
                return
            if self.list_combobox[i].currentText() == "Stock" and combo_text == "Stock":

                self.list_combobox[i].setCurrentText("Skip")
                has_stock = True
                return

