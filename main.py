from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
from Main_gui import *
from Utils import *

if __name__ == "__main__":
    app = QApplication(sys.argv)

    lDesktopScreen = app.primaryScreen()
    lScreenGeom = lDesktopScreen.availableGeometry()

    rec = QRect(lScreenGeom)
    resolution = [rec.width(), rec.height()]

    pointsize = int(resolution[0] / 110)
    pixelsize = "QWidget{ font-size:" + str(pointsize) + "px;}"

    with open(".\\files\\theme.qss") as my_file:
        theme = my_file.read()
        app.setStyleSheet(theme + pixelsize)

    utils = Utils(pointsize)

    main_gui = Main_gui()
    main_gui.show()

    sys.exit(app.exec_())