from solid.objects import cylinder, cube, rotate, translate


def tube(r=10, h=1, wall=1):
    return cylinder(r=r, h=h) - cylinder(r=r-wall, h=h)


def arc(angle=30, r=10, h=1, w=1, segment=5):
    quarter = tube(r, h, w)*cube(r*2)
    unit = quarter*rotate((0, 0, 90-segment))(quarter)
    return sum([rotate((0, 0, x))(unit) for x in range(segment, angle+segment, segment)])
