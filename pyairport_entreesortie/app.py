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
import building as bld
from radar_view import RadarView
from simulation import Simulation

## Data root directory
DATA_ROOT = "DATA"
## Airport to simulate (sub-directory of DATA_ROOT)
APT = ["LFPG", "LFPO"]
## Name of the airport description files
APT_FILE = "map.txt"
## Name of the traffic files
PLN_FILE = "flights.txt"
TERMINAL = "terminals.txt"

def choose_airport():
    try:
        choice = int(input("1 - [CDG]\n2 - Orly\n"))
    except ValueError:
        choice = 1
    return APT[choice - 1]


def main():
    """Main function."""
    # Load files
    choose= choose_airport()
    data_dir = os.path.join(DATA_ROOT, choose)
    apt_file = os.path.join(data_dir, APT_FILE)
    pln_file = os.path.join(data_dir, PLN_FILE)

    if choose == APT[0]:
        term_file = os.path.join(data_dir,TERMINAL)
        terminals=bld.from_file(term_file)
        ## Airport for the simulation
        apt = airport.from_file(apt_file,terminals)
    else:
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

    # The radar view is the root widget of this QApplication, so it must be explicitly shown...
    # rad.resize(1000, 600)
    rad.show()             # either as a normal window...
    # rad.showMaximized()  # ...or in full screen mode

    # Enter the main loop
    app.exec()


if __name__ == "__main__":
    main()
