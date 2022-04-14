import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from math import pi
from random import seed
from multipatprop import System, Transmitter, Receiver, Interferer, Point
from output import render

seed(123)

points_1 = [Point(-2, 0), Point(4, -2), Point(4, 3), Point(-2, 3), Point(-3, 3), Point(-3, 1), Point(2, 2), Point(2, 0), Point(-1, 0), Point(-2, 0)]
points_2 = [Point(-2, 0), Point(4, -2), Point(4, 3), Point(-2, 3), Point(-3, 3), Point(-3, 1), Point(2, 2), Point(2, 0), Point(-1, 0), Point(-2, 0)]

transmitter = Transmitter(Point(-1.3, -2))
receiver = Receiver(Point(1.5, 1.5))
interferers = [Interferer.square(Point(0, 0), 9, 0),
               Interferer.shape(points=points_1, position=Point(1, 1), scale=0.8, rotation=0),
               Interferer.shape(points=points_2, position=Point(-1, -1), scale=0.8, rotation=pi),
               Interferer.polygon(position=Point(-3, 2), diameter=1, number_sides=5, rotation=0),
               Interferer.polygon(position=Point(3, -2), diameter=1, number_sides=5, rotation=pi)]
system = System(transmitter, receiver, interferers)
multipath = system.get_multipath(starting_number=3000, receiver_diameter=0.1, max_reflections=50)
camera_position = Point(0, 0)
camera_zoom = 0.1
render(system, multipath, camera_position, camera_zoom, ui_size=1, bins=15, red_factor=3)
