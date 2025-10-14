##@namespace traffic
"""Traffic sample description.

This module allows to load a traffic file and to access all its flights information.
It provides functions to detect conflicts in the airport traffic.
"""

from enum import Enum, auto
import geometry
import timestep
import airport


# Conflict detection parameters
## Minimal separation distance (meters)
SEP = 70
## Runway area width (meters)
RWY_SEP = 90
## Conflict anticipation time (seconds)
DT = 120


class Movement(Enum):
    """Type of movement, either departure or arrival.

    Attributes:
        DEP: departure
        ARR: arrival
    """
    DEP = auto()
    ARR = auto()


def movement_from_string(s):
    """Build a value of the Movement enum from its string representation.

    Args:
        s:  (str)  a string representing a movement type

    Returns:
       The corresponding Movement.

    Raises:
        ValueError: if @c s does not represent a valid movement.
    """
    if s == "DEP":
        return Movement.DEP
    elif s == "ARR":
        return Movement.ARR
    else:
        raise ValueError(f"Unknown movement type: {s}")


class Flight:
    """ Flight information and trajectory handling.

    Attributes:
        call_sign:  (str)  Commercial call sign (e.g.: AB123)
        type:  (traffic.Movement)  Departure of arrival
        cat:  (airport.WakeVortexCategory)  Wake-vortex category
        stand:  (airport.AirportPoint | None)  Parking stand used
        runway:  (airport.Runway | None)  Runway used for takeoff of landing
        qfu:  (int)  Runway direction (either 0 or 1)
        start_t:  (int | None)  Time (in timesteps) of first trajectory point in the simulation
        end_t:  (int | None)  Time (in timesteps) of last trajectory point in the simulation
        rwy_t:  (int | None)  Time (in timesteps) at which flight enters (for takeoff) or leaves (for landing) the runway
        slot:  (int | None)  Takeoff slot time (in timesteps) as attributed by NMOC, if any
        route:  (geometry.Point tuple)  Trajectory on the airport as a sequence of points
    """

    def __init__(self, call_sign, flight_type, cat):
        """The class initializer.

        Args:
            call_sign:  (str)  commercial identifier of the flight
            flight_type:  (traffic.Movement)  departure or arrival
            cat:  (airport.WakeVortexCategory)  wake-vortex category
        """
        self.call_sign = call_sign
        self.type = flight_type
        self.cat = cat
        self.stand = None
        self.runway = None
        self.qfu = 0
        self.start_t = None
        self.end_t = None
        self.rwy_t = None
        self.slot = None
        self.route = ()

    def __repr__(self):
        """Representation of the flight.

        Returns:
            A string of the form \"<traffic.Flight call_sign>\".
        """
        return f"<traffic.Flight {self.call_sign}>"

    def get_position(self, t):
        """Access the aircraft position at a given time.

        Args:
            t:  (int)  a time stamp (in timesteps)

        Returns:
            The position (geometry.Point) of the aircraft at timestep `t`.

        Raises:
            IndexError: if the flight is not on the airport at @c t.
        """
        return self.route[t - self.start_t]

    def distance(self, other, t):
        """Compute the distance to another flight at a given time.

        Args:
            other:  (traffic.Flight)  another flight
            t:  (int)  a time stamp (in timesteps)

        Returns:
            The distance in meters (int) to the `other` flight at time `t`.

        Raises:
            IndexError: if any flight is not on the airport at @c t.
        """
        return self.get_position(t).distance(other.get_position(t))

    def use_runway(self, t):
        """Checks if the flight uses its runway at a given time.

        Args:
            t:  (int)  a time stamp (in timesteps)

        Returns:
            `True` iff the flight occupies its runway at time `t`.
        """
        return t <= self.rwy_t if self.type == Movement.ARR else self.rwy_t <= t

    def in_runway(self, runway, t):
        """Checks if the flight interferes with a runway at a given time.

        Args:
            runway:  (airport.Runway)  a runway
            t:  (int)  a time stamp (in timesteps)

        Returns:
            `True` iff the flight is closer than traffic.RWY_SEP to `runway`
            at time `t`.
        """
        (a, b) = runway.coords
        return self.get_position(t).distance_to_segment(a, b) <= RWY_SEP

    def conflicts(self, other, t):
        """Checks if the flight conflicts with another flight at a given time.

        Args:
            other:  (traffic.Flight)  another flight
            t:  (int)  a time stamp (in timesteps)

        Returns:
            `True` iff the flight conflicts with the `other` flight at time `t`.
        """
        return (self.distance(other, t) < SEP or
                self.use_runway(t) and other.in_runway(self.runway, t) or
                other.use_runway(t) and self.in_runway(other.runway, t))


# Load a traffic file
def from_file(apt, filename):
    """Parse a traffic file to extract flight plan information.

    Args:
        apt:  (airport.Airport)  the airport
        filename:  (str)  the name of the file containing the flight plans

    Returns:
        The flight plans (traffic.Flight list) that have successfully been parsed.
    """
    print(f"Loading traffic: {filename}...")
    with open(filename) as file:
        flights = []
        for line in file:
            words = line.strip().split()
            try:
                movement_type = movement_from_string(words[0])
                callsign = words[1]
                category = airport.category_from_string(words[2])
                flight = Flight(callsign, movement_type, category)
                flight.stand = apt.get_point(words[3])
                flight.qfu = apt.get_qfu(words[4])
                flight.runway = apt.get_runway(flight.qfu)
                flight.rwy_t = timestep.of_seconds(int(words[6]))
                flight.slot = None if words[7] == "_" else timestep.of_seconds(int(words[7]))
                flight.route = geometry.points_from_strings(words[8:])
                flight.start_t = timestep.of_seconds(int(words[5]))
                flight.end_t = flight.start_t + len(flight.route)
                flights.append(flight)
            except Exception as error:
                print(type(error), error, line)
        return flights


def select(flights, t):
    """Selects the flights that are moving at a given time step.

    Args:
        flights:  (Flight list)  the flights to select from
        t:  (int)  a time stamp (in timesteps)

    Returns:
        The selection as a Flight list.
    """
    return [f for f in flights if f.start_t <= t < f.start_t + len(f.route)]


def detect(flights, t):
    """Detect conflicts at a given time.

    Args:
        flights:  (Flight list)  the flights to consider
        t:  (int)  a time stamp (in timesteps)

    Returns:
        The set (Flight set) of conflicting `flights` at time `t`.
    """
    conflicts = set()
    for i, fi in enumerate(flights):
        for j in range(i):
            fj = flights[j]
            if fi.conflicts(fj, t):
                conflicts |= { fi, fj }
    return conflicts


def detect_in(flights, t1, t2):
    """Detect conflicts in a given period of time.

    Args:
        flights:  (Flight list)  the flights to consider
        t1:  (int)  the starting time stamp (in timesteps)
        t2:  (int)  the end time stamp (in timesteps)

    Returns:
        The set (Flight set) of conflicting `flights` between `t1` and `t2`.
    """
    conflicts = set()
    for i, fi in enumerate(flights):
        for j in range(i):
            fj = flights[j]
            for t in range(t1, min(t2 + 1, fi.end_t, fj.end_t)):
                if fi.conflicts(fj, t):
                    conflicts |= { fi, fj }
    return conflicts
