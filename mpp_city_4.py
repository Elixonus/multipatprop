from math import pi, tau, cos, sin
from random import seed, random
from multipatprop import System, Transmitter, Receiver, Interferer, Point
from output import render

seed(114230)


transmitter = Transmitter(Point(-3.5, -3.5))
receiver = Receiver(Point(3.5, 3.5))
interferers = [Interferer.square(Point(0, 0), 9, 0)]


for r in range(3):
    for a in range(10):
        radius = 2 + r
        angle = ((a + random() / 4) / 10) * tau
        interferer = Interferer.rectangle(position=Point(radius * cos(angle), radius * sin(angle)), length=0.7, width=0.5, rotation=angle + pi / 2)
        interferers.append(interferer)

system = System(transmitter, receiver, interferers)
multipath = system.get_multipath(starting_number=1000, receiver_diameter=0.2, max_reflections=30, power_multiplier=0.9)
camera_position = Point(0, 0)
camera_zoom = 0.1
render(system, multipath, camera_position, camera_zoom, ui_size=1, bins=30, red_factor=1)
