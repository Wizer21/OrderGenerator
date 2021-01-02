from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import locale

pixelsize = 0
pixmap_dict = {}
map_size = [0, 0]
icon_size = [0, 0]
resolution = [0, 0]
win_separator = 0

class Utils:
    def __init__(self, new_pixelsize, new_resolution):
        global pixelsize
        global pixmap_dict
        global map_size
        global resolution
        global win_separator

        width_from_rez = int(new_resolution[1] / 40)
        map_size = [width_from_rez, width_from_rez]
        icon_size = [int(map_size[0] * 3), int(map_size[1] * 3)]
        resolution = new_resolution

        locale.setlocale(locale.LC_ALL, '')
        win_separator = locale.localeconv()['decimal_point']

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
            "add": self.scale_pixmap(".\\files\\add.png", map_size[0], map_size[1]),
            "logo": self.scale_pixmap(".\\files\\logo.png", map_size[0], map_size[1]),
            "eyeopen": self.scale_pixmap(".\\files\\eyeopen.png", icon_size[0], icon_size[1]),
            "eyeclose": self.scale_pixmap(".\\files\\eyeclose.png", icon_size[0], icon_size[1]),
            "yes": self.scale_pixmap(".\\files\\yes.png", icon_size[0], icon_size[1]),
            "no": self.scale_pixmap(".\\files\\no.png", icon_size[0], icon_size[1])
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

    @staticmethod
    def resize_and_color_font(widget, value, color):
        widget.setStyleSheet("font-size: {0}px; color: {1}; font: bold;".format(int(pixelsize * value), color))

    @staticmethod
    def style_click_button(widget, color):
        style = """QPushButton {
                background-color: <color>;
                padding: 10px;
                border: 0px solid red;
                }
                QPushButton::hover {
                    border: 2px solid white;
                }
                QPushButton::pressed {
                    background-color: #161616;
                    color: <color>;
                    padding: 5px;
                    border: 0px solid transparent
                }"""
        widget.setStyleSheet(style.replace("<color>", color))


    @staticmethod
    def resize_from_resolution(window, ratio_w, ratio_h):
        window.resize(int(resolution[0] * ratio_w), int(resolution[1] * ratio_h))


    @staticmethod
    def main_menu_button_size(button, ratio_w):
        button.setFixedWidth(int(resolution[0] * ratio_w))

    @staticmethod
    def get_win_separator():
        return win_separator

    @staticmethod
    def format_large_numbers(value):
        value = round(value, 2)
        value = str(f"{value:_}")
        return value.replace("_", " ")

    @staticmethod
    def slider_lenght_from_res(slider, ratio):
        slider.setFixedWidth(int(resolution[1] * ratio))

    @staticmethod
    def clear_separators(value_str):
        value_str = value_str.replace("€", "")
        value_str = value_str.replace("$", "")
        value_str = value_str.replace("£", "")
        value_str = value_str.replace(",", ".")
        value_str = value_str.replace(win_separator, ".")
        return value_str

    @staticmethod
    def float_to_str(float):
        text = str(float)
        return text.replace(".0", "")
