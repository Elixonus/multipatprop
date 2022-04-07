from __future__ import annotations
from math import atan2, pi
from sympy import Point2D, Ray2D, Polygon


class System:
    transmitter: Transmitter
    receiver: Receiver
    interferers: list[Interferer]

    def __init__(self, transmitter: Transmitter, receiver: Receiver, interferers: list[Interferer]) -> None:
        self.transmitter = transmitter
        self.receiver = receiver
        self.interferers = interferers

    def get_path(self, angle: float, max_reflections) -> list[Ray2D]:
        ray = Ray2D(self.transmitter.position, angle=angle)
        closest = False
        closest_point = None
        closest_side: Ray2D = None
        for interferer in self.interferers:
            for side in interferer.polygon.sides:
                intersections = ray.intersection(side)
                if len(intersections) > 0:
                    point = intersections[0]
                    if not closest or ray.p1.distance(point) < ray.p1.distance(closest_point):
                        closest = True
                        closest_point = point
                        closest_side = side
        if not closest:
            return

        angle_incidence = angle
        angle_reflection = 2 * atan2(closest_side.direction.y, closest_side.direction.x) - angle_incidence
        print(angle_incidence * 180 / pi, angle_reflection * 180 / pi)






class Transmitter:
    position: Point2D

    def __init__(self, position: Point2D) -> None:
        self.position = position


class Receiver:
    position: Point2D

    def __init__(self, position: Point2D) -> None:
        self.position = position


class Interferer:
    polygon: Polygon

    def __init__(self, polygon: Polygon) -> None:
        self.polygon = polygon




class Absorber(Interferer):
    def __init__(self, position: Point2D, polygon: Polygon) -> None:
        super().__init__(position, polygon)


class Reflector(Interferer):
    def __init__(self, position: Point2D, polygon: Polygon) -> None:
        super().__init__(position, polygon)
