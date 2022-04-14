import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from math import pi
from random import seed, random, randint
from multipatprop import System, Transmitter, Receiver, Interferer, Point
from output import render

seed(11230)


transmitter = Transmitter(Point(-2, -2.5))
receiver = Receiver(Point(2, 2))
interferers = [Interferer.square(Point(0, 0), 9, 0)]


for x in range(8):
    for y in range(8):
        if ((x-4)**2 + (y-4)**2)**0.5 > 4:
            continue
        interferer = Interferer.rectangle(position=Point(x - 3.5 + random() / 4, y - 3.5 + random() / 4), length=0.3 + random() / 4, width=0.25, rotation=pi / 2 * randint(0, 100))
        interferers.append(interferer)



system = System(transmitter, receiver, interferers)
multipath = system.get_multipath(starting_number=1000, receiver_diameter=0.2, max_reflections=30, power_multiplier=0.9)
camera_position = Point(0, 0)
camera_zoom = 0.1
render(system, multipath, camera_position, camera_zoom, ui_size=1, bins=30, red_factor=1)
