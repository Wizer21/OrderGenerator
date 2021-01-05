from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from Utils import *


class Table_widget_zoom(QTableWidget):
    def __init__(self, parent, new_resize_to_content):
        QTableWidget.__init__(self, parent)
        self.main_pixel_size = Utils.get_main_pixel_size()
        self.zoom_ratio = 1
        self.resize_to_content = new_resize_to_content
        self.ctrlhold = False

    def wheelEvent(self, event):
        if QGuiApplication.queryKeyboardModifiers() == Qt.ControlModifier:
            numDegrees = event.angleDelta() / 8
            wheel_height = numDegrees.y()

            if wheel_height > 0:
                self.zoom_up()

            elif wheel_height < 0:
                self.zoom_down()
        else:
            QTableWidget.wheelEvent(self, event)

    def zoom_up(self):
        self.zoom_ratio += 0.1
        self.resize_table()

    def zoom_down(self):
        self.zoom_ratio -= 0.1
        self.resize_table()

    def resize_table(self):
        font = QFont(self.font())
        font.setPixelSize(int(self.main_pixel_size * self.zoom_ratio))
        self.setFont(font)

        if self.resize_to_content:
            self.resizeColumnsToContents()
            self.resizeRowsToContents()