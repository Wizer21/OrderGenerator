from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from Utils import *

class Communication(QObject):
    name_new_profile = Signal(str)


class NewNameDialog(QDialog):
    def __init__(self, who):
        QDialog.__init__(self)
        self.messager = Communication()

        self.layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.lineedit = QLineEdit(self)
        self.button = QPushButton("Validate", self)

        self.build()

        if who == "profile":
            self.label.setText("Profile name")
            self.setWindowTitle("New Profile")
        elif who == "mail":
            self.label.setText("Preset name")
            self.setWindowTitle("New mail preset")

    def build(self):

        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineedit)
        self.layout.addWidget(self.button)

        self.setWindowIcon(Utils.get_pixmap("add"))
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.button.clicked.connect(self.button_clicked)


    @Slot()
    def button_clicked(self):
        text = self.lineedit.text()
        if len(text) != 0:
            self.messager.name_new_profile.emit(text)
        self.close()