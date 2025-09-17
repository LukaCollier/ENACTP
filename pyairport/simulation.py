##@namespace simulation
"""
Interactive airport simulation.

This module defines the interactions with the simulation.
"""

import timestep
import traffic


## Day duration in seconds
DAY = 24 * 3600
## 12:00 but in seconds
NOON = DAY // 2


class Simulation:
    """The simulation state.

    Attributes:
        airport:  (airport.Airport)  The airport
        all_flights:  (traffic.Flight list)  The traffic
        time:  (int)  Current time in time-steps
        current_flights:  (traffic.Flight list)  Flights at current time
        conflicts: (traffic.Flight set)  Conflicts at current time
    """

    def __init__(self, apt, flights, init_time=NOON):
        """The class initializer.

        Args:
            apt:  (airport.Airport)  the airport
            flights:  (traffic.Flight list)  the traffic
            init_time:  (int)  time (in seconds) at which to start the simulation (optional, default value: `NOON`)
        """
        self.airport = apt
        self.all_flights = flights
        self.conflicts = set()
        self.time = timestep.of_seconds(init_time)
        self.current_flights = traffic.select(self.all_flights, self.time)

    def set_time(self, t):
        """Sets the current time of the simulation.

        Args:
            t:  (int)  a time-step
        """
        self.time = t
        self.current_flights = traffic.select(self.all_flights, self.time)

    def increment_time(self, dt):
        """Advance time by a given amount.

        Args:
            dt:  (int)  number of time-steps (might be < 0)
        """
        self.set_time(self.time + dt)
