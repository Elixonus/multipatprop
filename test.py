from sympy import Polygon, pi
p1, p2, p3 = [(0, 0), (1, 0), (5, 1)]
poly = Polygon(p1, p2, p3)
print(poly.sides)