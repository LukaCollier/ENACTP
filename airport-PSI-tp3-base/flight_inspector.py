"""
    Class displaying flight information.
    Wraps a widget designed with Qt Designer.
"""

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

import timestep
import traffic


class FlightInspector(QWidget):
    """ Widget displaying information about a Flight """

    def __init__(self, radar):
        super().__init__()

        # Instance variables
        self.radar_view = radar

        # load the flight inspector created with QtDesigner
        uic.loadUi("flight_inspector.ui", self)

        # Connect to flight_selected signal emitted by radarview
        self.radar_view.flight_selected.connect(self.inspect)

        self.show()

    @pyqtSlot(traffic.Flight)
    def inspect(self, flight):
        """ Display information about a flight """
        # Get and format information from the flight
        callsign = flight.call_sign
        flight_type = flight.type.name
        wake = flight.cat.name
        stand = flight.stand.name
        runway = flight.runway.name
        qfu = flight.qfu
        time = timestep.to_hms(flight.start_t)
        slot = 'No slot' if flight.slot is None else timestep.to_hms(flight.slot)

        # Update the displayed information
        self.label_callsign.setText(callsign)
        self.label_movement_type.setText(flight_type)
        self.label_wake.setText(wake)
        self.label_stand.setText(stand)
        self.label_runway.setText(runway)
        self.label_qfu.setText(qfu)
        self.label_time.setText(time)
        self.label_slot.setText(slot)
