"""A library for simulating multipath propagation of electromagnetic waves under interference."""

from __future__ import annotations
from math import tau, cos, sin, atan2, hypot
from itertools import pairwise
from typing import Iterable
from euclid import Point2 as Point, Vector2 as Vector, Ray2 as Ray, LineSegment2 as Segment


class System:
    """A multipath propagation system where a transmitter and receiver exist as well as interferers."""
    transmitter: Transmitter
    receiver: Receiver
    interferers: list[Interferer]

    def __init__(self, transmitter: Transmitter, receiver: Receiver, interferers: list[Interferer]) -> None:
        self.transmitter = transmitter
        self.receiver = receiver
        self.interferers = interferers

    def get_multipath(self, starting_number: int, receiver_diameter: float, max_reflections: int) -> Multipath:
        """Finds the path of a number of propagated transmissions distributed evenly in every direction.
        Each path returns with a vector indicating the last direction."""
        paths = []
        for n in range(starting_number):
            starting_angle = tau * (n / starting_number)
            starting_vector = Vector(cos(starting_angle), sin(starting_angle))
            path = self.get_path(starting_vector, receiver_diameter, max_reflections)
            if path is not None:
                paths.append(path)
        multipath = Multipath(paths)
        return multipath

    def get_path(self, starting_vector: Vector, receiver_diameter: float, max_reflections: int) -> Path | None:
        """Finds the path of one transmission, returns with vector only if max_reflections is not reached."""
        points = [self.transmitter.position.copy()]
        ray = Ray(points[0], starting_vector)
        vector = starting_vector
        segment_ignore = None
        for r in range(max_reflections):
            closest = False
            closest_point = None
            closest_segment = None
            for interferer in self.interferers:
                for s, segment in enumerate(interferer.segments):
                    if segment is segment_ignore:
                        continue
                    intersection = ray.intersect(segment)
                    if type(intersection) is Point:
                        point = intersection
                        if not closest or ray.p1.distance(point) < ray.p1.distance(closest_point):
                            closest = True
                            closest_point = point
                            closest_segment = segment

            if not closest:
                return
            points.append(closest_point)
            normal = Vector(-closest_segment.v.y, closest_segment.v.x).normalized()
            vector = vector.reflect(normal)
            ray = Ray(closest_point, vector)
            segment_ignore = closest_segment
            if ray.distance(self.receiver.position) < receiver_diameter / 2:
                points.append(self.receiver.position.copy())
                path = Path(points)
                return path
        return


class Transmitter:
    """A device that sends electromagnetic waves in every direction."""
    position: Point

    def __init__(self, position: Point) -> None:
        self.position = position


class Receiver:
    """A device that receives electromagnetic waves from a transmitter."""
    position: Point

    def __init__(self, position: Point) -> None:
        self.position = position


class Interferer:
    """An obstruction between the transmitter and receiver that reflects incoming light."""
    points: list[Point]
    segments: list[Segment]

    def __init__(self, points: list[Point]) -> None:
        self.points = points
        self.segments = []
        for point_1, point_2 in pairwise(points + [points[0]]):
            segment = Segment(point_1, point_2)
            self.segments.append(segment)

    @classmethod
    def shape(cls, points: list[Point], position: Point, scale: float, rotation: float) -> Interferer:
        for point in points:
            angle = atan2(point.y, point.x) + rotation
            radius = hypot(point.x, point.y) * scale
            point.x = position.x + radius * cos(angle)
            point.y = position.y + radius * sin(angle)
        return cls(points)

    @classmethod
    def square(cls, position: Point, length: float, rotation: float) -> Interferer:
        length_half = length / 2
        points = [Point(length_half, length_half),
                  Point(length_half, -length_half),
                  Point(-length_half, -length_half),
                  Point(-length_half, length_half)]
        return cls.shape(points, position, 1, rotation)

    @classmethod
    def rectangle(cls, position: Point, length: float, width: float, rotation: float) -> Interferer:
        length_half = length / 2
        width_half = width / 2
        points = [Point(length_half, width_half),
                  Point(length_half, -width_half),
                  Point(-length_half, -width_half),
                  Point(-length_half, width_half)]
        return cls.shape(points, position, 1, rotation)

    @classmethod
    def circle(cls, position: Point, radius: float, number_points: int) -> Interferer:
        points = []
        for p in range(number_points):
            angle = tau * (p / number_points)
            point = Point(radius * cos(angle), radius * sin(angle))
            points.append(point)
        return cls.shape(points, position, 1, 0)


class Multipath:
    paths: list[Path]

    def __init__(self, paths: list[Path]) -> None:
        self.paths = paths
    
    def __iter__(self) -> Iterable[Path]:
        for path in self.paths:
            yield path


class Path:
    points: list[Point]
    delay: float
    attenuation: float

    def __init__(self, points: list[Point]) -> None:
        self.points = points
        self.delay = 0
        for point_1, point_2 in pairwise(points):
            self.delay += point_1.distance(point_2) / 2.99792458e8
        self.attenuation = 0
        for p in range(len(points) - 2):
            self.attenuation *= 0.5

    def __iter__(self) -> Iterable[Point]:
        for point in self.points:
            yield point