from math import tau, atan2
import cairo
import matplotlib.pyplot as plt
import numpy as np
from multipatprop import System, Multipath, Point


def render(system: System, multipath: Multipath, camera_position: Point, camera_zoom: float, ui_size: float) -> None:
    with cairo.ImageSurface(cairo.FORMAT_RGB24, 1000, 1000) as surface:
        context = cairo.Context(surface)
        context.scale(1000, 1000)
        context.fill()
        context.translate(0.5, 0.5)
        context.scale(1, -1)
        context.scale(camera_zoom, camera_zoom)
        context.translate(-camera_position.x, -camera_position.y)

        for path in multipath:
            for point in path:
                context.line_to(point.x, point.y)
            context.set_source_rgba(0, 1, 0, 1 - path.power)
            context.set_line_width(0.01 * ui_size)
            context.set_line_join(cairo.LINE_JOIN_ROUND)
            context.set_line_cap(cairo.LINE_CAP_ROUND)
            context.stroke()

        for interferer in system.interferers:
            for point in interferer.points:
                context.line_to(point.x, point.y)
            context.close_path()
            context.set_source_rgb(1, 1, 1)
            context.set_line_width(0.05 * ui_size)
            context.set_line_join(cairo.LINE_JOIN_ROUND)
            context.set_line_cap(cairo.LINE_CAP_ROUND)
            context.stroke()

        context.arc(system.transmitter.position.x, system.transmitter.position.y, 0.1, 0, tau)
        context.set_source_rgb(1, 0, 0)
        context.fill_preserve()
        context.set_source_rgb(1, 1, 1)
        context.set_line_width(0.05 * ui_size)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.stroke()

        context.arc(system.receiver.position.x, system.receiver.position.y, 0.1, 0, tau)
        context.set_source_rgb(0, 0, 1)
        context.fill_preserve()
        context.set_source_rgb(1, 1, 1)
        context.set_line_width(0.05 * ui_size)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.stroke()

        surface.write_to_png("render.png")



    fig, ax = plt.subplots()
    ax.hist([path.delay for path in multipath], weights=[path.power for path in multipath], bins=20)
    plt.show()
