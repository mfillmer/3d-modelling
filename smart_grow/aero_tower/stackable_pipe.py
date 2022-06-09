from solid import cylinder, translate, square, rotate_extrude
from solid.objects import cube, hull, rotate
from solid import screw_thread


def ring(r1=10, r2=None, d1=None, d2=None, h=2, w=2, dx=0, dy=0, dz=0):
    if d1 is not None:
        r1 = d1/2
    if d2 is not None:
        r2 = d2/2
    r2 = r2 or r1
    s = 100
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


def hook(r=80, w=2, d=4, angle=30):

    plain = square((w, 3*d)) + translate((-2*d, d, 0))(square(d))
    translated_plain = hull()(translate((r-w, 0, 0))(plain))
    model = rotate_extrude(angle=angle, segments=100)(translated_plain)

    return model


def socket(r=12, w=2, d=None, gap=0, slots=3):
    '''
    @gap: describes the gap between socket and adapter. Should be between 0 and 1. Height will result in 3w.
    '''
    if d is not None:
        r = d/2

    _hook = hook(r=r, w=w/2, d=w, angle=30)
    # hull()(
    #     slot(r1=r-w, r2=r, h=w, dz=w*2),  # top
    #     slot(r1=r, h=w, w=w*2, dz=w),  # middle
    #     slot(r1=r, r2=r-w, h=w)  # bottom
    # )

    top = sum([rotate((0, 0, r))(_hook) for r in range(0, 360, 360//slots)])

    top += ring(r1=r, h=w*3, w=w/2)
    top -= ring(r1=r-w*2+gap, r2=r-w, h=w, w=w, dz=w*2)  # top
    top -= ring(r1=r-w*2+gap, h=w*3, w=w)  # middle
    top -= ring(r1=r-w, r2=r-w*2+gap, h=w, w=w)  # bottom

    return top


def adapter(r=12, w=2, d=None, slots=3, gap=0.2):
    """
    adapter which mounts into socket. diamoter/radius needs to be the same as the ones specified for the socket. Height will result in 7w.
    """
    angles = range(0, 360, 360//slots)
    if d is not None:
        r = d/2

    # outer and inner bottomring
    # add gap for smoother insert into socket
    bottom = ring(r1=r-w-gap, r2=r-w, h=w, w=w)\
        + ring(r1=r-w*2, h=w*3, w=w)

    # pipe transition
    bottom += ring(r1=r, dz=w*6, h=w)

    # diameter transitions
    bottom += ring(r1=r-w*2, r2=r+w, h=w*4, w=w, dz=w*3)\
        + ring(r1=r-w, r2=r-w*2, h=w, w=w, dz=w)

    # cut off overhang
    bottom -= ring(r1=r+w, h=w*3, w=w, dz=w*5)

    slot_cut = slot(r2=r-w + 0.5, r1=r-w + 0.5 - gap, w=w+0.5, h=w*2, angle=40)
    slots = sum([rotate((0, 0, a))(slot_cut) for a in angles])
    stopper = sum([rotate((0, 0, a))(translate((r-w*3, -w, 0))
                  (cube((w*2, w, w*5)))) for a in angles])
    stopper_ring = stopper - ring(r1=r - w*3, r2=r-w, h=w*2, dz=w*3, w=w*5)

    return bottom - slots + stopper_ring


def pipe(r=12, w=2, h=44, d=None):
    if d is not None:
        r = d/2
    bottom = adapter(r=r, w=w, d=d, slots=3)

    middle = ring(r1=r, dz=w*7, h=h-w*11)

    top = translate((0, 0, h-4*w))(socket(r=r, w=w, d=d, gap=0.2, slots=3))

    pipe = bottom + middle + top
    return pipe


def hollow_screw(radius=40, screw_height=80, wall=2, external=True, tooth_height=10, tooth_depth=5):
    body_radius = radius-tooth_depth if external else radius
    body = ring(r1=body_radius, h=screw_height, w=wall)

    inner_rad = body_radius if external else body_radius-wall

    SEGMENTS = 48
    section = screw_thread.default_thread_section(
        tooth_height=tooth_height, tooth_depth=tooth_depth)
    screw = screw_thread.thread(outline_pts=section,
                                inner_rad=inner_rad,
                                pitch=tooth_height+.5,
                                external=external,
                                length=screw_height,
                                segments_per_rot=SEGMENTS,
                                neck_in_degrees=90,
                                neck_out_degrees=90)

    return body + screw


def connection(d=80, h=30, wall=2, strength=2, gap=0.2):
    radius = d/2
    adapter = hollow_screw(radius=radius-wall-gap,
                           wall=wall, screw_height=h, external=True)
    socket = hollow_screw(radius=radius, wall=wall,
                          screw_height=h, external=False)

    return (adapter, socket)
