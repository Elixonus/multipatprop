from __future__ import annotations
from math import pi, tau
from random import random, seed
import cairo
import numpy as np
import matplotlib.pyplot as plt
from multipatprop import System, Transmitter, Receiver, Interferer, Point, DigitalSignal

seed(2)

transmitter = Transmitter(Point(-2.5, -2))
receiver = Receiver(Point(-1.5, -1.5))
interferers = []

for x in range(-4, 4):
    for y in range(-4, 4):
        interferer = Interferer.square(position=Point(x, y), length=0.3 + random() / 4, rotation=tau * random())
        interferers.append(interferer)

system = System(transmitter, receiver, interferers)
multipath = system.get_multipath(starting_number=1000, receiver_diameter=0.1, max_reflections=10)

camera_position = Point(0, 0)
camera_zoom = 0.1



from render import render
render(system, multipath, camera_position, camera_zoom, ui_size=1)
