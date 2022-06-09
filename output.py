from math import tau
from itertools import pairwise
from time import sleep
import cairo
import matplotlib.pyplot as plt
import numpy as np
from skimage.draw import line
from multipatprop import System, Multipath, Point


def render(system: System, multipath: Multipath, camera_position: Point, camera_zoom: float, ui_size: float, bins: int, red_factor: float) -> None:
    for interferer in system.interferers:
        interferer.hits = 0
    for path in multipath:
        for hit in path.hits:
            hit.hits += 1

    # create the rendered visualization of paths, and system
    with cairo.ImageSurface(cairo.FORMAT_RGB24, 1000, 1000) as surface:
        print("Rendering paths...")
        # perform initial transformations
        context = cairo.Context(surface)
        context.scale(1000, 1000)
        context.fill()
        context.translate(0.5, 0.5)
        context.scale(1, -1)
        context.scale(camera_zoom, camera_zoom)
        context.translate(-camera_position.x, -camera_position.y)

        # render each propagated path
        for path in multipath:
            for point in path:
                context.line_to(point.x, point.y)
            context.set_source_rgba(0, 1, 0, path.power)
            context.set_line_width(0.02 * ui_size)
            context.set_line_join(cairo.LINE_JOIN_ROUND)
            context.set_line_cap(cairo.LINE_CAP_ROUND)
            context.stroke()

        # render interferers
        for interferer in system.interferers:
            for point in interferer.points:
                context.line_to(point.x, point.y)
            context.close_path()
            context.set_source_rgb(1, max(1 - interferer.hits / 100 * red_factor, 0), max(1 - interferer.hits / 100 * red_factor, 0))
            context.set_line_width(0.05 * ui_size)
            context.set_line_join(cairo.LINE_JOIN_ROUND)
            context.set_line_cap(cairo.LINE_CAP_ROUND)
            context.stroke()

        # render transmitter
        context.arc(system.transmitter.position.x, system.transmitter.position.y, 0.1, 0, tau)
        context.set_source_rgb(1, 0, 0)
        context.fill_preserve()
        context.set_source_rgb(1, 1, 1)
        context.set_line_width(0.05 * ui_size)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.stroke()

        # render receiver
        context.arc(system.receiver.position.x, system.receiver.position.y, 0.1, 0, tau)
        context.set_source_rgb(0, 0, 1)
        context.fill_preserve()
        context.set_source_rgb(1, 1, 1)
        context.set_line_width(0.05 * ui_size)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.stroke()

        # convert pycairo image to pixel data and later load it in matplotlib
        raw = surface.get_data().tolist()
        counter = 0
        image = np.empty((1000, 1000, 3), dtype=np.uint8)
        for x in range(1000):
            for y in range(1000):
                for c in range(3):
                    image[x][y][2 - c] = raw[counter]
                    counter += 1
                counter += 1

    print("Making path density visualization...")
    # using minimum and maximum viewport coordinates to reverse transform coordinates
    camera_minimum = Point(camera_position.x - 0.5 / camera_zoom, camera_position.y - 0.5 / camera_zoom)
    camera_maximum = Point(camera_position.x + 0.5 / camera_zoom, camera_position.y + 0.5 / camera_zoom)

    def r_transform(p: Point) -> tuple[int, int]:
        return (round((100 - 1) * (p.y - camera_minimum.y) / (camera_maximum.y - camera_minimum.y)),
                round((100 - 1) * (p.x - camera_minimum.x) / (camera_maximum.x - camera_minimum.x)))

    # calculating density by drawing rasterized lines virtually with scipy
    density = np.zeros((100, 100))
    for path in multipath:
        for point_1, point_2 in pairwise(path):
            r1, c1 = r_transform(point_1)
            r2, c2 = r_transform(point_2)
            rr, cc = line(r1, c1, r2, c2)
            density[rr, cc] += path.power
    density_flat = density.flatten()
    density_low = np.percentile(density_flat, 5)
    density_high = np.percentile(density_flat, 95)

    # rendering density map
    fig, ax = plt.subplots()
    im = ax.imshow(density, vmin=density_low, vmax=density_high, origin="lower", cmap="inferno", interpolation="gaussian")
    plt.colorbar(im)
    ax.set_title("Relative density of propagated paths")

    # rendering energy time function
    fig, ax = plt.subplots()
    ax.hist([path.delay for path in multipath], weights=[path.power for path in multipath], bins=bins, rwidth=0.95)
    ax.set_xlabel("Time")
    ax.set_ylabel("Relative Signal Energy Rate")
    ax.set_title("Energy function of propagated waves")

    # rendering visualization of system
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.set_title("Propagated paths from transmitter to receiver")













    print("Done, displaying results...\n")
    sleep(1)
    print(f"Total number of paths: {multipath.starting_number}")
    print(f"Number of propagated paths: {len(multipath.paths)}")
    print(f"Propagation rate: {100 * (len(multipath.paths) / multipath.starting_number):.2f}%")
    if len(multipath.paths) > 0:
        print(f"Shortest path time: {min(path.delay for path in multipath)} seconds")
        print(f"Longest path time: {max(path.delay for path in multipath)} seconds")
    plt.show()


if __name__ == "__main__":
    print("This file is a utility program that does not work on its own.")
    sleep(5)
