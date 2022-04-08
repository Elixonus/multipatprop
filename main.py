from __future__ import annotations
from math import cos, sin, tau
import cairo
from multipatprop import System, Transmitter, Receiver, Interferer, Vector, Point, Ray, Segment, Circle


transmitter = Transmitter(Point(4, 3))
receiver = Receiver(Point(6, 6))
interferers = [Interferer([Point(7, 2), Point(8, 5), Point(5, 2)]),
               Interferer([Point(1, 4), Point(4, 7), Point(4, 8)])]

system = System(transmitter, receiver, interferers)
paths = system.get_paths(starting_number=50, max_reflections=30)
paths_propagated = system.get_paths_propagated(starting_number=1000, receiver_diameter=0.1, max_reflections=30)

camera_position = Point(5, 5)
camera_zoom = 0.1

p = system.get_path(Vector(1, 0), max_reflections=10)
print(p)

with cairo.ImageSurface(cairo.FORMAT_RGB24, 1000, 1000) as surface:
    context = cairo.Context(surface)
    context.scale(1000, 1000)
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

    for path in paths:
        for point in path[0]:
            context.line_to(point.x, point.y)
        if path[1] is not None:
            normalized = path[1].normalized()
            context.rel_line_to(100 * normalized.x, 100 * normalized.y)
        context.set_source_rgb(0.3, 0.3, 0.3)
        context.set_line_width(0.02)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.stroke()

    for path_propagated in paths_propagated:
        for point in path_propagated[0]:
            context.line_to(point.x, point.y)
        context.line_to(system.receiver.position.x, system.receiver.position.y)
        context.set_source_rgb(1, 1, 1)
        context.set_line_width(0.02)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.stroke()

    context.arc(system.transmitter.position.x, system.transmitter.position.y, 0.4, 0, tau)
    context.set_source_rgb(1, 0, 0)
    context.fill()

    context.arc(system.receiver.position.x, system.receiver.position.y, 0.4, 0, tau)
    context.set_source_rgb(0, 0, 1)
    context.fill()

    surface.write_to_png("render.png")