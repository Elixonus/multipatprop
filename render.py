from math import tau
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
            context.set_source_rgba(0, 1, 0, path.attenuation)
            context.set_line_width(0.02 * ui_size)
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

    delays = [path.delay for path in multipath]
    attenuations = [path.attenuation for path in multipath]
    degrees = 10
    coefficients = np.polyfit(delays, attenuations, deg=degrees)
    x = np.linspace(min(delays), max(delays), 100)
    y = np.zeros(100)
    for a in range(100):
        for d in range(degrees + 1):
            y[a] += coefficients[-d - 1] * x[a] ** d

    fig, ax = plt.subplots()
    ax.scatter(delays, attenuations)
    ax.plot(x, y)
    ax.set_title("Delay and attenuation of multiple propagating wave paths")
    ax.set_xlabel("Delay (seconds)")
    ax.set_ylabel("Attenuation factor")
    plt.show()