from PyQt5.QtWidgets import (QApplication, QGraphicsScene,
                             QGraphicsSimpleTextItem, QGraphicsView,
                             QHBoxLayout, QWidget,QGraphicsRectItem)
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import QBrush


class SceneBasedWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a scene and populate it
        self.scene = QGraphicsScene()
        self.init_scene()
        
        # Create a view attached to the scene, show it
        self.view = QGraphicsView(self.scene)
        self.view1 = QGraphicsView(self.scene)
        # Create a layout for this widget and add the view
        # (no need for the moment but if we have to add other widgets in the near future...)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.view)
        layout.addWidget(self.view1)
        self.rectitem.mousePressEvent =(lambda n : self.change_text("clique"))
        self.rectitem.mouseReleaseEvent=(lambda n: self.change_text("Coucou !"))

    def init_scene(self):
        # Create a QGraphicsItem
        self.text_item = QGraphicsSimpleTextItem("Coucou !")
        self.rectitem= QGraphicsRectItem(0,0,150,100)
        self.rectitem.setBrush(Qt.gray)
        # Add it to the QGraphicsScene
        self.scene.addItem(self.rectitem)
        self.scene.addItem(self.text_item)
    
    def change_text(self,s):
        self.text_item.setText(s)
        #print(s)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = SceneBasedWidget()
    widget.show()
    app.exec()
