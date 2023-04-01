"""A library for simulating multipath propagation of electromagnetic waves under interference."""

from __future__ import annotations
from math import pi, tau, cos, sin, atan2, hypot
from random import random
from itertools import pairwise
from typing import Iterable, Iterator
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

    def get_multipath(self, starting_number: int, receiver_diameter: float, max_reflections: int, power_multiplier: float = 0.9) -> Multipath:
        """Finds the path of a number of propagated transmissions distributed evenly in every direction.
        Each path returns with a vector indicating the last direction."""
        print("Calculating propagated paths...", end="\r")
        paths = []
        for n in range(starting_number):
            starting_angle = tau * (n / starting_number)
            starting_vector = Vector(cos(starting_angle), sin(starting_angle))
            path = self.get_path(starting_vector, receiver_diameter, max_reflections, power_multiplier)
            # figure out if path propagated
            if path is not None:
                paths.append(path)
                print(f"Calculating propagated paths... (number: {len(paths)}, angle: {round(starting_angle * 180 / pi)})", end="\r")
        multipath = Multipath(paths, starting_number)
        print()
        return multipath

    def get_path(self, starting_vector: Vector, receiver_diameter: float, max_reflections: int, power_multiplier: float = 0.9) -> Path | None:
        """Finds the path of one transmission, returns with vector only if max_reflections is not reached."""
        points = [self.transmitter.position.copy()]
        hits = []
        ray = Ray(points[0], starting_vector)
        vector = starting_vector
        segment_ignore = None
        for r in range(max_reflections):
            closest = False
            closest_point = Point(0, 0)
            for interferer in self.interferers:
                for s, segment in enumerate(interferer.segments):
                    if segment is segment_ignore:
                        continue
                    intersection = ray.intersect(segment)
                    if type(intersection) is Point:
                        point = intersection
                        # closest intersection is the point of reflection
                        if not closest or ray.p1.distance(point) < ray.p1.distance(closest_point):
                            closest = True
                            closest_point = point
                            closest_segment = segment
                            closest_interferer = interferer

            if not closest:
                return None
            points.append(closest_point)
            hits.append(closest_interferer)
            # calculate reflected ray
            normal = Vector(-closest_segment.v.y, closest_segment.v.x).normalized()
            vector = vector.reflect(normal)

            # determine ray propagation to target
            if ray.p1.distance(self.receiver.position) < ray.p1.distance(closest_point):
                if ray.distance(self.receiver.position) < receiver_diameter / 2:
                    points.append(self.receiver.position.copy())
                    path = Path(points, hits, power_multiplier)
                    return path

            ray = Ray(closest_point, vector)
            segment_ignore = closest_segment
        return None


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
    hits: int

    def __init__(self, points: list[Point], closed=True) -> None:
        self.points = points
        self.segments = []
        if closed:
            all_points = points + [points[0]]
        else:
            all_points = points
        for point_1, point_2 in pairwise(all_points):
            segment = Segment(point_1, point_2)
            self.segments.append(segment)
        self.hits = 0

    @classmethod
    def shape(cls, points: list[Point], position: Point, scale: float, rotation: float) -> Interferer:
        """Create a shape with points and transformations from which an interferer will be created."""
        for point in points:
            angle = atan2(point.y, point.x) + rotation
            radius = hypot(point.x, point.y) * scale
            point.x = position.x + radius * cos(angle)
            point.y = position.y + radius * sin(angle)
        return cls(points)

    @classmethod
    def square(cls, position: Point, length: float, rotation: float) -> Interferer:
        """Create a square shaped interferer."""
        length_half = length / 2
        points = [Point(length_half, length_half),
                  Point(length_half, -length_half),
                  Point(-length_half, -length_half),
                  Point(-length_half, length_half)]
        return cls.shape(points, position, 1, rotation)

    @classmethod
    def rectangle(cls, position: Point, length: float, width: float, rotation: float) -> Interferer:
        """Create a rectangle shaped interferer."""
        length_half = length / 2
        width_half = width / 2
        points = [Point(length_half, width_half),
                  Point(length_half, -width_half),
                  Point(-length_half, -width_half),
                  Point(-length_half, width_half)]
        return cls.shape(points, position, 1, rotation)

    @classmethod
    def polygon(cls, position: Point, diameter: float, number_sides: int, rotation: float) -> Interferer:
        """Create a regular polygon shaped interferer."""
        radius = diameter / 2
        points = []
        for p in range(number_sides):
            angle = tau * (p / number_sides)
            point = Point(radius * cos(angle), radius * sin(angle))
            points.append(point)
        return cls.shape(points, position, 1, rotation)

    @classmethod
    def circle(cls, position: Point, radius: float, number_points: int) -> Interferer:
        """Create a circular shaped interferer."""
        points = []
        for p in range(number_points):
            angle = tau * (p / number_points)
            point = Point(radius * cos(angle), radius * sin(angle))
            points.append(point)
        return cls.shape(points, position, 1, 0)

    @classmethod
    def blob(cls, position: Point, average_radius: float, number_points: int, smoothing_factor: float = 0, smoothing_iterations: int = 0) -> Interferer:
        """Create a random smoothly shaped interferer."""
        points = []
        for p in range(number_points):
            angle = tau * (p / number_points)
            radius = average_radius * (0.75 + random() / 2)
            point = Point(radius * cos(angle), radius * sin(angle))
            points.append(point)
        for s in range(smoothing_iterations):
            for p in range(number_points):
                point_left = points[p]
                point_middle = points[(p + 1) % number_points]
                point_right = points[(p + 2) % number_points]
                point_target = Point((point_left.x + point_right.x) / 2, (point_left.y + point_right.y) / 2)
                points[(p + 1) % number_points] = Point(point_middle.x * (1 - smoothing_factor) + point_target.x * smoothing_factor, point_middle.y * (1 - smoothing_factor) + point_target.y * smoothing_factor)
        return cls.shape(points, position, 1, tau * random())


