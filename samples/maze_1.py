import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from math import pi
from random import seed
from mazelib import Maze
from mazelib.generate.Prims import Prims
from multipatprop import System, Transmitter, Receiver, Interferer, Point
from output import render


maze = Maze(1)
maze.generator = Prims(5, 5)
maze.generate()

transmitter = Transmitter(Point(-2, -2))
receiver = Receiver(Point(2, 1.5))
interferers = []
for x in range(len(maze.grid)):
    for y in range(len(maze.grid[0])):
        if maze.grid[x][y] == 0:
            continue
        position = Point(5 * ((x / (len(maze.grid) - 1)) - 0.5),
                         5 * ((y / (len(maze.grid[0]) - 1)) - 0.5))
        interferers.append(Interferer.square(position, length=0.5, rotation=0))
system = System(transmitter, receiver, interferers)
multipath = system.get_multipath(starting_number=2000, receiver_diameter=0.1, max_reflections=50)
camera_position = Point(0, 0)
camera_zoom = 0.15
render(system, multipath, camera_position, camera_zoom, ui_size=1, bins=15, red_factor=0.2)
