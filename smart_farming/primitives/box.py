from solid.objects import cube, translate


def box(length=140, width=70, height=60, wall=4):
    c = cube((length, width, height))
    inner = cube((length-wall, width-wall, height))
    c -= translate((wall/2, wall/2, wall/2))(inner)

    return c
