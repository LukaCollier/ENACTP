import sys

from PyQt5.QtWidgets import QApplication, QPushButton


def affiche():
    print("1")

print("2")
app = QApplication(sys.argv)
bouton = QPushButton("press me")
bouton.setWindowTitle("tp flot d'execution")
bouton.pressed.connect(affiche)
bouton.setGeometry(300, 300, 250, 150)
bouton.show()
print("3")
app.exec()
print("4")
