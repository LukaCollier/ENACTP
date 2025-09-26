##@namespace radar_view
"""
    Airport and flights visualization.
    This module allows the visualization of an airport and its flights
    on a scalable graphics view
"""
##\privatesection

from PyQt5.QtCore import QCoreApplication, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QKeySequence, QPainterPath, QPen
from PyQt5.QtWidgets import (QGraphicsEllipseItem, QGraphicsItemGroup,
                             QGraphicsLineItem, QGraphicsPathItem,
                             QGraphicsRectItem, QGraphicsScene, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QShortcut,
                             QSlider, QVBoxLayout, QWidget)

import airport
import traffic
import timestep
from flight_views_motion_manager import FlightViewsMotionManager
from pan_zoom_view import PanZoomView
from time_manager import TimeManager

# Constants
WIDTH = 800           # Initial window width (pixels)
HEIGHT = 450          # Initial window height (pixels)
AIRPORT_Z_VALUE = 0   # To ensure airport items will be drawn in background

# Color constants (SVG color keyword names as defined by w3c
# https://www.w3.org/TR/SVG/types.html#ColorKeywords)
APT_COLOR = "lightgrey"   # Airport elements color
STAND_COLOR = "darkgrey"  # Stands color
POINT_COLOR = "grey"      # Points (other than stands) color

# Brushes
STAND_BRUSH = QBrush(QColor(STAND_COLOR))
POINT_BRUSH = QBrush(QColor(POINT_COLOR))


