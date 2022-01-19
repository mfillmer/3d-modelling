from solid.objects import cube
from starter_kit.prism import prism


def blade(width=100, length=6):
    return cube((width, 10, 2)) * prism(length, width=width)
