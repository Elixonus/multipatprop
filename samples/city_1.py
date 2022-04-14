from __future__ import annotations
from math import pi
from random import seed, random, randint
from copy import deepcopy
from multipatprop import System, Transmitter, Receiver, Interferer, Point, DigitalSignal
from output import render

seed(1123)


transmitter = Transmitter(Point(-2, -2.5))
receiver = Receiver(Point(2, 2))
interferers = [Interferer.square(Point(0, 0), 9, 0)]


for x in range(8):
    for y in range(8):
        interferer = Interferer.rectangle(position=Point(x - 3.5 + random() / 4, y - 3.5 + random() / 4), length=0.3 + random() / 4, width=0.25, rotation=pi / 2 * randint(0, 100))
        interferers.append(interferer)



system = System(transmitter, receiver, interferers)
multipath = system.get_multipath(starting_number=1000, receiver_diameter=0.2, max_reflections=40, power_multiplier=0.95)
camera_position = Point(0, 0)
camera_zoom = 0.1
render(system, multipath, camera_position, camera_zoom, ui_size=1, bins=30, red_factor=1)
