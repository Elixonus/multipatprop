from __future__ import annotations
from collections.abc import Iterable
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
    center: Point2D

    def __init__(self, point: Point2D) -> None:
        self.point = point


class Receiver:
    center: Point2D

    def __init__(self, point: Point2D) -> None:
        self.point = point


class Interferer:
    center: Point2D
    polygon: Polygon

    def __init__(self, center: Point2D, points: Iterable[Point2D]) -> None:
        self.polygon = Polygon(*points)




class Absorber(Interferer):
    def __init__(self, point: Point, points: Iterable[Point]) -> None:
        super().__init__(point, points)


class Reflector(Interferer):
    def __init__(self, point: Point, points: Iterable[Point]) -> None:
        super().__init__(point, points)
