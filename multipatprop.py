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

    def path(self, ray: Ray2D):
        for interferer in self.interferers:
            print(interferer.polygon.intersect(ray))





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