class RadarView(QWidget):
    """ An interactive view of an airport and its flights """

    def __init__(self, simu):
        super().__init__()

        #### Simulation data and control
        self.simulation = simu
        # Create the time manager in charge of running the simulation
        self.time_manager = TimeManager(self.simulation)

        #### RadarView global settings
        # Settings
        self.setWindowTitle("Airport Sim at " + self.simulation.airport.name)
        self.resize(WIDTH, HEIGHT)

        # Create the root layout allowing to align the RadarView children vertically
        root_layout = QVBoxLayout()
        self.setLayout(root_layout)

        #### Airport and flight views
        self.scene = QGraphicsScene()           # Scene that holds airport and flight views
        self.view = self.create_airport_view()  # View that displays the scene
        root_layout.addWidget(self.view)        # Add the view to the root layout
        self.flight_views_motion_manager = FlightViewsMotionManager(self)  # Flight views

        #### Toolbar
        # (allows the user to control the simulation playback)
        toolbar = self.create_toolbar()
        root_layout.addLayout(toolbar)

        # Ask time manager to send all its signals in order to initialize the values of the widgets
        # connected to it (convenience method to avoid having to initialize them one by one)
        self.time_manager.send_initialization_signals()

        #### Show this widget
        self.show()

    def create_toolbar(self):
        """ Create the toolbar """
        #### Toolbar (a horizontal layout to hold time controls)
        toolbar = QHBoxLayout()

        #### Buttons
        # Factor the creation of buttons in a nested function
        def add_button(text, slot):
            button = QPushButton(text)    # Create and setup the button
            toolbar.addWidget(button)     # Add it to its parent
            button.clicked.connect(slot)  # Connect the button's clicked signal to the slot

        # Add buttons to toolbar
        # (using lambda function allows to pass extra arguments to slots)
        add_button("-", lambda: self.view.zoom_view(1/1.1))
        add_button("+", lambda: self.view.zoom_view(1.1))
        toolbar.addStretch()
        add_button("<<", lambda: self.time_manager.set_time_increment(-5))
        add_button(" <", lambda: self.time_manager.set_time_increment(-1))
        add_button("|>", self.time_manager.play_pause)
        add_button(" >", lambda: self.time_manager.set_time_increment(1))
        add_button(">>", lambda: self.time_manager.set_time_increment(5))

        #### Time entry
        # Add a QLineEdit to display simulation's time and let the user change it at will
        time_entry = QLineEdit()
        toolbar.addWidget(time_entry)
        time_entry.setInputMask("00:00:00")

        # Slot to react to user's entries on the time entry widget
        def on_time_entry_change():
            # Modify time in time manager according to the user's input
            self.time_manager.set_time(timestep.of_hms(time_entry.text()))
            time_entry.clearFocus()

        # Connect the QLineEdit's editingFinished signal to slot
        time_entry.editingFinished.connect(on_time_entry_change)

        # Conversely, react to time changes in time manager:
        # change the value displayed by the time entry
        self.time_manager.time_changed.connect(lambda int_val: time_entry.setText(timestep.to_hms(int_val)))

        #### Shortcuts
        # Factor the creation of shotcuts in a nested function
        def add_shortcut(text, slot):
            shortcut = QShortcut(QKeySequence(text), self)
            shortcut.activated.connect(slot)

        # Add shortcuts
        add_shortcut("-", lambda: self.view.zoom_view(1/1.1))
        add_shortcut("+", lambda: self.view.zoom_view(1.1))
        add_shortcut(" ", self.time_manager.play_pause)
        add_shortcut("q", QCoreApplication.instance().quit)

        return toolbar

    def create_airport_view(self):
        """ Add the airport (as a group) to the QGraphicsScene, drawn by the QGraphicsView """
        # Create the view that displays the scene
        view = PanZoomView(self.scene)
        # Invert y axis for the view
        # (oriented upwards in the real world and downwards in the Qt coordinate system)
        view.scale(1, -1)

        # Airport items

        # Create a group to hold all the airport items, add it to the scene
        # and make sure it is drawn in background
        airport_group = QGraphicsItemGroup()
        self.scene.addItem(airport_group)
        airport_group.setZValue(AIRPORT_Z_VALUE)

        # Taxiways
        pen = QPen(QColor(APT_COLOR), airport.TAXIWAY_WIDTH)
        pen.setCapStyle(Qt.RoundCap)
        for taxiway in self.simulation.airport.taxiways:
            path = QPainterPath()
            path.moveTo(taxiway.coords[0].x, taxiway.coords[0].y)
            for xy in taxiway.coords[1:]:
                path.lineTo(xy.x, xy.y)
            item = QGraphicsPathItem(path, airport_group)
            item.setPen(pen)
            item.setToolTip("Taxiway " + taxiway.taxi_name)

        # Runways
        pen = QPen(QColor(APT_COLOR), airport.RUNWAY_WIDTH)
        for runway in self.simulation.airport.runways:
            (p1, p2) = runway.coords
            item = QGraphicsLineItem(p1.x, p1.y, p2.x, p2.y, airport_group)
            item.setPen(pen)
            item.setToolTip("Runway " + runway.name)

        # Named points
        pen = QPen(Qt.transparent)
        width = 0.7 * traffic.SEP
        half_width = width / 2.
        for point in self.simulation.airport.points:
            bounds = QRectF(point.x - half_width, point.y - half_width, width, width)
            if point.type == airport.PointType.STAND:
                item = QGraphicsEllipseItem(bounds, airport_group)
                item.setBrush(STAND_BRUSH)
                point_type_description = "Stand"
            else:
                item = QGraphicsRectItem(bounds, airport_group)
                item.setBrush(POINT_BRUSH)
                if point.type == airport.PointType.RUNWAY_POINT:
                    point_type_description = "Runway point"
                else:
                    point_type_description = "Deicing point"
            item.setPen(pen)
            item.setToolTip(point_type_description + " " + point.name)

        # Once the scene is complete, make it fit in the view
        view.fit_scene_in_view()

        return view

    def add_flight_view(self, item):
        """ Add a flight view to the scene """
        self.scene.addItem(item)

    def remove_flight_view(self, item):
        """ Remove a flight view from the scene """
        self.scene.removeItem(item)

##\endprivatesection
