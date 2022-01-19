

from solid.objects import cube, rotate, translate
from solid.utils import forward, left, right

from starter_kit.blade import blade
from starter_kit.box import box
from starter_kit.grid import grid


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
        sum([forward(x)(blade(70, length=4)) for x in range(0, 140, 8)]
            + [
            cube((2, 144, 2)),
            right(68)(cube((2, 144, 2))),
            cube((70, 2, 2)),
            forward(142)(cube((70, 2, 2)))
        ])
    )
)

Untersatz = box(144, 74, 60, 4) \
    + translate((0, 2, 2))(box(144, 70, 40, 4)) \
    + translate((0, 4, 2))(box(144, 66, 40, 4)) \
    - translate((0, 2, 58))(cube((144, 70, 2)))


Einlegeboden = grid()
