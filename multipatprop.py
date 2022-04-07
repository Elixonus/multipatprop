from __future__ import annotations
from sympy import Point2D, Ray2D, Polygon


class System:
    transmitter: Transmitter
    receiver: Receiver
    interferers: list[Interferer]

    def __init__(self, transmitter: Transmitter, receiver: Receiver, interferers: list[Interferer]) -> None:
        self.transmitter = transmitter
        self.receiver = receiver
        self.interferers = interferers

    def get_path(self, ray: Ray2D):
        closest = False
        closest_point = None
        closest_side = None
        closest_interferer = None
        for interferer in self.interferers:
            for side in interferer.polygon.sides:
                intersections = ray.intersection(side)
                if len(intersections) > 0:
                    point = intersections[0]
                    if not closest or ray.p1.distance(point) < ray.p1.distance(closest_point):
                        closest_point = point
                        closest_side = side
                        closest_interferer = interferer
        print(closest_side)






class Transmitter:
    position: Point2D

    def __init__(self, position: Point2D) -> None:
        self.point = position


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
