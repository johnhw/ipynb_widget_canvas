
from __future__ import division, print_function, unicode_literals, absolute_import

"""
Apply transforms to point data and image data.
"""

import numpy as np


def make_homogeneous(points):
    """
    Convert 2D Cartesian points to 3D Homogeneous.
    http://en.wikipedia.org/wiki/Homogeneous_coordinates

    Parameters
    ----------
    points : array_like
        Two dimensional array with shape (num_points, 2)
        *or*
        One dimensional array with shape (2,)

    Returns
    -------
    points_homog : ndarray with shape (num_points, 3) or (3,)
    """
    points = np.asarray(points)

    if points.ndim == 1:
        # change shape (2,) --> (1,2)
        points = points[None, :]
    elif points.ndim == 2:
        pass
    else:
        raise ValueError('Invalid data: {}'.format(points.shape))

    num_points = points.shape[0]
    if points.shape[1] != 2:
        raise ValueError('Invalid 2D data: {}'.format(points.shape))

    # Extend to 3D.
    points_homog = np.hstack((points, np.ones((num_points, 1))))

    return points_homog


def make_cartesian(points):
    """
    Ensure that data points are 2D Cartesian.
    http://en.wikipedia.org/wiki/Homogeneous_coordinates

    Parameters
    ----------
    points : array_like
        Two dimensional Homogeneous data with shape (num_points, 3).
        *or*
        One dimensional array with shape (3,).

    Returns
    -------
    points_cart : Two dimensional array with shape (num_points, 2)
    """
    points = np.asarray(points)

    if points.ndim == 1:
        # change shape (3,) --> (1,3)
        points = points[None, :]
    elif points.ndim == 2:
        pass
    else:
        raise ValueError('Invalid data: {}'.format(points.shape))

    if points.shape[1] != 3:
        raise ValueError('Invalid 3D data: {}'.format(points.shape))

    points_cart = points[:, :2]
    points_cart[:, 0] /= points[:, 2]
    points_cart[:, 1] /= points[:, 2]

    return points_cart


def is_singular(H):
    """
    Check if transform matrix is singular.
    """
    value_test = H[0, 0]*H[1, 1] - H[0, 1]*H[1, 0]

    if abs(value_test) <= 1.e-6:
        return True
    else:
        return False


def is_valid(H, reason=False):
    """
    Check that supplied transform matrix has proper shape and structure.

    Parameters
    ----------
    H : Transform matrix

    Returns
    -------
    bool

    """
    H = np.asarray(H)
    msg = ''

    ###############
    if H.ndim != 2:
        msg = 'not 2D array'

        if reason:
            return False, msg
        else:
            return False

    ###############
    if not (H.shape[0] == 3 and H.shape[1] == 3):
        msg = 'not 3x3 array'
        if reason:
            return False, msg
        else:
            return False

    ###############
    eps = 1.e-6
    val = H[-1, -1]
    try:
        if abs(val - 1.) > eps:
            msg = 'bottom-right element must be 1'
            if reason:
                return False, msg
            else:
                return False

    except ValueError:
        msg = 'array element is not a scalar'
        if reason:
            return False, msg
        else:
            return False

    ###############
    # Singular?
    if is_singular(H):
        msg = 'matrix is singular'
        if reason:
            return False, msg
        else:
            return False

    ###############
    # Everything checks out fine.
    if reason:
        if not msg:
            msg = 'everything is fine'

        return True, msg
    else:
        return True


#################################################

"""
Build transform matrix from component values (rotation angle, offset vector, etc.)
"""


def translate(offset_x, offset_y=None):
    """
    Build translation matrix.

    Parameters
    ----------
    offset : translation vector, 2D ndarray

    Returns
    -------
    H : Homogeneous transformation matrix
    """
    if offset_y is not None:
        offset_x = offset_x, offset_y

    H = np.identity(3)
    H[:2, 2] = offset_x[:2]

    return H


