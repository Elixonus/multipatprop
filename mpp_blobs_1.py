from random import seed
from multipatprop.multipatprop import System, Transmitter, Receiver, Interferer, Point
from multipatprop.output import render

seed(1123)


transmitter = Transmitter(Point(-2.3, -2.5))
receiver = Receiver(Point(2, 3))
interferers = [Interferer.square(Point(0, 0), 9, 0),
               Interferer.blob(position=Point(0, 0), average_radius=1.5, number_points=50, smoothing_factor=0.3, smoothing_iterations=3),
               Interferer.blob(position=Point(-2, 3), average_radius=0.5, number_points=20),
               Interferer.blob(position=Point(3, 3), average_radius=0.5, number_points=20),
               Interferer.blob(position=Point(-3, -3), average_radius=0.5, number_points=20),
               Interferer.blob(position=Point(2.5, -2.5), average_radius=0.5, number_points=20)]
system = System(transmitter, receiver, interferers)
multipath = system.get_multipath(starting_number=500, receiver_diameter=0.1, max_reflections=30)
camera_position = Point(0, 0)
camera_zoom = 0.1
render(system, multipath, camera_position, camera_zoom, ui_size=1, bins=30, red_factor=0.5)
