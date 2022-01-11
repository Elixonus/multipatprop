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


class Transmitter:
    point: Point

    def __init__(self, point: Point) -> None:
        self.point = point


class Receiver:
    point: Point

    def __init__(self, point: Point) -> None:
        self.point = point


class Interferer:
    points: list[Point]

    def __init__(self, points: list[Point]) -> None:
        self.points = points


class Absorber(Interferer):
    def __init__(self, points: list[Point]) -> None:
        super(points)


class Reflector(Interferer):
    def __init__(self, vertices: list[Point]):


sys = System(None, None, [Absorber([Point(4, 3)])])