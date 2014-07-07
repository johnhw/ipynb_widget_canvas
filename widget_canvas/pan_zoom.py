
from __future__ import division, print_function, unicode_literals

"""Helper functions to provide Pan/Zoom callback functionality.
"""

import transform



def handle_scroll(ev):
    tick = ev['deltaY']

    factor = 1.1

    if tick == 0:
#         raise Exception()
#         print('tick == 0, do nothing')
        return

    if tick > 0:
        scl = factor
    else:
        scl = 1./factor

    px, py = ev['canvas_xy']

    Q = T.copy()
    px, py = Q.invert().transform_point(px, py)
    T.translate(px, py).scale(scl).translate(-px, -py)

    update_transform(T)


def handle_drag(ev):
    dx, dy = ev['drag_delta_xy']

    Q = T.copy()
    Q.invert()

    p0x, p0y = Q.m13, Q.m23  # Q.transform_point(0, 0)
    pdx, pdy = Q.transform_point(dx, dy)

    T.translate(pdx-p0x, pdy-p0y)

    update_transform(T)


