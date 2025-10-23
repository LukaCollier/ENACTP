##@namespace app
"""
Main module for the Python Airport Simulation
"""

import os
import os.path
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDockWidget, QMainWindow

import airport
import traffic
from flight_inspector import FlightInspector
from pan_zoom_view import PanZoomView
from radar_view import RadarView
from simulation import Simulation

## Data root directory
DATA_ROOT = "DATA"
## Airport to simulate (sub-directory of DATA_ROOT)
APT = "LFPG"
## Name of the airport description files
APT_FILE = "map.txt"
## Name of the traffic files
PLN_FILE = "flights.txt"


def main():
    """Main function."""
    # Load files
    data_dir = os.path.join(DATA_ROOT, APT)
    apt_file = os.path.join(data_dir, APT_FILE)
    pln_file = os.path.join(data_dir, PLN_FILE)

    ## Airport for the simulation
    apt = airport.from_file(apt_file)

    ## Traffic considered for simulation
    flights = traffic.from_file(apt, pln_file)

    # Create the simulation
    ## Initial simulation state
    sim = Simulation(apt, flights)

    # Initialize Qt
    ## Main application
    app = QApplication(sys.argv)

    # Create the radar view and the time navigation interface
    rad = RadarView(sim)
    rad.move(10, 10)

    # Create the flight inspector (displays information about the selected flight)
    insp = FlightInspector(rad)

    # Create a QDockWidget to hold the flight inspector
    insp_dock = QDockWidget()
    insp_dock.setWidget(insp)

    # Create the QMainWindow to hold both radar view and flight inspector
    win = QMainWindow()
    win.setWindowTitle("AirPort Sim Qt MainWindow & Dock")
    win.setCentralWidget(rad)
    win.addDockWidget(Qt.DockWidgetArea(1), insp_dock)
    # The QMainWindow is the root widget of this QApplication, so it must be explicitly shown...
    # win.resize(1000, 600)
    # win.show()         # either as a normal window...
    win.showMaximized()  # ...or in full screen mode
    sview=PanZoomView(rad.scene)
    sview.scale(0.1,-0.1)
    sview.show()
    # Enter the main loop
    app.exec()


if __name__ == "__main__":
    main()
