from __future__ import annotations
from math import tau, pi
from random import random
import cairo
from multipatprop import System, Transmitter, Receiver, Interferer, Point


transmitter = Transmitter(Point(4, 3))
receiver = Receiver(Point(6, 6))
interferers = [Interferer([Point(7, 3), Point(8, 5), Point(5, 2)]),
               Interferer([Point(2, 4), Point(4, 7), Point(4, 8)]),
               Interferer.circle(Point(3, 5), 0.5, 100)]

system = System(transmitter, receiver, interferers)
paths = system.get_multipath(starting_number=50, receiver_diameter=0.1, max_reflections=30)

camera_position = Point(5, 5)
camera_zoom = 0.1


svg = cairo.SVGSurface("example.svg", 200, 200)


with cairo.ImageSurface(cairo.FORMAT_RGB24, 1000, 1000) as surface:
    context = cairo.Context(surface)
    context.scale(1000, 1000)

    context.set_source_rgb(0, 0, 0)
    context.rectangle(0, 0, 1, 1)
    context.fill()



    context.translate(0.5, 0.5)
    context.scale(1, -1)
    context.scale(camera_zoom, camera_zoom)
    context.translate(-camera_position.x, -camera_position.y)



    for path in paths:
        for point in path:
            context.line_to(point.x, point.y)
        context.set_source_rgb(0, 1, 0)
        context.set_line_width(0.02)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.stroke()

    for interferer in system.interferers:
        for point in interferer.points:
            context.line_to(point.x, point.y)
        context.close_path()
        context.set_source_rgb(0, 0, 0)
        context.fill_preserve()
        context.set_source_rgb(1, 1, 1)
        context.set_line_width(0.05)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.stroke()

    context.arc(system.transmitter.position.x, system.transmitter.position.y, 0.4, 0, tau)
    context.set_source_rgb(1, 0, 0)
    context.fill_preserve()
    context.set_source_rgb(1, 1, 1)
    context.set_line_width(0.05)
    context.set_line_join(cairo.LINE_JOIN_ROUND)
    context.set_line_cap(cairo.LINE_CAP_ROUND)
    context.stroke()

    context.arc(system.receiver.position.x, system.receiver.position.y, 0.4, 0, tau)
    context.set_source_rgb(0, 0, 1)
    context.fill_preserve()
    context.set_source_rgb(1, 1, 1)
    context.set_line_width(0.05)
    context.set_line_join(cairo.LINE_JOIN_ROUND)
    context.set_line_cap(cairo.LINE_CAP_ROUND)
    context.stroke()

    surface.write_to_png("render.png")