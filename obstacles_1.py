from __future__ import annotations
from math import pi, tau
from random import random, seed
from multipatprop import System, Transmitter, Receiver, Interferer, Point, DigitalSignal
from render import render

seed(1)

transmitter = Transmitter(Point(-3.5, -3))
receiver = Receiver(Point(1.5, 1.5))
interferers = [Interferer.square(Point(-2, 2), 2, pi/16),
               Interferer.square(Point(0, 0), 9, 0),
               Interferer.rectangle(Point(0, 0), 2, 0.3, rotation=3*pi/4),
               Interferer.polygon(Point(0, 3), diameter=1, number_sides=3, rotation=0),
               Interferer.polygon(Point(-1, -3), diameter=1, number_sides=5, rotation=0),
               Interferer.polygon(Point(3, -1), diameter=2, number_sides=6, rotation=0)]
system = System(transmitter, receiver, interferers)
multipath = system.get_multipath(starting_number=1000, receiver_diameter=0.1, max_reflections=10)
camera_position = Point(0, 0)
camera_zoom = 0.1
render(system, multipath, camera_position, camera_zoom, ui_size=1)
