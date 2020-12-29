from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class Communication(QObject):
    name_new_profile = Signal(str)


class NewNameDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.messager = Communication()

        self.layout = QVBoxLayout(self)
        self.label = QLabel("Profile name", self)
        self.lineedit = QLineEdit(self)
        self.button = QPushButton("Validate", self)

        self.build()

    def build(self):
        self.setWindowTitle("New Profile")

        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineedit)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.button_clicked)


    @Slot()
    def button_clicked(self):
        text = self.lineedit.text()
        if len(text) != 0:
            self.messager.name_new_profile.emit(text)
        self.close()