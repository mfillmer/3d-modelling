from solid import cylinder, translate
from solid.objects import cube, hull, rotate


def ring(r1=10, r2=None, h=2, w=2, dx=0, dy=0, dz=0):
    r2 = r2 or r1
    s = 60
    outer = cylinder(r1=r1, r2=r2, h=h, segments=s)
    inner = cylinder(r1=r1-w, r2=r2-w, h=h, segments=s)
    return translate((dx, dy, dz))(outer-inner)


def slot(*args, angle=30, r1=10, r2=None, w=2, h=2, **kwargs):
    r2 = r2 or r1
    size = max(r1, r2, w, h, 100)
    size *= 2
    half = ring(*args, r1=r1, r2=r2, w=w, h=h, **kwargs)
    half -= translate((-size/2, -size, 0))(cube(size))
    if angle == 180:
        return half
    elif angle < 180:
        return half * rotate((0, 0, 180+angle))(half)
    else:
        return half + rotate((0, 0, angle))(half)


def socket(r=12, w=2, d=None):
    if d is not None:
        r = d/2
    h = w*4
    hook = hull()(slot(r1=r-w, r2=r, h=w, dz=h-w*2)
                  + slot(r1=r, h=w, w=w*1.5, dz=h-w*3)
                  + slot(r1=r, r2=r-w, h=w, dz=h-w*4))\
        + ring(r1=r, h=w*3, dz=h-w*4)\

    top = sum([rotate((0, 0, r))(hook) for r in [0, 120, 240]])
    return top


def adapter(r=12, w=2, d=None):
    """
    adapter which mounts into socket. diamoter/radius needs to be the same as the ones specified for the socket. Height will result in 7w.
    """
    if d is not None:
        r = d/2
    bottom = ring(r1=r-w, h=w, w=w)\
        + ring(r1=r-w*2, h=w*2, w=w)\
        + ring(r1=r-w, r2=r-w*2, h=w, w=w, dz=w)\
        + ring(r1=r-w*2, h=w, w=w, dz=w*2) \
        + ring(r1=r-w*2, r2=r+w, h=w*4, w=w, dz=w*3)\
        + ring(r1=r, dz=w*6, h=w)\
        - ring(r1=r+w, h=w*3, w=w, dz=w*5)
    slots = sum([rotate((0, 0, a))(slot(r1=r-w + 0.5, w=w+0.5, h=w*2, angle=40))
                for a in [0, 120, 240]])
    stopper = sum([rotate((0, 0, a))(translate((r-w*3, -w, 0))
                  (cube((w*2, w, w*5)))) for a in [0, 120, 240]])
    stopper_ring = stopper - ring(r1=r - w*3, r2=r-w, h=w*2, dz=w*3, w=w*5)

    return bottom - slots + stopper_ring


def pipe(r=12, w=2, h=44, d=None):
    if d is not None:
        r = d/2
    bottom = ring(r1=r-w, h=w, w=w)\
        + ring(r1=r-w*2, h=w*2, w=w)\
        + ring(r1=r-w, r2=r-w*2, h=w, w=w, dz=w)\
        + ring(r1=r-w*2, h=w, w=w, dz=w*2) \
        + ring(r1=r-w*2, r2=r+w, h=w*4, w=w, dz=w*3)\
        + ring(r1=r, dz=w*6, h=w)\
        - ring(r1=r+w, h=w*3, w=w, dz=w*5)

    middle = ring(r1=r, dz=w*7, h=h-w*11)

    slots = sum([rotate((0, 0, a))(slot(r1=r-w + 0.5, w=w+0.5, h=w*2, angle=40))
                for a in [0, 120, 240]])

    stopper = sum([rotate((0, 0, a))(translate((r-w*3, -w, 0))
                  (cube((w*2, w, w*5)))) for a in [0, 120, 240]])
    stopper -= ring(r1=r - w*3, r2=r-w, h=w*2, dz=w*3, w=w*5)

    hook = hull()(slot(r1=r-w, r2=r, h=w, dz=h-w*2)
                  + slot(r1=r, h=w, w=w*1.5, dz=h-w*3)
                  + slot(r1=r, r2=r-w, h=w, dz=h-w*4))\
        + ring(r1=r, h=w*3, dz=h-w*4)\
        + (ring(r1=r, h=w, dz=h-w) * ring(r1=r, r2=r+w, h=w, dz=h-w))\

    top = sum([rotate((0, 0, r))(hook) for r in [0, 120, 240]])

    pipe = bottom + middle - slots + top + stopper
    return pipe
