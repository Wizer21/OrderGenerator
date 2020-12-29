from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class TableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return super().__lt__(other)