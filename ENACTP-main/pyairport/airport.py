## @namespace airport
"""
Airport elements description.

This module allows to load an airport description file
and to access to all its elements information.
"""

from enum import Enum, auto
import geometry


class PointType(Enum):
    """The types of points found on an airport.

    Attributes:
        STAND:  Parking stand
        DEICING: Winter is coming
        RUNWAY_POINT:  Access to a runway
    """
    STAND = auto()
    DEICING = auto()
    RUNWAY_POINT = auto()


def point_type_from_int(i):
    """Build a value of the PointType enum from an int.

    Args:
        i:  (int)  an integer indexing the point types

    Returns:
        The corresponding PointType

    Raises:
        ValueError:  if @c i does not represent a valid point type.
    """
    if i == 0:
        return PointType.STAND
    elif i == 1:
        return PointType.DEICING
    elif i == 2:
        return PointType.RUNWAY_POINT
    else:
        raise ValueError(f"Invalid point type: {i}")


class WakeVortexCategory(Enum):
    """Wake-vortex categories.

    Attributes:
        LIGHT:  mass <= 7000kg
        MEDIUM:  7000kg < mass < 136000kg
        HEAVY:  136000kg <= mass
    """
    LIGHT = auto()
    MEDIUM = auto()
    HEAVY = auto()


def category_from_string(s):
    """Build a value of the WakeVortexCategory enum from its string representation.

    Args:
        s:  (str)  a string representing a wake-vortex category

    Returns:
        The corresponding WakeVortexCategory.

    Raises:
        ValueError:  if @c s does not represent a valid category.
    """
    if s == "L":
        return WakeVortexCategory.LIGHT
    elif s == "M":
        return WakeVortexCategory.MEDIUM
    elif s == "H":
        return WakeVortexCategory.HEAVY
    else:
        raise ValueError(f"Unknown wake vortex category: {s}")


## Runways area (in meters)
RUNWAY_WIDTH = 90
## Taxiways area (in meters)
TAXIWAY_WIDTH = 15


class AirportPoint(geometry.Point):
    """Point of the airport.

    Attributes:
        name:  (str)  Name of the point
        type:  (airport.PointType)  Type of point
    """

    def __init__(self, name, pt_type, point):
        """The class initializer.

        Args:
            name:  (str)  name of the point
            pt_type:  (airport.PointType)  type of point
            point:  (geometry.Point)  location
        """
        super().__init__(point.x, point.y)
        self.name = name
        self.type = pt_type

    def __repr__(self):
        """Representation of the point.

        Returns:
            A string of the form \"<airport.AirportPoint name>\".
        """
        return f"<airport.AirportPoint {self.name}>"


class Taxiway(geometry.PolyLine):
    """Taxiway portion of the airport.

    Attributes:
        taxi_name:  (str)  Name of the taxiway that it belongs to
        speed:  (int)  Maximum speed on the portion in m/s
        cat:  (airport.WakeVortexCategory)  Maximum allowed wake vortex category
        one_way:  (bool)  Is it a one-way portion?
    """

    def __init__(self, taxi_name, speed, cat, one_way, coords):
        """The class initializer.

        Args:
            taxi_name:  (str)  name of the taxiway
            speed:  (int)  maximum speed on the portion in m/s
            cat: (airport.WakeVortexCategory) maximum allowed wake vortex category
            one_way:  (bool)  true if the portion is one-way
            coords:  (geometry.Point iterable)  the points describing the portion
        """
        super().__init__(coords)
        self.taxi_name = taxi_name
        self.speed = speed
        self.cat = cat
        self.one_way = one_way

    def __repr__(self):
        """Representation of the taxiway portion.

        Returns:
            A string of the form \"<airport.Taxiway taxi_name>\".
        """
        return f"<airport.Taxiway {self.taxi_name}>"


class Runway(geometry.PolyLine):
    """Runway of the airport.

    Attributes:
        name:  (str)  Name of the runway
        qfus:  (str tuple)  Runway directions
        runway_points:  (airport.AirportPoint tuple)  Access points to the runway
    """

    def __init__(self, name, qfu1, qfu2, ends, runway_points):
        """The class initializer.

        Args:
            name:  (str)  name of the runway
            qfu1:  (str)  first runway direction
            qfu2:  (str)  second runway direction
            ends:  (geometry.Point list)  end-points of the runway
            runway_points:  (airport.AirportPoint tuple)  access points to the runway
        """
        super().__init__(ends)
        self.name = name
        self.qfus = (qfu1, qfu2)
        self.runway_points = runway_points

    def __repr__(self):
        """Representation of the runway.

        Returns:
            A string of the form \"<airport.Runway name>\".
        """
        return f"<airport.Runway {self.name}>"


