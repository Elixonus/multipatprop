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

    def get_path(self, transmitting_angle: float, receiving_radius: float, max_reflections: int) -> dict | None:
        collision_points = []
        collision_segments = []
        collision_interferers = []

        points = [self.transmitter.position.copy()]
        transmitting_vector = Vector(cos(transmitting_angle), sin(transmitting_angle))
        vector = transmitting_vector
        ray = Ray(points[0], transmitting_vector)
        segment_ignore = None
        for r in range(max_reflections):
            close = False
            closest_point = None
            closest_segment = None
            closest_interferer = None
            for interferer in self.interferers:
                for s, segment in enumerate(interferer.segments):
                    if segment is segment_ignore:
                        continue
                    intersection = ray.intersect(segment)
                    if type(intersection) is Point:
                        point = intersection
                        # closest intersection is the point of reflection
                        if not close or ray.p1.distance(point) < ray.p1.distance(closest_point):
                            close = True
                            closest_point = point
                            closest_segment = segment
                            closest_interferer = interferer

            if not close:
                # case light goes away from all interferers
                return {
                    "path_points": points,
                    "collision_points": collision_points,
                    "collision_segments": collision_segments,
                    "collision_interferers": collision_interferers,
                    "exiting_angle": atan2(vector.y, vector.x)}
            points.append(closest_point)
            collision_points.append(closest_point)
            collision_segments.append(closest_segment)
            collision_interferers.append(closest_interferer)
            # calculate reflected ray
            normal = Vector(-closest_segment.v.y, closest_segment.v.x).normalized()
            vector = vector.reflect(normal)
            ray = Ray(closest_point, vector)
            segment_ignore = closest_segment
        # case light reaches the max_reflections limit
        return {
            "path_points": points,
            "collision_points": collision_points,
            "collision_segments": collision_segments,
            "collision_interferers": collision_interferers,
        }


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
    """An obstruction between the transmitter and receiver that reflects and fades incoming light."""
    points: list[Point]
    segments: list[Segment]

    def __init__(self, points: list[Point], closed=True) -> None:
        self.points = points
        self.segments = []
        if closed:
            points_closed = points + [points[0]]
        else:
            points_closed = points
        for point_1, point_2 in pairwise(points_closed):
            segment = Segment(point_1, point_2)
            self.segments.append(segment)
