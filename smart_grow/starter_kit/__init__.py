

from solid.objects import cube, rotate, translate
from solid.utils import forward, left, right

from starter_kit.blade import blade
from starter_kit.box import box
from starter_kit.grid import grid
from starter_kit.logo import arc, logo, tube

inner_corner = arc(angle=90, r=4, h=42, w=2)
outer_corner = arc(angle=90, r=4, h=60, w=2)

inner_corners = translate((6, 68, 0))(rotate((0, 0, 0))(inner_corner))\
    + translate((6, 6, 0))(rotate((0, 0, 90))(inner_corner))\
    + translate((138, 6, 0))(rotate((0, 0, 180))(inner_corner))\
    + translate((138, 68, 0))(rotate((0, 0, 270))(inner_corner))

outer_corners = translate((2, 72, 0))(rotate((0, 0, 0))(outer_corner))\
    + translate((2, 2, 0))(rotate((0, 0, 90))(outer_corner))\
    + translate((142, 2, 0))(rotate((0, 0, 180))(outer_corner))\
    + translate((142, 72, 0))(rotate((0, 0, 270))(outer_corner))

Einsatzschneide = forward(70)(
    rotate((0, 0, 270))(
        sum([forward(x)(blade(70, length=4)) for x in range(0, 140, 8)]
            + [
            cube((2, 140, 2)),
            right(68)(cube((2, 140, 2))),
            cube((70, 2, 2)),
            forward(138)(cube((70, 2, 2)))
        ])
    )
)

Aufsatzschneide = forward(70)(
    rotate((0, 0, 270))(
        sum([forward(x)(blade(70, length=4)) for x in range(6, 142, 8)]
            + [
            cube((2, 144, 2)),
            right(68)(cube((2, 144, 2))),
            cube((70, 2, 2)),
            forward(142)(cube((70, 2, 2))),
            # blade(70, 4),
            # forward(140)(blade(70, 4))
        ])
    )
)

logo_vertical = translate((0, 15, 30))(rotate((0, 90, 0))(logo(30)))

Untersatz = box(144, 74, 60, 4) \
    + translate((2, 2, 2))(box(140, 70, 40, 4)) \
    - translate((0, 2, 58))(cube((144, 70, 2)))\
    - translate((0, 22, 7))(logo_vertical)\
    - translate((143, 22, 7))(logo_vertical)


Untersatz = Untersatz\
    + inner_corners\
    - outer_corners

Einlegeboden = grid(length=138)


Logo = logo()
