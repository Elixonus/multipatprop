from __future__ import annotations
import cairo
from multipatprop import System, Transmitter, Receiver, Interferer, Point2D, Ray2D, Polygon

#system = mpp.System(mpp.Transmitter(Point(4, 3), 20), mpp.Receiver(Point(5, 8), 10), [mpp.Interferer([Point(6, 3), Point(7, 3), Point(4, 9)])])
system = System(Transmitter(Point2D(0, 0)), Receiver(Point2D(0, 0)), [Interferer(Point2D(0, 0), [Point2D(0, 0), Point2D(1, 0), Point2D(0, 1)])])
system.path(Ray2D(Point2D(-1, -1), Point2D(0, 0)))

minimum = Point(-3, -3)
maximum = Point(10, 10)

with cairo.ImageSurface(cairo.FORMAT_RGB24, 500, 500) as surface:
    context = cairo.Context(surface)
    context.translate(-minimum.x, -minimum.y)
    context.scale(*(1 / (maximum - minimum)))
    context.scale(500, 500)

    context.arc(*system.transmitter.point, 0.1, 0, 6)
    context.set_source_rgb(1, 0, 0)
    context.fill()

    context.arc(*system.receiver.point, 0.1, 0, 6)
    context.set_source_rgb(0, 0, 1)
    context.fill()

    for interferer in system.interferers:
        for point in interferer.points:
            context.line_to(*point)
        context.close_path()
        context.set_source_rgb(0, 1, 0)
        context.set_line_width(0.05)
        context.stroke()

    surface.write_to_png("test.png")