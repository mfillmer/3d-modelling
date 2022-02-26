from solid.objects import cube, translate
from solid.utils import right, forward


def grid(length=140, width=70, height=2):
    c = cube((length, width, 14))
    c -= translate((2, 2, 2))(cube((length-4, width-4, 12)))

    holes = right(3)(forward(2)(cube(2)))
    for x in range(3, length-3, 4):
        for y in range(2, width-2, 4):
            holes += translate((x, y, 0))(cube(2))

    return c - holes
