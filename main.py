from __future__ import annotations
from math import pi, tau
from random import random, seed
import cairo
from multipatprop import System, Transmitter, Receiver, Interferer, Point

seed(1)

transmitter = Transmitter(Point(-2.5, -2.5))
receiver = Receiver(Point(1.5, 0.5))
interferers = []

for x in range(-4, 4):
    for y in range(-4, 4):
        interferer = Interferer.square(position=Point(x, y), length=0.3 + random() / 4, rotation=tau * random())
        interferers.append(interferer)

system = System(transmitter, receiver, interferers)
multipath = system.get_multipath(starting_number=1000, receiver_diameter=0.01, max_reflections=10)

camera_position = Point(0, 0)
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

    for path in multipath:
        for point in path:
            context.line_to(point.x, point.y)
        context.set_source_rgba(0, 1, 0)
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

    context.arc(system.transmitter.position.x, system.transmitter.position.y, 0.1, 0, tau)
    context.set_source_rgb(1, 0, 0)
    context.fill_preserve()
    context.set_source_rgb(1, 1, 1)
    context.set_line_width(0.05)
    context.set_line_join(cairo.LINE_JOIN_ROUND)
    context.set_line_cap(cairo.LINE_CAP_ROUND)
    context.stroke()

    context.arc(system.receiver.position.x, system.receiver.position.y, 0.1, 0, tau)
    context.set_source_rgb(0, 0, 1)
    context.fill_preserve()
    context.set_source_rgb(1, 1, 1)
    context.set_line_width(0.05)
    context.set_line_join(cairo.LINE_JOIN_ROUND)
    context.set_line_cap(cairo.LINE_CAP_ROUND)
    context.stroke()

    surface.write_to_png("render.png")