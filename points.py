from __future__ import annotations
from math import atan2, cos, hypot, sin
from collections.abc import Iterator


class Point:
    """Two-dimensional point represented in cartesian coordinates."""
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        """Instantiate a point from cartesian coordinates."""
        self.x = x
        self.y = y

    def __iter__(self) -> Iterator[float]:
        """Iterate through the pair of coordinates."""
        yield self.x
        yield self.y

    def __add__(self, point: Point, /) -> Point:
        """(+) Add caller point with parameter point, without modification to point."""
        return self.copy().__iadd__(point)

    def __iadd__(self, point: Point, /) -> Point:
        """(+=) Add caller point with parameter point, with modification to caller point."""
        return self.add(point)

    def __sub__(self, point: Point, /) -> Point:
        """(-) Subtract parameter point from caller point, without modification to point."""
        return self.copy().__isub__(point)

    def __isub__(self, point: Point, /) -> Point:
        """(-=) Subtract parameter point from caller point, with modification to caller point."""
        return self.sub(point)

    def __mul__(self, multiplier: float, /) -> Point:
        """(*) Multiply point coordinates by a number, without modification to point."""
        return self.copy().__imul__(multiplier)

    def __rmul__(self, multiplier: float, /) -> Point:
        """(*) Multiply point coordinates by a number, without modification to point."""
        return self.__mul__(multiplier)

    def __imul__(self, multiplier: float, /) -> Point:
        """(*=) Multiply point coordinates by a number, with modification to point."""
        return self.mul(multiplier)

    def __truediv__(self, divisor: float, /) -> Point:
        """(/) Divide point coordinates by a number, without modification to point."""
        return self.copy().__truediv__(divisor)

    def __itruediv__(self, divisor: float, /) -> Point:
        """(/=) Divide point coordinates by a number, with modification to point."""
        return self.div(divisor)

    def __pos__(self) -> Point:
        """(+) Return the same point instance."""
        return self

    def __neg__(self) -> Point:
        """(-) Flip the sign of point coordinates, without modification to point."""
        return self.copy().mul(-1)

    def __matmul__(self, point: Point, /) -> float:
        """(@) Find the dot product of two points as vectors."""
        return self.dot(point)

    def __mod__(self, point: Point, /) -> float:
        """(%) Find the cross product of two points as vectors."""
        return self.cross(point)

    def set(self, point: Point, /) -> Point:
        """Set coordinates of caller point to match parameter point."""
        self.x = point.x
        self.y = point.y
        return self

    def add(self, point: Point, /) -> Point:
        """(+) Add caller point with parameter point, with modification to caller point."""
        self.x += point.x
        self.y += point.y
        return self

    def sub(self, point: Point, /) -> Point:
        """Subtract parameter point from caller point, with modification to caller point."""
        self.x -= point.x
        self.y -= point.y
        return self

    def mul(self, multiplier: float, /) -> Point:
        """Multiply point coordinates by a number, with modification to point."""
        self.x *= multiplier
        self.y *= multiplier
        return self

    def div(self, divisor: float, /) -> Point:
        """Divide point coordinates by a number, with modification to point."""
        self.x /= divisor
        self.y /= divisor
        return self

    def len(self) -> float:
        """Find the distance to the origin."""
        return hypot(self.x, self.y)

    def dist(self, point: Point, /) -> float:
        """Find the distance between two points."""
        return hypot(self.x - point.x, self.y - point.y)

    def angle(self, point: Point, /) -> float:
        """Find the angle in radians from the caller point to the parameter point."""
        return atan2(self.y - point.y, self.x - point.x)

    def dot(self, point: Point, /) -> float:
        """Find the dot product of two points as vectors."""
        return self.x * point.x + self.y * point.y

    def cross(self, point: Point, /) -> float:
        """Find the cross product of two points as vectors."""
        return self.x * point.y - self.y * point.x

    def copy(self) -> Point:
        """Get a copied point instance."""
        return Point(self.x, self.y)

    @classmethod
    def origin(cls) -> Point:
        """Instantiate a point from the origin."""
        return cls(0., 0.)

    @classmethod
    def polar(cls, radius: float, theta: float) -> Point:
        """Instantiate a cartesian point from polar coordinates."""
        return cls(radius * cos(theta), radius * sin(theta))


class Segment:
    point_1: Point
    point_2: Point

    def __init__(self, point_1: Point, point_2: Point) -> None:
        self.point_1 = point_1
        self.point_2 = point_2

    def change(self, line: Segment, /) -> Segment:
        self.point_1 = line.point_1
        self.point_2 = line.point_2
        return self

    def replace(self, point_1, point_2) -> Segment:
        self.point_1 = point_1
        self.point_2 = point_2
        return self

    def add(self, point: Point, /) -> Segment:
        self.point_1.add(point)
        self.point_2.add(point)
        return self

    def sub(self, point: Point, /) -> Segment:
        self.point_1.sub(point)
        self.point_2.sub(point)
        return self

    def mul(self, multiplier: float, /) -> Segment:
        self.point_1.mul(multiplier)
        self.point_2.mul(multiplier)
        return self

    def div(self, divisor: float, /) -> Segment:
        self.point_1.div(divisor)
        self.point_2.div(divisor)
        return self

    def len(self) -> float:
        return self.point_1.dist(self.point_2)

    def angle(self) -> float:
        return self.point_1.angle(self.point_2)


class Line(Segment):
    def __init__(self, point_1: Point, point_2: Point) -> None:
        super().__init__(point_1, point_2)


class Ray(Segment):
    def __init__(self, point_1: Point, point_2: Point) -> None:
        super().__init__(point_1, point_2)






class Polygon:
    sides: list[Segment]

    def __init__(self, points: list[Point]) -> None:
        self.points = points

    def side(self, number: int) -> Iterator[Point]:
        return 1

pol = Polygon([Point(4, 3), Point(5, 3)])
print(pol.side(0))

p1 = Point(5, 5)
print(p1 is Point)