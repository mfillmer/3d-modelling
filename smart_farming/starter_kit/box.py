from solid.objects import cube, translate


def box(length=140, width=70, height=60, wall=4):
    c = cube((length, width, height))
    inner = cube((length-wall, width-wall, height))
    c -= translate((wall/2, wall/2, wall/2))(inner)

    return c


Untersatz = box(144, 74, 60, 2) \
    + translate((0, 2, 2))(box(144, 70, 40, 2)) \
    + translate((0, 4, 2))(box(144, 66, 40, 2)) \
    - translate((0, 2, 58))(cube((144, 70, 2)))
