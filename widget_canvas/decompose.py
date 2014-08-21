
from __future__ import division, print_function, unicode_literals

import numpy as np
import transform_2D


def decompose(H):
    """
    Decompose general transform matrix into elemental transforms.

    Parameters
    ----------
    H : Transform matrix

    Returns
    -------
    H_translate, H_scale, H_shear, H_rotate, H_perspective

    Notes
    -----
    See this page for details:
    http://math.stackexchange.com/questions/78137/decomposition-of-a-nonsquare-affine-matrix

    Homography matrix:

        | h_11  h_12  h_13 |
    H = | h_21  h_22  h_23 |
        | h_31  h_32  h_33 |

    """

    #############################################
    # Part 1

    # Translation.
    dx = H[0, 2]
    dy = H[1, 2]
    H_translate = transform_2D.offset(dx, dy)

    # Perspective.
    px = H[2, 0]
    py = H[2, 1]
    H_perspective = transform_2D.perspective(px, py)

    #############################################
    # Part 2

    # Non-homogeneous affine transform (scale, shear, rotate).
    a_11 = H[0, 0] - H[0, 2] * H[2, 0]
    a_12 = H[0, 1] - H[0, 2] * H[1, 2]
    a_21 = H[1, 0] - H[1, 2] * H[2, 0]
    a_22 = H[1, 1] - H[1, 2] * H[2, 1]

    # Determinant.
    D2 = a_11 * a_22 - a_12 * a_21

    if D2 < 0:
        if a_11 < 0:
            a_11 *= -1
            a_12 *= -1
        else:
            a_21 *= -1
            a_22 *= -1

    # Recompute determinant.
    D2 = a_11 * a_22 - a_12 * a_21

    if D2 < 0:
        raise ValueError('Determinant should be positive: {}'.format(D2))

    #############################################
    # Part 3.
    D = D2**.5

    scale_x = (a_11**2 + a_12**2)**.5
    scale_y = D / scale_x

    shear_y = (a_11*a_21 + a_12*a_22) / D

    angle = np.arctan2(-a_12, a_11)

    H_scale = transform_2D.scale(scale_x, scale_y)
    H_shear = transform_2D.shear(shear_y)
    H_rotate = transform_2D.rotate(angle)

    # Done
    return H_translate, H_scale, H_shear, H_rotate, H_perspective


if __name__ == '__main__':
    pass