def rotate(angle, origin=None):
    """
    Build rotation matrix about a point.
    http://en.wikipedia.org/wiki/Transformation_matrix#Rotation

    Right-hand rule.

    Parameters
    ----------
    angle : Angle of rotation (radians)
    origin : Center of rotation, default to origin, optional

    Returns
    -------
    H : Homogeneous transformation matrix
    """
    cosa = np.cos(angle)
    sina = np.sin(angle)

    H = np.identity(3)
    H[0, 0] = cosa
    H[0, 1] = -sina
    H[1, 0] = sina
    H[1, 1] = cosa

    if origin is not None:
        origin = make_homogeneous(origin)

        offset = origin - np.dot(H, origin)
        H[:, 2] = offset

    return H


def scale(factor, factor_y=None):
    """
    Build scaling matrix.

    Parameters
    ----------
    factor : Size scale factor(s): scalar or two-element sequence

    Returns
    -------
    H : Homogeneous transformation matrix
    """
    if factor_y is not None:
        factor = factor, factor_y
    factor = np.asarray(factor)

    if factor.size == 1:
        H = np.diag([factor, factor, 1.0])
    elif factor.size == 2:
        H = np.diag([factor[0], factor[1], 1.0])
    else:
        raise ValueError('Invalid scale factor: {:s}'.format(factor))

    return H


def shear(shear_y):
    """
    Build transform to shear by given angle.

    Parameters
    ----------
    shear_y : shear factor Y directions.

    Returns
    -------
    H : Homogeneous transformation matrix

    Notes
    -----
    This one took me about 20 minutes to figure out the geometry.  It helps to think in 3D to fully
    understand how it works for a 2D problem.  I guess that's why we do everything in Homogeneous
    coordinates, eh?

    The shear plane defines the 2D space where distances between two points are unaffected by the
    shear transform.  For 2D problems the shear plane may be any plane orthogonal to the XY plane.
    This plane is defined by two items: a point in the XY plane and a vector normal to the shear
    plane (also defined in the XY plane for 2D problems).  For convenience we define the direction
    vector as one constrained to lie within the XY plane and within the shear plane.  Thus the
    direction vector is orthogoinal to the above normal vector.

    A point P in the XY plane is transformed by the shear matrix into P" such that the vector P-P"
    is parallel to the direction vector and the angle is defined by P-P'-P", where P' is the
    orthogonal projection of P onto the shear plane.

    In 2D, it is best to set the reference point to the origin and let the shear normal be computed
    from the supplied parameters.

    In the end its really just easier to think of this in terms of X and Y shear factors: sx and
    sy.
    """

    Hsy = np.identity(3)

    Hsy[1, 0] = shear_y

    return Hsy


def perspective(p, py=None):
    """
    Build transform containing perspective partition data.

    Parameters
    ----------
    pa, pb : perspective scale parameters

    Returns
    -------
    H : Homogeneous transformation matrix
    """
    if py is not None:
        p = p, py

    H = np.identity(3)

    H[2, 0] = p[0]
    H[2, 1] = p[1]

    return H


def invert(H):
    """
    Invert supplied transform matrix and normalize to unit homography scale factor,
    e.g. H[-1, -1] = 1.0.  Therefore this inverse function is not the same as np.linalg.inv().

    Parameters
    ----------
    H : Transform matrix

    Returns
    -------
    H_inv : Inverse of matrix H
    """
    ok, msg = is_valid(H, reason=True)
    if not ok:
        raise ValueError('Invalid transform H: {}.  Reason: {:s}'.format(H, msg))

    H_inv = np.linalg.inv(H)

    # Normalize result to proper homogeneous form.
    # H_inv /= H_inv[-1, -1]

    return H_inv


