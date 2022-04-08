"""A library for simulating multipath propagation of electromagnetic waves under interference."""

from __future__ import annotations
from math import tau, cos, sin, atan2, hypot
from itertools import pairwise
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

    def get_paths_propagated(self, starting_number: int, receiver_diameter: float, max_reflections: int) -> list[tuple[list[Point], Vector]]:
        """Finds the path of a number of propagated transmissions distributed evenly in every direction.
        Each path returns with a vector indicating the last direction."""
        paths = []
        for n in range(starting_number):
            angle = tau * (n / starting_number)
            path = self.get_path(Vector(cos(angle), sin(angle)), max_reflections)
            if path[1] is None:
                continue
            propagated_ray = Ray(path[0][-1], path[1])
            if propagated_ray.distance(self.receiver.position) < receiver_diameter / 2:
                paths.append(path)
        return paths

    def get_paths(self, starting_number: int, max_reflections: int) -> list[tuple[list[Point], Vector | None]]:
        """Finds the path of a number of transmissions distributed evenly in every direction.
        Each path returns with vector only if max_reflections is not reached."""
        paths = []
        for n in range(starting_number):
            angle = tau * (n / starting_number)
            paths.append(self.get_path(Vector(cos(angle), sin(angle)), max_reflections))
        return paths

    def get_path(self, starting_vector: Vector, max_reflections: int) -> tuple[list[Point], Vector | None]:
        """Finds the path of one transmission, returns with vector only if max_reflections is not reached."""
        path = [self.transmitter.position.copy()]
        ray = Ray(path[0], starting_vector)
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
                return path, vector
            path.append(closest_point)
            normal = Vector(-closest_segment.v.y, closest_segment.v.x).normalized()
            vector = vector.reflect(normal)
            ray = Ray(closest_point, vector)
            segment_ignore = closest_segment
        return path, None


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
    def square(cls, length: float, position: Point, rotation: float) -> Interferer:
        length_half = length / 2
        points = [Point(length_half, length_half),
                  Point(length_half, -length_half),
                  Point(-length_half, -length_half),
                  Point(-length_half, length_half)]
        return cls.shape(points, position, 1, rotation)