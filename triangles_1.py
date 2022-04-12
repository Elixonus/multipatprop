from __future__ import annotations
from math import pi, tau, cos, sin, sqrt
from random import seed, random
from multipatprop import System, Transmitter, Receiver, Interferer, Point, DigitalSignal
from render import render

seed(5)

transmitter = Transmitter(Point(-3.3, -2))
receiver = Receiver(Point(1.5, 1.5))
interferers = [Interferer.square(Point(0, 0), 9, 0)]

for n in range(30):
    theta = tau * random()
    radius = 3 * sqrt(sqrt(random()))
    interferer = Interferer.polygon(Point(radius * cos(theta), radius * sin(theta)), diameter=0.5, number_sides=3, rotation=tau * random())
    interferers.append(interferer)

system = System(transmitter, receiver, interferers)
multipath = system.get_multipath(starting_number=1000, receiver_diameter=0.1, max_reflections=10)
camera_position = Point(0, 0)
camera_zoom = 0.1
render(system, multipath, camera_position, camera_zoom, ui_size=1, bins=15, red_factor=10)
