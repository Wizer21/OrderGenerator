from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

pixelsize = 0
pixmap_dict = {}
map_size = [0, 0]
icon_size = [0, 0]

class Utils:
    def __init__(self, new_pixelsize):
        global pixelsize
        global pixmap_dict
        global map_size

        map_size = [50, 50]
        icon_size = [int(map_size[0] * 2), int(map_size[1] * 2)]

        pixelsize = new_pixelsize
        pixmap_dict = {
            "paste_clipboard": self.scale_pixmap(".\\files\\paste_clipboard.png", icon_size[0], icon_size[1]),
            "skip_items": self.scale_pixmap(".\\files\\skip_items.png", icon_size[0], icon_size[1]),
            "add_items": self.scale_pixmap(".\\files\\add_items.png", icon_size[0], icon_size[1]),
            "pushtable": self.scale_pixmap(".\\files\\pushtable.png", icon_size[0], icon_size[1]),
            "settings": self.scale_pixmap(".\\files\\settings.png", map_size[0], map_size[1]),
            "add_profile": self.scale_pixmap(".\\files\\add_profile.png", map_size[0], map_size[1]),
            "trash": self.scale_pixmap(".\\files\\trash.png", icon_size[0], icon_size[1]),
            "import_data": self.scale_pixmap(".\\files\\import_data.png", icon_size[0], icon_size[1]),
            "mail": self.scale_pixmap(".\\files\\mail.png", icon_size[0], icon_size[1]),
            "copy": self.scale_pixmap(".\\files\\copy.png", icon_size[0], icon_size[1]),
            "create_mail": self.scale_pixmap(".\\files\\create_mail.png", icon_size[0], icon_size[1]),
            "edit_mail": self.scale_pixmap(".\\files\\edit_mail.png", icon_size[0], icon_size[1]),
            "mail_dark": self.scale_pixmap(".\\files\\mail_dark.png", map_size[0], map_size[1]),
            "settings_dark": self.scale_pixmap(".\\files\\settings_dark.png", map_size[0], map_size[1]),
            "import_data_dark": self.scale_pixmap(".\\files\\import_data_dark.png", map_size[0], map_size[1]),
            "add": self.scale_pixmap(".\\files\\add.png", map_size[0], map_size[1])
        }

    def scale_pixmap(self, url, w, h):
        map = QPixmap(url)
        map = map.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return map

    @staticmethod
    def get_pixmap(name):
        return pixmap_dict[name]

    @staticmethod
    def set_icon(widget, pixmap_name, scale):
        widget.setIcon(pixmap_dict[pixmap_name])
        widget.setIconSize(QSize(int(map_size[0] * scale), int(map_size[1] * scale)))

    @staticmethod
    def resize_font(widget, value):
        widget.setStyleSheet("font-size: {0}px;".format(int(pixelsize * value)))

