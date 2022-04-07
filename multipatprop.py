from __future__ import annotations
from math import pi, tau, atan2
from sympy import Point2D, Ray2D, Polygon


class System:
    transmitter: Transmitter
    receiver: Receiver
    interferers: list[Interferer]

    def __init__(self, transmitter: Transmitter, receiver: Receiver, interferers: list[Interferer]) -> None:
        self.transmitter = transmitter
        self.receiver = receiver
        self.interferers = interferers

    def get_paths(self, starting_number: int, max_reflections: int) -> list[tuple[list[Point2D], float | None]]:
        paths = [self.get_path(tau * (n / starting_number), max_reflections) for n in range(starting_number)]
        return paths

    def get_path(self, starting_angle: float, max_reflections: int) -> tuple[list[Point2D], float | None]:
        path = [self.transmitter.position.copy()]
        ray = Ray2D(path[0], angle=starting_angle)
        angle = starting_angle
        side_ignore = None
        for r in range(max_reflections):
            closest = False
            closest_point = None
            closest_side = None
            for interferer in self.interferers:
                for side in interferer.polygon.sides:
                    if side == side_ignore:
                        continue
                    intersections = ray.intersection(side)
                    if len(intersections) > 0:
                        point = intersections[0]
                        if not closest or ray.p1.distance(point) < ray.p1.distance(closest_point):
                            closest = True
                            closest_point = point
                            closest_side = side
            if not closest:
                return path, angle

            path.append(closest_point)
            angle = 2 * atan2(closest_side.direction.y, closest_side.direction.x) - angle
            ray = Ray2D(closest_point, angle=angle)
            side_ignore = closest_side
        return path, None





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
