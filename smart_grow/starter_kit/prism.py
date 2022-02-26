
from solid.objects import cube, rotate, translate
from math import sqrt


def prism(length=5, width=100):
    side = sqrt(length**2/2)
    c = cube((width, side, side))
    c -= rotate((45, 0, 0))(cube((width, side**2, side)))
    c = rotate((135, 0, 0))(c)
    c = translate((0, sqrt(side**2*2), 0))(c)

    return c
