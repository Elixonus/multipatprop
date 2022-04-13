from math import tau, atan2
from itertools import pairwise
import cairo
import matplotlib.pyplot as plt
import numpy as np
from skimage.draw import line, line_aa
from multipatprop import System, Multipath, Point, Segment


def render(system: System, multipath: Multipath, camera_position: Point, camera_zoom: float, ui_size: float, bins: int, red_factor: float) -> None:
    for interferer in system.interferers:
        interferer.hits = 0
    for path in multipath:
        for hit in path.hits:
            hit.hits += 1

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
            context.set_source_rgba(0, 1, 0, path.power)
            context.set_line_width(0.02 * ui_size)
            context.set_line_join(cairo.LINE_JOIN_ROUND)
            context.set_line_cap(cairo.LINE_CAP_ROUND)
            context.stroke()

        for interferer in system.interferers:
            for point in interferer.points:
                context.line_to(point.x, point.y)
            context.close_path()
            context.set_source_rgb(1, max(1 - interferer.hits / 100 * red_factor, 0), max(1 - interferer.hits / 100 * red_factor, 0))
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
    ax.hist([path.delay for path in multipath], weights=[path.power for path in multipath], bins=bins, rwidth=0.9)
    ax.set_xlabel("Time")
    ax.set_ylabel("Signal Energy")
    ax.set_title("Energy function of propagated waves")

    """
    camera_minimum = Point(camera_position.x - 0.5 / camera_zoom, camera_position.y - 0.5 / camera_zoom)
    camera_maximum = Point(camera_position.x + 0.5 / camera_zoom, camera_position.y + 0.5 / camera_zoom)
    densities = np.zeros((100, 100))
    for ix, x in enumerate(np.linspace(camera_minimum.x, camera_maximum.x, 100)):
        for iy, y in enumerate(np.linspace(camera_minimum.y, camera_maximum.y, 100)):
            density = 0
            for path in multipath:
                for point_1, point_2 in pairwise(path):
                    segment = Segment(point_1, point_2)
                    density += path.power / Point(x, y).distance(segment)
            densities[iy][ix] = density
    densities_flat = densities.flatten()
    density_low = np.percentile(densities_flat, 5)
    density_high = np.percentile(densities_flat, 95)
    fig, ax = plt.subplots()
    ax.imshow(densities, vmin=density_low, vmax=density_high, origin="lower", cmap="inferno")
    plt.show()
    """

    camera_minimum = Point(camera_position.x - 0.5 / camera_zoom, camera_position.y - 0.5 / camera_zoom)
    camera_maximum = Point(camera_position.x + 0.5 / camera_zoom, camera_position.y + 0.5 / camera_zoom)

    def r_transform(point: Point) -> tuple[int, int]:
        return (round(49 * (point.y - camera_minimum.y) / (camera_maximum.y - camera_minimum.y)),
                round(49 * (point.x - camera_minimum.x) / (camera_maximum.x - camera_minimum.x)))

    image = np.zeros((50, 50))
    for path in multipath:
        for point_1, point_2 in pairwise(path):
            r1, c1 = r_transform(point_1)
            r2, c2 = r_transform(point_2)
            rr, cc, val = line_aa(r1, c1, r2, c2)
            image[rr, cc] += val
    image_flat = image.flatten()
    image_low = np.percentile(image_flat, 10)
    image_high = np.percentile(image_flat, 90)

    fig, ax = plt.subplots()
    ax.imshow(image, vmin=image_low, vmax=image_high, origin="lower", cmap="inferno")
    plt.show()