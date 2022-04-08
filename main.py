from __future__ import annotations
from math import cos, sin, tau
import cairo
from multipatprop import System, Transmitter, Receiver, Interferer, Vector, Point, Ray, Segment, Circle


transmitter = Transmitter(Point(3, 3))
receiver = Receiver(Point(9, 8))
interferers = [Interferer([Point(7, 2), Point(8, 5), Point(5, 2)])]

system = System(transmitter, receiver, interferers)
#paths = system.get_paths(starting_number=100, max_reflections=10)
#paths_propagated = system.get_paths_propagated(starting_number=100, receiver_diameter=1.6, max_reflections=10)

camera_position = Point(5, 5)
camera_zoom = 0.1

print(system.get_path(Vector(1, 0), max_reflections=10))

with cairo.ImageSurface(cairo.FORMAT_RGB24, 500, 500) as surface:
    context = cairo.Context(surface)
    context.scale(500, 500)
    context.translate(0.5, 0.5)
    context.scale(1, -1)
    context.scale(camera_zoom, camera_zoom)
    context.translate(-camera_position.x, -camera_position.y)

    for interferer in system.interferers:
        for point in interferer.points:
            context.line_to(point.x, point.y)
        context.close_path()
        context.set_source_rgb(0, 1, 0)
        context.set_line_width(0.05)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.stroke()
    """
    for path in paths:
        for point in path[0]:
            context.line_to(point.x, point.y)
        if path[1] is not None:
            context.rel_line_to(100 * cos(path[1]), 100 * sin(path[1]))
        context.set_source_rgb(0.3, 0.3, 0.3)
        context.set_line_width(0.02)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.stroke()

    for path_propagated in paths_propagated:
        for point in path_propagated:
            context.line_to(point.x, point.y)
        context.set_source_rgb(1, 1, 1)
        context.set_line_width(0.02)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.stroke()
    """

    context.arc(system.transmitter.position.x, system.transmitter.position.y, 0.4, 0, tau)
    context.set_source_rgb(1, 0, 0)
    context.fill()

    context.arc(system.receiver.position.x, system.receiver.position.y, 0.8, 0, tau)
    context.set_source_rgb(0, 0, 1)
    context.fill()

    surface.write_to_png("render.png")