def concatenate(*matrices):
    """
    Concatenate together a sequence of transformation matrices.  The last entry in the
    supplied set of transforms is the first to be applied to data.

    Parameters
    ----------
    matrices : Sequence of (3, 3) transformations.

    Notes
    -----
    if matrices = [H2, H1], then output of this function is the combined transform of applying H1
    to some data, and then next applying H2 to the output of the previous step.

    Returns
    -------
    H : Concatenation of input transformation matrices, (3, 3)
    """
    H = np.identity(3)

    for Q in matrices[::-1]:
        flag, reason = is_valid(Q, reason=True)
        if not flag:
            raise ValueError('Invalid transform Q: {}.  Reason: {}'.format(Q, reason))

        H = Q.dot(H)

    # Normalize result to proper homogeneous form.
    H /= H[-1, -1]

    return H


#################################################
"""
compute basic component values from supplied transform matrix.
"""


def decompose(H, as_transforms=False):
    """
    Decompose general transform matrix into elemental transforms.

    Parameters
    ----------
    H : Homogeneous transformation matrix

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
    offset_x = H[0, 2]
    offset_y = H[1, 2]

    # Perspective.
    persp_x = H[2, 0]
    persp_y = H[2, 1]

    #############################################
    # Part 2

    # Non-homogeneous affine transform (scale, shear, rotate).
    a_11 = H[0, 0] - H[0, 2] * H[2, 0]
    a_12 = H[0, 1] - H[0, 2] * H[2, 1]
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

        # Recompute determinant a different way.
        D2 = a_11 * a_22 - a_12 * a_21

    if D2 < 0:
        raise ValueError('Determinant should be positive: {}'.format(D2))

    #############################################
    # Part 3.

    scale_x = (a_11**2 + a_12**2)**.5
    scale_y = D2 / scale_x

    shear_y = (a_11*a_21 + a_12*a_22) / D2

    angle = np.arctan2(-a_12, a_11)

    if as_transforms:
        H_translate = translate(offset_x, offset_y)
        H_scale = scale(scale_x, scale_y)
        H_shear = shear(shear_y)
        H_rotate = rotate(angle)
        H_perspective = perspective(persp_x, persp_y)

        return H_translate, H_scale, H_shear, H_rotate, H_perspective

    else:
        offset_xy = (offset_x, offset_y)
        scale_xy = (scale_x, scale_y)
        # shear_y = shear_y
        persp = (persp_x, persp_y)

        return offset_xy, scale_xy, shear_y, angle, persp

#################################################


def warp_points(points, H):
    """
    Warp 2D points via numpy matrix multiply.
    """
    points = np.asarray(points)

    if points.ndim == 1:
        # change shape (2,) --> (1,2)
        points = points[None, :]
    elif points.ndim == 2:
        pass
    else:
        raise ValueError('Invalid data: {}'.format(points.shape))

    if points.shape[1] != 2:
        raise ValueError('Invalid 2D data: {}'.format(points.shape))

    points_H = make_homogeneous(points)

    points_out_H = H.dot(points_H.T).T

    points_out = make_cartesian(points_out_H)

    return points_out

#################################################


class Transform(object):
    """
    This is a simple class for manipulating and keeping track of a transformation matrix.
    """
    def __init__(self, H=None):
        """
        Create a new instance of a Transform Homography matrix:

            | h_11  h_12  h_13 |
        H = | h_21  h_22  h_23 |
            | h_31  h_32  h_33 |

        These values are stored internally as a 3x3 array, but in practice they are flattened to a
        sequence of numbers.  This sequence form is directly compatible with
        the HTML5 Canvas Element's Context method setTransform().  The internal flattened
        representation is given by the sequence: M = [m11, m12, m21, m22, m13, m23]

        See link for details:
        http://www.whatwg.org/specs/web-apps/current-work/multipage/the-canvas-element.html

        Different browser API implementation may swap m12 with m21.  See the Note mentioned in the
        linked description.
        """
        self._matrix = None
        self.H = H

    def __repr__(self):
        """
        Pretty self-representation.
        """
        template = '{:6.2f} {:6.2f} {:6.2f}\n{:6.2f} {:6.2f} {:6.2f}\n{:6.2f} {:6.2f} {:6.2f}\n'

        result = template.format(self.H[0, 0], self.H[0, 1], self.H[0, 2],
                                 self.H[1, 0], self.H[1, 1], self.H[1, 2],
                                 self.H[2, 0], self.H[2, 1], self.H[2, 2])
        return result

    def _repr_latex_(self):
        """
        Pretty self-representation using IPython display system.
        """
        template = """
                \\begin{{equation*}}
                M = \\begin{{vmatrix}} {:6.2f} & {:6.2f} & {:6.2f} \\\\
                                       {:6.2f} & {:6.2f} & {:6.2f} \\\\
                                       {:6.2f} & {:6.2f} & {:6.2f} \\end{{vmatrix}}
                \\end{{equation*}}
                """

        result = template.format(self.H[0, 0], self.H[0, 1], self.H[0, 2],
                                 self.H[1, 0], self.H[1, 1], self.H[1, 2],
                                 self.H[2, 0], self.H[2, 1], self.H[2, 2])
        return result

    def copy(self):
        """
        Return copy of self.
        """
        return Transform(self.H.copy())

    def reset(self):
        """
        Reset transform to 3x3 identity matrix.
        """
        self.H = None

    @property
    def H(self):
        """
        Return current 3x3 transform matrix.
        """
        return self._matrix

    @H.setter
    def H(self, H):
        """
        Set current 3x3 transform matrix.
        """
        if H is None:
            H = np.identity(3)

        H = np.asarray(H)

        if H.shape != (3, 3):
            raise ValueError('Invalid matrix shape: {}'.format(H.shape))

        # Normalize to proper homogeneous form.
        H /= H[-1, -1]

        self._parts = None
        self._matrix = H

    #############################################

    def apply(self, H):
        """
        Apply supplied 3x3 matrix transform to self.
        Input H may be 3x3 numpy array, or a Transform instance.
        """
        if isinstance(H, Transform):
            H = H.H

        self.H = H.dot(self.H)

        return self

    def rotate(self, a):
        """
        Apply rotation to self.
        """
        P = rotate(a)
        return self.apply(P)

    def translate(self, o):
        """
        Apply translation to self.
        """
        P = translate(o)
        return self.apply(P)

    def scale(self, s):
        """
        Apply scale factor to self.
        """
        P = scale(s)
        return self.apply(P)

    def shear(self, z):
        """
        Apply shear to self.
        """
        P = shear(z)
        return self.apply(P)

    def invert(self):
        """
        Invert self.
        """
        self.H = invert(self.H)
        return self

    def warp_points(self, points):
        """
        Apply self to supplied 2D points coordinates.

        Two-dimensional points with shape: (N, 2)
        """
        return warp_points(points, self.H)

    #############################################

    @property
    def offset(self):
        """
        Current translation offset.
        """
        if not self._parts:
            self._parts = decompose(self.H)
        # offset_xy, scale_xy, shear_y, angle, persp = decompose(self.H)
        return self._parts[0]

    @property
    def scale_factor(self):
        """
        Current scale factor.
        """
        if not self._parts:
            self._parts = decompose(self.H)
        # offset_xy, scale_xy, shear_y, angle, persp = decompose(self.H)
        return self._parts[1]

    @property
    def shear_factor(self):
        """
        Cuurrent shear factor.
        """
        if not self._parts:
            self._parts = decompose(self.H)
        # offset_xy, scale_xy, shear_y, angle, persp = decompose(self.H)
        return self._parts[2]

    @property
    def angle(self):
        """
        Current rotation angle.
        """
        if not self._parts:
            self._parts = decompose(self.H)
        # offset_xy, scale_xy, shear_y, angle, persp = decompose(self.H)
        return self._parts[3]

#################################################

if __name__ == '__main__':
    pass
