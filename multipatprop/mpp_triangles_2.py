from math import tau
from random import seed, random
from multipatprop import System, Transmitter, Receiver, Interferer, Point
from output import render

seed(2451)

transmitter = Transmitter(Point(-3.3, -2))
receiver = Receiver(Point(1.5, 1.5))
interferers = [Interferer.square(Point(0, 0), 9, 0)]

for x in range(5):
    for y in range(7):
        position = Point(x - 5 / 2 + random() / 2, y - 7 / 2 + random() / 2)
        interferer = Interferer.polygon(
            position, diameter=0.4, number_sides=3, rotation=tau * random()
        )
        interferers.append(interferer)

system = System(transmitter, receiver, interferers)
multipath = system.get_multipath(
    starting_number=500, receiver_diameter=0.1, max_reflections=50
)
camera_position = Point(0, 0)
camera_zoom = 0.1
render(
    system, multipath, camera_position, camera_zoom, ui_size=1, bins=15, red_factor=2
)
