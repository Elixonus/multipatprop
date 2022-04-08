from __future__ import annotations
from math import pi, tau, cos, sin, atan2
from itertools import pairwise
from euclid import Vector2 as Vector, Point2 as Point, Ray2 as Ray, LineSegment2 as Segment, Circle


class System:
    transmitter: Transmitter
    receiver: Receiver
    interferers: list[Interferer]

    def __init__(self, transmitter: Transmitter, receiver: Receiver, interferers: list[Interferer]) -> None:
        self.transmitter = transmitter
        self.receiver = receiver
        self.interferers = interferers

    def get_paths_propagated(self, starting_number: int, receiver_diameter: float, max_reflections: int) -> list[list[Point2D]]:
        paths = []
        for n in range(starting_number):
            angle = tau * (n / starting_number)
            path = self.get_path(Vector(cos(angle), sin(angle)), max_reflections)
            if path[1] is None:
                continue
            propagated_ray = Ray2D(path[0][-1], angle=path[1])
            receiver_circle = Circle(self.receiver.position, receiver_diameter / 2)
            if len(propagated_ray.intersection(receiver_circle)) > 0:
                path[0].append(self.receiver.position)
                paths.append(path[0])
        return paths


    def get_paths(self, starting_number: int, max_reflections: int) -> list[tuple[list[Point], Vector | None]]:
        paths = []
        for n in range(starting_number):
            angle = tau * (n / starting_number)
            paths.append(self.get_path(Vector(cos(angle), sin(angle)), max_reflections))
        return paths


    def get_path(self, starting_vector: Vector, max_reflections: int) -> tuple[list[Point], Vector | None]:
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
    position: Point

    def __init__(self, position: Point) -> None:
        self.position = position


class Receiver:
    position: Point

    def __init__(self, position: Point) -> None:
        self.position = position


class Interferer:
    points: list[Point]
    segments: list[Segment]

    def __init__(self, points: list[Point]) -> None:
        self.points = points
        self.segments = []
        for point_1, point_2 in pairwise(points + [points[0]]):
            segment = Segment(point_1, point_2)
            self.segments.append(segment)


