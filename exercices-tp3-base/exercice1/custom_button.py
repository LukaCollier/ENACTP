import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QPushButton


class CustomButton(QPushButton):
    """ a QPushButton subclass with custom painting """

    def __init__(self, label):
        """ builds a custom button and displays it"""
        # calls super constuctor
        super().__init__(label)
        # adds custom logic
        self.setWindowTitle("tp flot d'execution")
        self.setGeometry(300, 300, 250, 150)

    def paintEvent(self, event):
        """ the slot triggered each time required """
        # calls super paintEvent method
        super().paintEvent(event)
        # adds custom drawing code
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.red)
        qp.drawRect(10, 10, 20, 20)
        qp.end()
        print("paintEvent has been triggered")


app = QApplication(sys.argv)
bouton = CustomButton("press me")
bouton.show()
# time.sleep(5)
app.exec()
