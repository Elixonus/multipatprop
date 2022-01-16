from __future__ import annotations
from collections.abc import Iterable
from points import Point, Line, Polygon


class System:
    transmitter: Transmitter
    receiver: Receiver
    interferers: list[Interferer]

    def __init__(self, transmitter: Transmitter, receiver: Receiver, interferers: list[Interferer]) -> None:
        self.transmitter = transmitter
        self.receiver = receiver
        self.interferers = interferers

    def path(self):
        pass





class Transmitter:
    point: Point
    transmissions: int

    def __init__(self, point: Point, transmissions: int) -> None:
        self.point = point
        self.transmissions = transmissions


class Receiver:
    point: Point
    distance: float

    def __init__(self, point: Point, distance: float) -> None:
        self.point = point
        self.distance = distance


class Interferer(Polygon):
    point: Point

    def __init__(self, point: Point, points: Iterable[Point]) -> None:
        super().__init__(points)
        self.point = point

    def interfere(self, transmission: Line):
        for line in self.lines:
            v1 = transmission.point_1 - line.point_1
            v2 = line.vec()





class Absorber(Interferer):
    def __init__(self, point: Point, points: Iterable[Point]) -> None:
        super().__init__(point, points)


class Reflector(Interferer):
    def __init__(self, point: Point, points: Iterable[Point]) -> None:
        super().__init__(point, points)
