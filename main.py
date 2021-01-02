from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
from Main_gui import *
from Utils import *

if __name__ == "__main__":
    app = QApplication(sys.argv)

    QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    lDesktopScreen = app.primaryScreen()
    lScreenGeom = lDesktopScreen.availableGeometry()
    rec = QRect(lScreenGeom)
    resolution = [rec.width(), rec.height()]

    font_size = int(resolution[0] / 110)
    font_qss = "QWidget{ font-size:" + str(font_size) + "px;}"

    combo_size = str(int(resolution[1]/54))
    combo_style = "QComboBox:drop-down{ height: " + combo_size + "px; width: " + combo_size + "px;}"

    with open(".\\files\\theme.qss") as my_file:
        theme = my_file.read()
        app.setStyleSheet(font_qss + combo_style + theme)

    utils = Utils(font_size, resolution)

    main_gui = Main_gui()
    main_gui.show()

    sys.exit(app.exec_())