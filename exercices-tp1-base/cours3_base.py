import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QWidget
from random import randint
# Ma base de données
class Film:
    def __init__(self, titre, version):
        self.titre = titre
        self.version = version
    def uversion(self):
        self.version +=1
        #print(self.version)
    

films = [Film('Fast and Furious', 9), Film('xXx', 3)]
def affiche(film,label):
    film.uversion()
    label.setText(film.titre + " " + str(film.version))
app = QApplication(sys.argv)

container = QWidget()
box = QHBoxLayout()
container.setLayout(box)

label_annonce = QLabel('Vin Diesel joue dans')
box.addWidget(label_annonce)

label_titre = QLabel(films[0].titre + " " + str(films[0].version))
box.addWidget(label_titre)

button = QPushButton("Et c'est tout ?")
button.clicked.connect(lambda :affiche(films[randint(0,1)],label_titre))

box.addWidget(button)

container.show()
app.exec()
