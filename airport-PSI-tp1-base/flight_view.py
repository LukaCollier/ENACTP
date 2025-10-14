##@namespace flight_view
"""
    This module allows the representation of a flight (FlightView class)
"""
##\privatesection

from enum import Enum, auto

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPainterPath, QPen
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsPathItem

import airport
import traffic
from simulation_utilities import min_dist_time

# Constant colors
DEP_COLOR = "blue"     # Departure color
ARR_COLOR = "magenta"  # Arrival color
CONF_COLOR = "red"     # Conflicting aircraft color
SEL_COLOR = "green"    # color for selected aircraft

# Brushes
DEP_BRUSH = QBrush(QColor(DEP_COLOR))
ARR_BRUSH = QBrush(QColor(ARR_COLOR))
CONF_BRUSH = QBrush(QColor(CONF_COLOR))

PEN_WIDTH = 3
DEP_PEN = QPen(QColor(DEP_COLOR), PEN_WIDTH)
ARR_PEN = QPen(QColor(ARR_COLOR), PEN_WIDTH)
CONF_PEN = QPen(QColor(CONF_COLOR), PEN_WIDTH)
SEL_PEN = QPen(QColor(SEL_COLOR), 40)
NO_PEN = QPen(Qt.NoPen)


class FlightView(QGraphicsEllipseItem):
    """ The view of an aircraft to add in a QGraphicsScene """

    def __init__(self, f, radar):
        """ FlightView constructor, creates the ellipse and adds it to the scene """
        super().__init__()

        # Instance variables
        self.flight = f
        self.radar_view = radar

        # Create the tooltip
        tooltip = f.type.name + " " + f.call_sign + " " + f.qfu
        self.setToolTip(tooltip)

        # Build the ellipse by computing its initial size
        self.update_size()

    def update_position(self, is_conflict):
        """ Move this FlightView in the scene """
        position = self.flight.get_position(self.radar_view.simulation.time)
        self.setBrush(DEP_BRUSH if self.flight.type == traffic.Movement.DEP else ARR_BRUSH)
        if is_conflict:
            self.setBrush(CONF_BRUSH)
        self.setPos(position.x, position.y)

    def update_size(self):
        """ Compute and update the size of this FlightView """
        width = 1.5 * traffic.SEP if self.flight.cat == airport.WakeVortexCategory.HEAVY else traffic.SEP
        self.setRect(-width, -width, width * 2, width * 2)

    def mousePressEvent(self, event):
        """ Overrides method in QGraphicsItemGroup for interaction on the scene """
        event.accept()


##\endprivatesection
