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
    number: int

    def __init__(self, point: Point, number: int) -> None:
        self.point = point
        self.number = number


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


class Absorber(Interferer):
    def __init__(self, point: Point, points: Iterable[Point]) -> None:
        super().__init__(point, points)


class Reflector(Interferer):
    def __init__(self, point: Point, points: Iterable[Point]) -> None:
        super().__init__(point, points)
