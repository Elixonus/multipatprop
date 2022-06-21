from multipatprop.multipatprop import System, Transmitter, Receiver, Interferer, Point, Vector
from math import pi, tau
from rich import print

transmitter = Transmitter(position=Point(0, 0))
receiver = Receiver(position=Point(5, 0))
interferer = Interferer(points=[Point(2, 2), Point(3, 2), Point(4, -2), Point(1, -2)])
system = System(transmitter=transmitter, receiver=receiver, interferers=[interferer])
path = system.get_path(transmitting_angle=pi, max_reflections=10)
print(path)