class Airport:
    """Whole airport description.

    Attributes:
        name:  (str)  Airport name
        points:  (airport.AirportPoint tuple)  Points on the airport
        taxiways:  (airport.Taxiway tuple)  Taxi-way portions
        runways:  (airport.Runway tuple)  Runways
    """
    '''
    def __init__(self, name, points, taxiways, runways):
        """The class initializer.

        Args:
            name:  (str)  airport name
            points:  (airport.AirportPoint tuple)  points on the airport
            taxiways:  (airport.Taxiway tuple)  taxiway portions
            runways:  (airport.Runway tuple)  runways
        """
        self.name = name
        self.points = points
        self.taxiways = taxiways
        self.runways = runways
    '''
    def __init__(self, name, points, taxiways, runways):
        """The class initializer.

        Args:
            name:  (str)  airport name
            points:  (airport.AirportPoint tuple)  points on the airport
            taxiways:  (airport.Taxiway tuple)  taxiway portions
            runways:  (airport.Runway tuple)  runways
        """
        self.name = name
        self.points = points
        self.taxiways = taxiways
        self.runways = runways
        self.pt_dict = {pt.name : pt for pt in self.points}
        self.qfu_dict = {}
        for qf in self.runways:
            self.qfu_dict[qf.qfus[0]]= qf
            self.qfu_dict[qf.qfus[1]]= qf
            
                         
        
    def __repr__(self):
        """Representation of the airport.

        Returns:
            A string of the form \"<airport.Airport name>\".
        """
        return f"<airport.Airport {self.name}>"
    def get_qfu(self, name):
        """Checks whether a given QFU exists on the airport.

        Args:
            name:  (str)  name of the QFU

        Returns:
            str | None: @c name if it is a valid QFU, @c None otherwise
        """
        for rwy in self.runways:
            if name == rwy.qfus[0] or name == rwy.qfus[1]:
                return name
    def get_point(self,name):
         return self.pt_dict[name]
    def get_runway(self,name):
        return self.qfu_dict[name]

# Reading an airport file
def from_file(filename):
    """Parse an airport description file to extract information.

    Args:
        filename:  (str)  the name of the file containing the airport description

    Returns:
        Airport: the parsed airport information.
    """
    print(f"Loading airport {filename}...")
    with open(filename) as file:
        name = file.readline().strip()
        points, taxiways, runways = [], [], []
        for line in file:
            try :
                words = line.strip().split()
                if words[0] == "P":  # Point description
                    name = words[1]
                    point_type = point_type_from_int(int(words[2]))
                    point = geometry.point_from_string(words[3])
                    airport_point = AirportPoint(name, point_type, point)
                    points.append(airport_point)
                elif words[0] == "L":  # Taxiway description
                    taxi_name = words[1]
                    speed = int(words[2])
                    cat = category_from_string(words[3])
                    one_way = (words[4] == "S")
                    pts = geometry.points_from_strings(words[5:])
                    taxiway = Taxiway(taxi_name, speed, cat, one_way, pts)
                    taxiways.append(taxiway)
                elif words[0] == "R":  # Runway description
                    name = words[1]
                    qfu1 = words[2]
                    qfu2 = words[3]
                    pts = tuple(words[4].split(","))
                    ends = geometry.points_from_strings(words[5:])
                    runway = Runway(name, qfu1, qfu2, ends, pts)
                    runways.append(runway)
            except  Exception :
                print(line)
        return Airport(name, tuple(points), tuple(taxiways), tuple(runways))


def from_file2(filename):
    """Parse an airport description file to extract information.

    Args:
        filename:  (str)  the name of the file containing the airport description

    Returns:
        Airport: the parsed airport information.
    """
    print(f"Loading airport {filename}...")
    with open(filename) as file:
        name = file.readline().strip()
        points, taxiways, runways = [], [], []
        for line in file:
            words = line.strip().split()
            if words[0] == "P":  # Point description
                name = words[1]
                point_type = point_type_from_int(int(words[2]))
                point = geometry.point_from_string(words[3])
                airport_point = AirportPoint(name, point_type, point)
                points.append(airport_point)
            elif words[0] == "L":  # Taxiway description
                taxi_name = words[1]
                speed = int(words[2])
                cat = category_from_string(words[3])
                one_way = (words[4] == "S")
                pts = geometry.points_from_strings(words[5:])
                taxiway = Taxiway(taxi_name, speed, cat, one_way, pts)
                taxiways.append(taxiway)
            elif words[0] == "R":  # Runway description
                name = words[1]
                qfu1 = words[2]
                qfu2 = words[3]
                pts = tuple(words[4].split(","))
                ends = geometry.points_from_strings(words[5:])
                runway = Runway(name, qfu1, qfu2, ends, pts)
                runways.append(runway)
        return Airport(name, tuple(points), tuple(taxiways), tuple(runways))

'''
def get_point(apt, name):
    """Get a point from its name on the airport.

    Args:
        apt:  (airport.Airport)  the airport in which to search
        name:  (str)  name of the point

    Returns:
        The corresponding airport.AirportPoint.

    Raises:
        KeyError: if the name does not correspond to an existing point.
    """
    for point in apt.points:
        if point.name == name:
            return point
'''
'''
def get_point(apt, name):
    """Get a point from its name on the airport.

    Args:
        apt:  (airport.Airport)  the airport in which to search
        name:  (str)  name of the point

    Returns:
        The corresponding airport.AirportPoint.

    Raises:
        KeyError: if the name does not correspond to an existing point.
    """
    a=apt.pt_dict.get(name,42)
    if a !=42:
        return a

'''
'''
def get_runway(apt, name):
    """Get a runway from a given QFU.

    Args:
        apt:  (airport.Airport)  the airport in which to search
        name:  (str)  name of the QFU

    Returns:
        The airport.Runway on which the QFU is found.

    Raises:
        KeyError: if the name does not correspond to an existing QFU.
    """
    for rwy in apt.runways:
        if name == rwy.qfus[0] or name == rwy.qfus[1]:
            return rwy
'''
'''
def get_runway(apt, name):
    """Get a runway from a given QFU.

    Args:
        apt:  (airport.Airport)  the airport in which to search
        name:  (str)  name of the QFU

    Returns:
        The airport.Runway on which the QFU is found.

    Raises:
        KeyError: if the name does not correspond to an existing QFU.
    """
    a=apt.qfu_dict.get(name,42)
    if a !=42:
        return a
'''
