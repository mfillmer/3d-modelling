from solid import *
from math import sqrt
from solid.objects import cube, hull, rotate
from solid.utils import up, down
from solid import screw_thread


def mount_to_bottom(obj):
    return hull()(
        obj,
        linear_extrude(height=1)(projection()(obj))
    )


def cutout(size):
    c = cube(size)\
        - translate((size/2, 0, 0))(cylinder(r=size/2, h=size, segments=100))\
        - translate((size/2, size, 0))(cylinder(r=size/2, h=size, segments=100))\
        - translate((size/2, 0, 0))(cube(size))

    c = translate((size/2, -size/2, 0))(rotate((0, -90, 0))(c))
    c = rotate(90)(c)
    c = translate((0, size/2, 0))(c)

    return c


def tended_obj(w):
    return lambda obj: up(sqrt(((w/2)**2)/2))(
        rotate((45, 0, 0))(obj)
    )


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


def hollow_screw(radius=40, screw_height=80, wall=2, external=True, tooth_height=10, tooth_depth=5):
    body_radius = radius-tooth_depth if external else radius
    body = ring(r1=body_radius, h=screw_height, w=wall)

    inner_rad = body_radius if external else body_radius-wall

    SEGMENTS = 360
    NECK = 30
    section = screw_thread.default_thread_section(
        tooth_height=tooth_height, tooth_depth=tooth_depth)
    screw = screw_thread.thread(outline_pts=section,
                                inner_rad=inner_rad,
                                pitch=tooth_height+.5,
                                external=external,
                                length=screw_height,
                                segments_per_rot=SEGMENTS,
                                neck_in_degrees=NECK,
                                neck_out_degrees=NECK)

    return body + screw


def connection(d=80, h=30, wall=2, strength=2, gap=0.2, tooth_height=10, tooth_depth=5):
    radius = d/2
    adapter = hollow_screw(radius=radius-wall-gap,
                           wall=wall, screw_height=h, external=True, tooth_depth=tooth_depth, tooth_height=tooth_height)
    socket = hollow_screw(radius=radius, wall=wall,
                          screw_height=h, external=False, tooth_depth=tooth_depth, tooth_height=tooth_height)

    return (adapter, socket)


def two_sided_connection(outer_d=180, outer_w=2, outer_tooth=2, inner_d=160, inner_w=2, inner_tooth=2, height=20, gap=0.2):
    (adapter, _) = connection(d=outer_d, h=height,
                              tooth_depth=outer_tooth, wall=outer_w, tooth_height=outer_tooth*2)
    (_, socket) = connection(d=inner_d, h=height,
                             tooth_depth=inner_tooth, wall=inner_w, tooth_height=inner_tooth*2)

    con_d = outer_d-(outer_tooth+outer_w+gap)*2
    con_w = (con_d-inner_d) / 2
    con = ring(d1=con_d, w=con_w, h=height)

    return adapter + socket + con


def pipe(d=160, w=2, tooth=2, socket_h=10, h=50):
    gap = 0.2
    delta_r = w + tooth + gap
    body = ring(d1=d, h=h-(socket_h+delta_r), w=w)
    (adapter, socket) = connection(d=d, h=socket_h,
                                   wall=w, tooth_depth=tooth, tooth_height=2*tooth, gap=gap)
    pipe = translate((0, 0, socket_h+delta_r))(body)
    pipe += adapter + translate((0, 0, socket_h)
                                )(ring(r2=d/2, r1=d/2-delta_r, h=delta_r))

    pipe += up(h-socket_h)(socket)

    return pipe


def sliding_connector(length=60, width=20, gap=0.2):
    slider = cylinder(
        d=width, h=length, segments=3, center=True
    )
    socket = rotate((0, 90, 0))(
        slider +
        translate((0, 0, length/4))(
            cube((width/5*4, width/5*4, length/2), center=True)
        )
    )
    slider = cylinder(
        d=width-gap, h=length, segments=3, center=True
    )
    adapter = rotate((0, 90, 0))(
        slider *
        translate((0, 0, length/4))(
            cube((width/5*4, width/5*4, length/2), center=True)
        )
    )*translate((0, -length/2, 0))(cube((length)))

    return socket, adapter
