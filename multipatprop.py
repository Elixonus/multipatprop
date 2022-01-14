from __future__ import annotations
from points import Point


class System:
    transmitter: Transmitter
    receiver: Receiver
    interferers: list[Interferer]

    def __init__(self, transmitter: Transmitter, receiver: Receiver, interferers: list[Interferer]) -> None:
        self.transmitter = transmitter
        self.receiver = receiver
        self.interferers = interferers

    def path(self):
        for i in range(1):
            for interferer in self.interferers:
                points = interferer.points

                for point_1, point_2 in zip(points, points[1:] + points[:1]):
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


class Interferer:
    points: list[Point]

    def __init__(self, points: list[Point]) -> None:
        self.points = points

    def stuff(self, endpoint: Point, point: Point):
        ray: Point = point - endpoint

        for point_1, point_2 in zip(self.points, self.points[1:] + self.points[:1]):
            segment = point_2 - point_1



class Absorber(Interferer):
    def __init__(self, points: list[Point]) -> None:
        super().__init__(points)


class Reflector(Interferer):
    def __init__(self, points: list[Point]) -> None:
        super().__init__(points)
