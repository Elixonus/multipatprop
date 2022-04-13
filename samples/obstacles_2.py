from __future__ import annotations
from math import pi
from random import seed
from multipatprop import System, Transmitter, Receiver, Interferer, Point, DigitalSignal
from render import render

seed(1)

transmitter = Transmitter(Point(-3.3, -2))
receiver = Receiver(Point(1.5, 1.5))
interferers = [Interferer.square(Point(0, 0), 9, 0),
               Interferer.polygon(Point(0, 0), diameter=4, number_sides=7, rotation=0),
               Interferer.rectangle(Point(-3, 2), length=2, width=0.5, rotation=-pi / 4),
               Interferer.rectangle(Point(3, -2), length=2, width=0.5, rotation=-pi / 4)]
system = System(transmitter, receiver, interferers)
multipath = system.get_multipath(starting_number=1000, receiver_diameter=0.1, max_reflections=30)
camera_position = Point(0, 0)
camera_zoom = 0.1
render(system, multipath, camera_position, camera_zoom, ui_size=1, bins=15, red_factor=0.3)
