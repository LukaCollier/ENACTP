##@namespace pan_zoom_view
"""
    This module defines an interactive view that supports Pan and Zoom functions
    (PanZoomView class)
"""
##\privatesection

import math

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView


class PanZoomView(QGraphicsView):
    """ An interactive view that supports Pan and Zoom functions """

    def __init__(self, scene):
        super().__init__(scene)
        # enable anti-aliasing
        self.setRenderHint(QPainter.Antialiasing)
        # enable drag and drop of the view
        self.setDragMode(self.ScrollHandDrag)

    def fit_scene_in_view(self):
        """ Make sure the scene is displayed in its entirety by the view """
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def zoom_view(self, factor):
        """ This slot updates the zoom factor of the view """
        self.setTransformationAnchor(self.AnchorUnderMouse)
        super().scale(factor, factor)

    def wheelEvent(self, event):
        """ Overrides method in QGraphicsView in order to zoom it when mouse scroll occurs """
        factor = math.pow(1.001, event.angleDelta().y())
        self.zoom_view(factor)

##\endprivatesection
