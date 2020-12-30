from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

pixelsize = 0

class Utils:
    def __init__(self, new_pixelsize):
        global pixelsize

        pixelsize = new_pixelsize

    @staticmethod
    def resize_font(widget, value):
        widget.setStyleSheet("font-size: {0}px;".format(int(pixelsize * value)))
