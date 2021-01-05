from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from Utils import *
import locale
from Combo_no_wheel import *
from Table_widget_zoom import *


class Connection(QObject):
    send_table = Signal(dict)


class Data_dialog(QDialog):
    def __init__(self, new_color_dict):
        QDialog.__init__(self)
        self.messager = Connection()
        self.add_new_items = True
        self.list_combobox = []
        self.list_rows_button = []
        self.table = [[]]
        self.update_clip = True
        self.color_dict = new_color_dict
        self.event_no_wheel = QObject()

        self.layout_main = QGridLayout(self)

        self.widget_top = QWidget(self)
        self.layout_header = QGridLayout(self)
        self.label_new_item = QLabel("New Items:", self)
        self.button_add_clear = QPushButton("Add", self)
        self.label_error = QLabel(self)
        self.button_push = QPushButton("Push table", self)

        self.group_clipboard = QGroupBox("Clipboard", self)
        self.layout_clipboard = QGridLayout(self)
        self.rich_clipboard = QTextEdit(self)
        self.button_paste = QPushButton("Paste table from clipboard")

        self.table_import_view = Table_widget_zoom(self, False)

        self.build()
        Utils.resize_from_resolution(self, 0.6, 0.6)

    def build(self):
        # STRUCTURE
        self.setLayout(self.layout_main)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint)

        self.layout_main.addWidget(self.widget_top, 0, 0, 1, 2)
        self.widget_top.setLayout(self.layout_header)
        self.layout_header.addWidget(self.label_new_item, 0, 0)
        self.layout_header.addWidget(self.button_add_clear, 1, 0)
        self.layout_header.addWidget(self.label_error, 0, 1)
        self.layout_header.addWidget(self.button_push, 1, 1)

        self.layout_main.addWidget(self.group_clipboard, 2, 0, 1, 2)
        self.group_clipboard.setLayout(self.layout_clipboard)
        self.layout_clipboard.addWidget(self.rich_clipboard, 0, 0, 3, 1)
        self.layout_clipboard.addWidget(self.button_paste, 3, 0, 1, 1)

        # WIDGETS PARAMETERS
        self.setWindowTitle("Import Table")
        self.setWindowIcon(Utils.get_pixmap("import_data_dark"))
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.layout_main.setAlignment(Qt.AlignTop)
        self.layout_main.setRowStretch(0, 0)
        self.layout_main.setRowStretch(1, 0)
        self.widget_top.setVisible(False)

        self.layout_clipboard.setRowStretch(0, 1)
        self.layout_clipboard.setRowStretch(1, 1)
        self.layout_clipboard.setRowStretch(2, 1)
        self.layout_clipboard.setRowStretch(3, 1)

        self.button_paste.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_import_view.setVisible(False)
        self.button_add_clear.setCursor(Qt.PointingHandCursor)
        self.button_push.setCursor(Qt.PointingHandCursor)
        self.button_paste.setCursor(Qt.PointingHandCursor)

        Utils.set_icon(self.button_add_clear, "add_items", 1.5)
        Utils.set_icon(self.button_push, "pushtable", 1.5)
        Utils.set_icon(self.button_paste, "paste_clipboard", 2)
        Utils.style_click_button(self.button_paste, "#1976d2")
        Utils.style_click_button(self.button_push, "#689f38")
        Utils.style_click_button(self.button_add_clear, "#ffa000")
        self.label_error.setStyleSheet("color: #d32f2f;")

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

            self.widget_top.setVisible(True)

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

        self.table_import_view.setColumnCount(len(self.table[0]) + 1)  # SET ROW/COLUMN COUNT
        self.table_import_view.setRowCount(len(self.table) + 1)

        count_columns = self.table_import_view.columnCount()
        headers = [""]
        for i in range(1, count_columns):
            headers.append(str(i))
        self.table_import_view.setHorizontalHeaderLabels(headers)

        for i in range(len(self.table[0])):  # SET TOP BUTTONS
            combo = Combo_no_wheel(self)
            combo.addItems(["Skip", "Ref.", "Name", "Sells", "Stock", "Buy P.", "Sell P."])

            self.table_import_view.setCellWidget(0, i + 1, combo)
            combo.setCursor(Qt.PointingHandCursor)
            combo.setObjectName(str(i))
            combo.setCurrentIndex(3)

            combo.setItemDelegate(QStyledItemDelegate())
            combo.textActivated.connect(self.combo_top_changed)
            self.list_combobox.append(combo)

        self.list_combobox[0].setCurrentIndex(2)
        self.list_combobox[len(self.list_combobox) - 1].setCurrentIndex(4)
        self.style_boxes()

        for i in range(len(self.table)):
            button = QPushButton()
            button.setObjectName(str(i) + "y")

            Utils.style_click_button(button, "#689f38")
            Utils.set_icon(button, "yes", 1)
            button.setCursor(Qt.PointingHandCursor)

            self.list_rows_button.append(button)
            self.table_import_view.setCellWidget(i + 1, 0, button)
            button.clicked.connect(self.row_clicked)

        self.table_import_view.setColumnWidth(0, 1)

        for i in range(len(self.table)):  # PUSH DATA
            for y in range(len(self.table[i])):
                item = QTableWidgetItem(self.table[i][y])
                item.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)

                self.table_import_view.setItem(i + 1, y + 1, item)

    @Slot()
    def push_button_clicked(self):
        self.label_error.setText("")
        if self.update_clip:
            self.label_error.setText("No table copied")
            return

        got_name = False  # Check if there is not only one column 'Name'
        for i in range(len(self.list_combobox)):
            if self.list_combobox[i].currentText() == "Name":
                got_name = True
                continue
        if not got_name:
            self.label_error.setText("Need at least one column name")
            return

        table_save = self.table.copy()

        self.list_rows_button.reverse()
        for i in self.list_rows_button:
            obj_name = i.objectName()
            if obj_name[len(obj_name) - 1] == "n":
                obj_name = obj_name.replace("n", "")
                del self.table[int(obj_name)]
        if len(self.table) == 0:
            self.table = table_save.copy()
            self.label_error.setText("Nothing imported")
            self.list_rows_button.reverse()
            return

        final_data = {
            "Name": [],
            "Sells": [],
            "Reference": [],
            "Stock": [],
            "Buyprice": [],
            "Sellprice": [],
            "Add Items": self.add_new_items
        }

        for i in range(len(self.list_combobox)):
            if self.list_combobox[i].currentText() == "Skip":
                continue
            elif self.list_combobox[i].currentText() == "Name":
                my_list = []
                for y in self.table:
                    my_list.append(y[i])
                final_data["Name"] = my_list

            elif self.list_combobox[i].currentText() == "Sells":
                my_list = []
                for y in range(len(self.table)):
                    value = Utils.clear_separators(self.table[y][i])
                    try:
                        my_list.append(int(value))
                    except ValueError:
                        self.table = table_save.copy()
                        self.list_rows_button.reverse()
                        self.label_error.setText("Column {0}, value ".format(i + 1) + str(self.table[y][i]) + " must be numeric")
                        return
                final_data["Sells"].append(my_list)

            elif self.list_combobox[i].currentText() == "Ref.":
                my_list = []
                for y in self.table:
                    my_list.append(y[i])
                final_data["Reference"] = my_list

            elif self.list_combobox[i].currentText() == "Stock":
                my_list = []
                for y in range(len(self.table)):
                    value = Utils.clear_separators(self.table[y][i])
                    try:
                        my_list.append(float(value))
                    except ValueError:
                        self.table = table_save.copy()
                        self.list_rows_button.reverse()
                        self.label_error.setText("Column {0}, value ".format(i + 1) + str(self.table[y][i]) + " must be numeric")
                        return
                final_data["Stock"] = my_list

            elif self.list_combobox[i].currentText() == "Buy P.":
                my_list = []
                for y in range(len(self.table)):
                    value = Utils.clear_separators(self.table[y][i])
                    try:
                        my_list.append(float(value))
                    except ValueError:
                        self.table = table_save.copy()
                        self.list_rows_button.reverse()
                        self.label_error.setText("Column {0}, value ".format(i + 1) + str(self.table[y][i]) + " must be numeric")
                        return
                final_data["Buyprice"] = my_list

            elif self.list_combobox[i].currentText() == "Sell P.":
                my_list = []
                for y in range(len(self.table)):
                    value = Utils.clear_separators(self.table[y][i])
                    try:
                        my_list.append(float(value))
                    except ValueError:
                        self.table = table_save.copy()
                        self.list_rows_button.reverse()
                        self.label_error.setText("Column {0}, value ".format(i + 1) + str(self.table[y][i]) + " must be numeric")
                        return
                final_data["Sellprice"] = my_list

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
            Utils.style_click_button(self.button_add_clear, "#455a64")
        else:
            self.add_new_items = True
            self.button_add_clear.setText("Add")
            Utils.set_icon(self.button_add_clear, "add_items", 1.5)
            Utils.style_click_button(self.button_add_clear, "#ffa000")

    # @Slot(str)  # SLOT BLOCK OBJECT NAME ???
    def combo_top_changed(self, combo_text):
        combo = self.sender()

        self.paint_box(combo, combo_text)

        for i in range(len(self.list_combobox)):
            if combo.objectName() == self.list_combobox[i].objectName():
                continue
            if self.list_combobox[i].currentText() == "Name" and combo_text == "Name":
                self.list_combobox[i].setCurrentText("Skip")
                self.paint_box(self.list_combobox[i], "Skip")
                return
            if self.list_combobox[i].currentText() == "Ref." and combo_text == "Ref.":
                self.list_combobox[i].setCurrentText("Skip")
                self.paint_box(self.list_combobox[i], "Skip")
                return
            if self.list_combobox[i].currentText() == "Stock" and combo_text == "Stock":
                self.list_combobox[i].setCurrentText("Skip")
                self.paint_box(self.list_combobox[i], "Skip")
                return
            if self.list_combobox[i].currentText() == "Buy P." and combo_text == "Buy P.":
                self.list_combobox[i].setCurrentText("Skip")
                self.paint_box(self.list_combobox[i], "Skip")
                return
            if self.list_combobox[i].currentText() == "Sell P." and combo_text == "Sell P.":
                self.list_combobox[i].setCurrentText("Skip")
                self.paint_box(self.list_combobox[i], "Skip")
                return

    def style_boxes(self):
        for i in self.list_combobox:
            self.paint_box(i, i.currentText())

            i.setItemData(0, QColor("#000000"), Qt.BackgroundRole)
            i.setItemData(1, QColor(self.color_dict["Reference"]), Qt.BackgroundRole)
            i.setItemData(2, QColor(self.color_dict["Name"]), Qt.BackgroundRole)
            i.setItemData(3, QColor(self.color_dict["Sells"]), Qt.BackgroundRole)
            i.setItemData(4, QColor(self.color_dict["Stock"]), Qt.BackgroundRole)
            i.setItemData(5, QColor(self.color_dict["Buyp"]), Qt.BackgroundRole)
            i.setItemData(6, QColor(self.color_dict["Sellp"]), Qt.BackgroundRole)

    def row_clicked(self):
        button = self.sender()
        name = button.objectName()
        if name[len(name) - 1] == "y":
            name = name.replace("y", "n")
            button.setObjectName(name)
            Utils.style_click_button(button, "#d32f2f")
            Utils.set_icon(button, "no", 1)
        else:
            name = name.replace("n", "y")
            button.setObjectName(name)
            Utils.style_click_button(button, "#689f38")
            Utils.set_icon(button, "yes", 1)

    def paint_box(self, combo, text):
        if text == "Ref.":
            text = "Reference"
        elif text == "Buy P.":
            text = "Buyp"
        elif text == "Sell P.":
            text = "Sellp"
        elif text == "Skip":
            combo.setStyleSheet("background-color: #000000;")
            return

        if text in self.color_dict:
            combo.setStyleSheet("background-color: {0};".format(self.color_dict[text]))
        else:
            combo.setStyleSheet("background-color: transparent;")
