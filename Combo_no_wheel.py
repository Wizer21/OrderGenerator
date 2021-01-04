from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class Combo_no_wheel(QComboBox):
    def __init__(self, parent):
        QComboBox.__init__(self, parent)

    def wheelEvent(self, e):
        return