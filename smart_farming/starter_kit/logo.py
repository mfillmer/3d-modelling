from solid.objects import cylinder, cube, rotate, translate


def tube(r=10, h=1, wall=1):
    return cylinder(r=r, h=h) - cylinder(r=r-wall, h=h)


def arc(angle=30, r=10, h=1, w=1, segment=5):
    quarter = tube(r, h, w)*cube(r*2)
    unit = quarter*rotate((0, 0, 90-segment))(quarter)
    return sum([rotate((0, 0, x))(unit) for x in range(segment, angle+segment, segment)])


def logo(w=40, h=1):
    r1 = w/2
    r2 = r1/3*2

    leaves = rotate((0, 0, 180))(arc(h=h, angle=180, r=r2)) \
        + translate((r2, r2-0.5, 0))(rotate((0, 0, 90))(arc(h=h, r=r2, angle=145)))\
        + translate((r2, -r2+0.5, 0))(rotate((0, 0, -55))
                                      (arc(h=h, r=r2, angle=145)))

    bulb = tube(r1, wall=2, h=h)\
        + translate([5, 0, 0])(rotate((0, 0, 240))(arc(h=h, angle=60, r=r1, w=2)))\
        + translate([10, 0, 0])(rotate((0, 0, 240))(arc(h=h, angle=60, r=r1, w=2)))\
        + translate([15, 0, 0])(rotate((0, 0, 240))(arc(h=h, angle=60, r=r1, w=2)))\

    logo = bulb + translate((-(r1/3), 0, 0))(leaves)

    return logo
