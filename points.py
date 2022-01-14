from __future__ import annotations
from math import atan2, cos, hypot, sin
from copy import copy
from collections.abc import Iterator


class Point:
    """Two-dimensional point represented in cartesian coordinates."""
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        """Create a point from cartesian coordinates."""
        self.x = x
        self.y = y

    def __iter__(self) -> Iterator[float]:
        """Iterate through the x and y."""
        yield self.x
        yield self.y

    def __add__(self, point: Point, /) -> Point:
        """(+) Add caller point with parameter point, without modification to the existing point."""
        return copy(self).__iadd__(point)

    def __iadd__(self, point: Point, /) -> Point:
        """(+=) Add caller point with parameter point, with modification to the existing point."""
        return self.add(point)

    def __sub__(self, point: Point, /) -> Point:
        """(-) Subtract parameter point from the caller point, without modification to the existing point."""
        return copy(self).__isub__(point)

    def __isub__(self, point: Point, /) -> Point:
        """(-=) Subtract parameter point from the caller point, with modification to the existing point."""
        return self.subtract(point)

    def __mul__(self, multiplier: float, /) -> Point:
        """(*) Multiply point coordinates by a number, without modification to the existing point."""
        return copy(self).__imul__(multiplier)

    def __rmul__(self, multiplier: float, /) -> Point:
        """(*) Multiply point coordinates by a number, without modification to the existing point."""
        return self.__mul__(multiplier)

    def __imul__(self, multiplier: float, /) -> Point:
        """(*=) Multiply point coordinates by a number, with modification to the existing point."""
        return self.multiply(multiplier)

    def __truediv__(self, divisor: float, /) -> Point:
        """(/) Divide point coordinates by a number, without modification to the existing point."""
        return copy(self).__truediv__(divisor)

    def __rtruediv__(self, dividend: float, /) -> tuple[float, float]:
        """(/) Divide a number twice by each point coordinate."""
        return dividend / self.x, dividend / self.y

    def __itruediv__(self, divisor: float, /) -> Point:
        """(/=) Divide point coordinates by a number, with modification to the existing point."""
        return self.divide(divisor)

    def __pos__(self) -> Point:
        return copy(self)

    def __neg__(self) -> Point:
        return copy(self).multiply(-1)

    def __matmul__(self, point: Point, /) -> float:
        """(@) Find the dot product of caller and parameter points."""
        return self.dot_product(point)

    def __mod__(self, point: Point, /) -> float:
        """(%) Find the cross product of caller and parameter points."""
        return self.cross_product(point)

    def change(self, point: Point, /) -> Point:
        """Change coordinates of caller point to match parameter point."""
        self.x = point.x
        self.y = point.y
        return self

    def replace(self, x, y) -> Point:
        """Replace individual coordinates of caller point with a set of x and y values."""
        self.x = x
        self.y = y
        return self

    def add(self, point: Point, /) -> Point:
        """Add caller point with parameter point with, modification to the existing point."""
        self.x += point.x
        self.y += point.y
        return self

    def subtract(self, point: Point, /) -> Point:
        """Subtract parameter point from the caller point, with modification to the existing point."""
        self.x -= point.x
        self.y -= point.y
        return self

    def multiply(self, multiplier: float, /) -> Point:
        """Multiply point coordinates by a number, with modification to the existing point."""
        self.x *= multiplier
        self.y *= multiplier
        return self

    def divide(self, divisor: float, /) -> Point:
        """Divide point coordinates by a number, with modification to the existing point."""
        self.x /= divisor
        self.y /= divisor
        return self

    def length(self) -> float:
        """Find the distance from caller point to the origin."""
        return hypot(self.x, self.y)

    def distance(self, point: Point, /) -> float:
        """Find the Euclidean distance between caller and parameter points."""
        return hypot(self.x - point.x, self.y - point.y)

    def direction(self, point: Point, /) -> float:
        """Find the direction in radians from the caller point to the parameter point."""
        return atan2(self.y - point.y, self.x - point.x)

    def dot_product(self, point: Point, /) -> float:
        """Find the dot product of caller and parameter points."""
        return self.x * point.x + self.y * point.y

    def cross_product(self, point: Point, /) -> float:
        """Find the cross product of caller and parameter points."""
        return self.x * point.y - self.y * point.x

    @classmethod
    def origin(cls) -> Point:
        """Create a cartesian point placed on the origin."""
        return cls(0., 0.)

    @classmethod
    def polar(cls, radius: float, theta: float) -> Point:
        """Create a cartesian point from polar coordinates."""
        return cls(radius * cos(theta), radius * sin(theta))
