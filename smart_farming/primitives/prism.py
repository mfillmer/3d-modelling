
from solid.objects import cube, rotate, translate
from math import sqrt


def prism(height=5, width=100):
    c = cube((width, height, height))
    c -= rotate((45, 0, 0))(cube((width, height**2, height)))
    c = rotate((135, 0, 0))(c)
    c = translate((0, sqrt(height**2*2), 0))(c)

    return c
