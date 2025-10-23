##@namespace time_manager
"""
    This module manages time to control simulation playback
    (TimeManager class)
"""
##\privatesection

from PyQt5.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot

ANIMATION_DELAY = 50  # Animation delay to play simulation (milliseconds)
INITIAL_TIME_INCREMENT = 1


class TimeManager(QObject):
    """
        This class is composed of:
        a timer to control the time steps of the simulation,
        methods to change the way it manages it,
        signal to connect to in order to update accordingly to time changes
    """

    # Signal to notify that simulation's time has changed
    time_changed = pyqtSignal(int)

    # Signal to notify that time increment has changed
    # (each tick of the timer increments simulation's time by self.time_increment)
    time_increment_changed = pyqtSignal(int)

    def __init__(self, simu):
        super().__init__()
        self.simulation = simu
        self.time_increment = INITIAL_TIME_INCREMENT

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)

    def set_time(self, time):
        """ Change simulation's time """
        self.simulation.set_time(time)
        self.time_changed.emit(self.simulation.time)

    def set_time_increment(self, incr):
        """ Change simulation's time increment """
        self.time_increment = incr
        self.time_increment_changed.emit(self.time_increment)

    def play_pause(self):
        """ Toggle play/pause using the timer as model """
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(ANIMATION_DELAY)

    def send_initialization_signals(self):
        """ Send all the signals in order to initialize the values of the widgets connected to
            this TimeManager (convenience method to avoid having to initialize them one by one) """
        self.time_changed.emit(self.simulation.time)
        self.time_increment_changed.emit(self.time_increment)

    @pyqtSlot()
    def on_timeout(self):
        """ This slot computes the new time at each time out """
        self.simulation.increment_time(self.time_increment)
        self.time_changed.emit(self.simulation.time)

##\endprivatesection
