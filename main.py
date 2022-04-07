from __future__ import annotations
from math import tau
import cairo
from multipatprop import System, Transmitter, Receiver, Interferer, Point2D, Ray2D, Polygon

transmitter = Transmitter(Point2D(1, 1))
receiver = Receiver(Point2D(9, 8))
interferers = [Interferer(Polygon(Point2D(5, 5), Point2D(2, 5), Point2D(5, 3)))]

system = System(transmitter, receiver, interferers)
system.get_path(Ray2D(Point2D(-1, -1), Point2D(0, 0)))

camera_position = Point2D(5, 5)
camera_zoom = 0.1

with cairo.ImageSurface(cairo.FORMAT_RGB24, 500, 500) as surface:
    context = cairo.Context(surface)
    context.scale(500, 500)
    context.translate(0.5, 0.5)
    context.scale(1, -1)
    context.scale(camera_zoom, camera_zoom)
    context.translate(-camera_position.x, -camera_position.y)

    context.arc(system.transmitter.point.x, system.transmitter.point.y, 0.2, 0, tau)
    context.set_source_rgb(1, 0, 0)
    context.fill()

    context.arc(system.receiver.position.x, system.receiver.position.y, 0.2, 0, tau)
    context.set_source_rgb(0, 0, 1)
    context.fill()

    for interferer in system.interferers:
        for vertex in interferer.polygon.vertices:
            context.line_to(vertex.x, vertex.y)
        context.close_path()
        context.set_source_rgb(0, 1, 0)
        context.set_line_width(0.05)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.stroke()

    surface.write_to_png("render.png")