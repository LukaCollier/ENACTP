import sys
from PyQt5.QtWidgets import QApplication, QPushButton


def affiche(texte):
    print('hello %s' % texte)

app = QApplication(sys.argv)
button = QPushButton("press me")
button.clicked.connect(lambda: affiche("toto"))
button.show()
app.exec()
print("fin")
