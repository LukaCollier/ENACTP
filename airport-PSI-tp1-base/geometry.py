## @namespace geometry
"""
Geometry classes and utilities.

This module provides two classes to  represent simple 2D objects:
points and poly-lines. Points (or vectors) are described by their
coordinates (in meters) in a 2D Euclidean space, and handle the classic
operations such as addition, subtraction, dot product, etc.

Poly-lines are simply described by a sequence of points, and can provide
their length.
"""

import math


class Point:
    """A 2D point described by its coordinates in meters.

    Attributes:
        x:  (int)  x-coordinate in meters
        y:  (int)  y-coordinate in meters
    """

    def __init__(self, x, y):
        """The class initializer.

        Args:
            x:  (int)  the x-coordinate in meters
            y:  (int)  the y-coordinate in meters
        """
        self.x = x
        self.y = y

    def __repr__(self):
        """Representation of the point.

        Returns:
            A string of the form \"(x, y)\".
        """
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        """Vector addition

        Args:
            other:  (geometry.Point)  the other vector

        Returns:
            A new vector (geometry.Point) corresponding to the addition.
        """
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Vector subtraction.

        Args:
            other:  (type geometry.Point)  the other vector

        Returns:
            A new vector (geometry.Point) corresponding to the subtraction.
        """
        return Point(self.x - other.x, self.y - other.y)

    def __rmul__(self, k):
        """Vector multiplication by a scalar.

        Args:
            k:  (int)  the multiplication factor

        Returns:
            A new vector (geometry.Point) corresponding to the multiplication.
        """
        return Point(k * self.x, k * self.y)

    def __abs__(self):
        """Euclidean norm.

        Returns:
            A float corresponding to the Euclidean distance between the point
            and the origin (0, 0).
        """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def sca(self, other):
        """Scalar product.

        Args:
            other:  (geometry.Point)  another point or vector

        Returns:
            A float corresponding to the scalar product of
            one vector by the `other`.
        """
        return self.x * other.x + self.y * other.y

    def det(self, other):
        """Determinant.

        Args:
            other:  (geometry.Point)  another point or vector

        Returns:
            An int corresponding to the determinant between
            one vector and the `other`.
        """
        return self.x * other.y - self.y * other.x

    def distance(self, other):
        """Distance to another point.

        Args:
            other:  (geometry.Point)  another point or vector

        Returns:
            A float corresponding to the Euclidean distance in meters
            to the `other` point.
        """
        return abs(self - other)

    def distance_to_segment(self, a, b):
        """Distance to a segment.

        Args:
            a:  (geometry.Point)  first end of the segment
            b:  (geometry.Point)  second end of the segment

        Returns:
            A float corresponding to the distance in meters
            to the segment delimited by points `a` and `b`.
        """
        ab = b - a
        ap = self - a
        bp = self - b
        if ab.sca(ap) <= 0:
            return abs(ap)
        elif ab.sca(bp) >= 0:
            return abs(bp)
        else:
            return abs(ab.det(ap)) / abs(ap)


class PolyLine:
    """A 2D poly-line described by a series of points.

    Attributes:
        length:  (float)  Overall length of the poly-line in meters
        coords:  (geometry.Point iterable)  Points describing the poly-line
    """

    def __init__(self, coords):
        """The class initializer.

        Args:
            coords:  (geometry.Point iterable)  the points in the poly-line
        """
        self.length = sum(pi.distance(coords[i - 1])
                          for i, pi in enumerate(coords[1:]))
        self.coords = coords

    def __repr__(self):
        """Basic representation of the poly-line.

        Returns:
            A string of the form \"<geometry.PolyLine length>\".
        """
        return f"<geometry.PolyLine {len(self)}>"

    def __str__(self):
        """Representation of the poly-line by its points.

        Returns:
            A string showing all points in the poly-line.
        """
        points = ", ".join(str(p) for p in self.coords)
        return f"PolyLine {self.length}m: ({points})"

    def __len__(self):
        """Length as the number of points.

        Returns:
            An int corresponding to the number of points in the poly-line.
        """
        return len(self.coords)


def point_from_string(str_xy):
    """Parse an x,y string to construct a point.

    Args:
        str_xy:  (str)  a string of the form \"x,y\"

    Returns:
        A Point with coordinates x and y.

    Raises:
        ValueError:  if @c str_xy is ill-formed
    """
    x, y = map(int, str_xy.split(","))
    return Point(x, y)


def points_from_strings(str_xy_list):
    """Same as geometry.point_from_string, but for a list.

    Args:
        str_xy_list:  (str list)  a list of strings, each of the form \"x,y\"

    Returns:
        A Point list corresponding to the points of coordinates
        (x0, y0), ..., (xn, yn).

    Raises:
        ValueError:  if any of the strings in @c str_xy_list is ill-formed
    """
    return tuple(point_from_string(s) for s in str_xy_list)