class Multipath:
    """A structure containing multiple propagated paths."""
    paths: list[Path]
    starting_number: int

    def __init__(self, paths: list[Path], starting_number: int) -> None:
        self.paths = paths
        self.starting_number = starting_number
    
    def __iter__(self) -> Iterator[Path]:
        for path in self.paths:
            yield path

    def signals(self, signal: DigitalSignal) -> Iterable[DigitalSignal]:
        for path in self.paths:
            yield path.signal(signal)


class Path:
    """Propagated path containing points of travel, final power and delay."""
    points: list[Point]
    power: float
    delay: float
    hits: list[Interferer]

    def __init__(self, points: list[Point], hits: list[Interferer], power_multiplier: float = 0.9) -> None:
        self.points = points
        self.delay = 0
        for point_1, point_2 in pairwise(points):
            self.delay += point_1.distance(point_2) / 2.99792458e8
        self.power = 1
        for p in range(len(points) - 2):
            self.power *= power_multiplier
        self.hits = hits

    def __iter__(self) -> Iterator[Point]:
        for point in self.points:
            yield point

    def signal(self, signal: DigitalSignal) -> DigitalSignal:
        times = []
        strengths = []
        for time, strength in signal:
            times.append(time + self.delay)
            strengths.append(strength * self.power)
        signal = DigitalSignal(times, strengths)
        return signal


class DigitalSignal:
    number: int
    times: list[float]
    strengths: list[float]

    def __init__(self, times: list[float], strengths: list[float]) -> None:
        self.number = len(times)
        self.times = times
        self.strengths = strengths

    def __iter__(self) -> Iterator[tuple[float, float]]:
        for n in range(self.number):
            yield self.times[n], self.strengths[n]

    def strength(self, time: float) -> float:
        for s, (time_1, time_2) in enumerate(pairwise(self.times)):
            if time_1 <= time <= time_2:
                balance = (time - time_1) / (time_2 - time_1)
                strength = (1 - balance) * self.strengths[s] + balance * self.strengths[s + 1]
                return strength
        return 0


if __name__ == "__main__":
    from time import sleep
    print("This file is just a library, does not work on its own.")
    sleep(5)
