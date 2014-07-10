
from __future__ import division, print_function, unicode_literals

import numpy as np


"""
Build and deconstruct transformation matrices for 2D problems.

https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
"""


def is_homogeneous(points):
    """
    Determine if supplied data points are homogeneous (True) or Cartesian (False).

    Returns
    -------

    True or False
    """
    # points = np.asarray(points)

    if points.ndim == 1:
        # Vector.
        if points.size == 2:
            # Cartesian
            return False
        else:
            # Homogeneous
            return True
    elif points.ndim == 2:
        # Array.
        space_dims = points.shape[1]
        if space_dims == 2:
            # Cartesian
            return False
        elif space_dims == 3:
            # Homogeneous
            return True
        else:
            raise ValueError('Invalid input spatial dimension size: {:d}'.format(space_dims))
    else:
        raise ValueError('Invalid number of data dimensions: {:d}'.format(points.ndim))


def homogeneous(points):
    """
    Ensure that supplied data points are 3D Homogeneous.
    http://en.wikipedia.org/wiki/Homogeneous_coordinates

    Parameters
    ----------
    points : array_like
        Two dimensional array with shape (num_points, 2) or (num_points, 3).
        *or*
        One dimensional array with shape (2,) or (3,).

    Returns
    -------
    points_homog : ndarray with shape (num_points, 3) or (3,)

    """
    points = np.asarray(points)

    if is_homogeneous(points):
        # Input data is just fine like it is.  No need to change.
        points_homog = points
    else:
        # Convert to homogeneous, extend to 3rd dimension.
        if points.ndim == 1:
            # Single point
            points_homog = np.asarray([points[0], points[1], 0])
        elif points.ndim == 2:
            # Multiple data points.
            num_points = points.shape[0]
            col = np.zeros((num_points, 1))
            points_homog = np.concatenate((points, col), axis=1)

    return points_homog


def cartesian(points):
    """
    Ensure that data points are 2D Cartesian.
    http://en.wikipedia.org/wiki/Homogeneous_coordinates

    Parameters
    ----------
    points : array_like
        Two dimensional array with shape (num_points, 2) or (num_points, 3).
        *or*
        One dimensional array with shape (2,) or (3,).

    Returns
    -------
    points_cart : Two dimensional array with shape (num_points, 2) or (2,)

    """
    points = np.asarray(points)

    if is_homogeneous(points):
        # Convert to Cartesian, collapse to 2nd dimension.
        if points.ndim == 1:
            # Single point
            points_cart = points[:2]
        elif points.ndim == 2:
            # Multiple data points.
            points_cart = points[:, :2]
    else:
        # Input data is just fine like it is.  No need to change.
        points_cart = points

    return points_cart


def transform_is_valid(H):
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
    if H.ndim != 2:
        return False

    if not (H.shape[0] == 3 and H.shape[1] == 3):
        return False

    eps = 1.e-6
    val = H[-1, -1]
    if abs(val - 1.) > eps:
        return False

    # Everything checks out fine.
    return True

#################################################


def translate(offset):
    """
    Build translation matrix.

    Parameters
    ----------
    offset : Translation vector, 2D ndarray

    Returns
    -------
    H : Transform matrix

    """
    offset = homogeneous(offset)

    H = np.identity(3)
    H[:, 2] = offset

    return H


def rotate(angle, origin=None):
    """
    Build rotation matrix about a point.

    Parameters
    ----------
    angle : Angle of rotation (radians)
    origin : Center of rotation, default to rotation about origin, optional

    Returns
    -------
    H : Homogeneous transformation matrix

    """
    cosa = np.cos(angle)
    sina = np.sin(angle)

    H = np.identity(3)
    H[0, 0] = cosa
    H[1, 1] = cosa
    H[0, 1] = sina
    H[1, 0] = sina

    if not origin is None:
        origin = homogeneous(origin)

        # offset = origin - np.dot(H, origin)
        offset = np.dot((np.identity(3) - H), origin)
        H[:, 2] = offset

    return H


def scale(factor):
    """
    Build scaling matrix.

    Parameters
    ----------
    factor : Size scale factor(s): scalar or 2D

    Returns
    -------
    H : Transform matrix

    """
    factor = np.asarray(factor)
    if factor.size == 1:
        H = np.diag([factor, factor, 1.0])
    elif factor.size == 2:
        H = np.diag([factor[0], factor[1], 1.0])
    else:
        raise ValueError('Invalid scale factor: {:s}'.format(factor))

    return H


def shear(angle, direction):
    """
    Build transform to shear by given angle.

    Parameters
    ----------
    angle : Shear angle (radians)
    direction : Shear direction vector

    Returns
    -------
    H : Transform matrix

    Notes
    -----
    This one took me about 20 minutes to figure out the geometry.  It helps to think in 3D to fully
    understand how it works for a 2D problem.  I guess that's why we do everything in Homogeneous
    coordinates, eh?

    The shear plane defines the 2D space where distances between two points are unaffected by the
    shear transform.  For 2D problems the shear plane may be any plane orthogonal to the XY plane.
    This plane is defined by two items: a point in the XY plane and a vector normal to the shear
    plane (also defined in the XY plane).

    A point P in the XY plane is transformed by the shear matrix into P" such that the vector P-P"
    is parallel to the direction vector and the angle is defined by P-P'-P", where P' is the
    orthogonal projection of P onto the shear plane.

    In 2D, it is best to set the reference point to the origin and let the shear normal be computed
    from the supplied parameters.

    """
    tangle = np.tan(angle)
    direction = homogeneous(direction)

    normal = np.asarray([0., 0., 1.])
    # point = np.zeros(3)

    H = np.identity(3)
    H[:2, :2] += tangle * np.outer(direction, normal)
    # H[:2, 2] = -tangle * np.dot(point, normal) * direction

    return H


def perspective(values):
    """
    Build transform containing perspective partition data.

    Parameters
    ----------
    values : vector size 2

    Returns
    -------
    H : Transform matrix

    """

    H = np.identity(3)

    if len(values) == 2:
        H[2, :2] = values
    else:
        raise ValueError('Invalid input values: {}'.format(values))

    # H[3, 3] = values[-1]
    # H /= H[3, 3]
    # H[3, 3] = 1.0

    return H


def shape_match_scale(img_src, img_dst):
    """Helper function for computing similarity transform to make size of source image match
    that of destination image.

    Parameters
    ----------
    img_src : image array, (src_num_rows, src_num_cols, ...) or
              shape tuple, (src_num_rows, src_num_cols, ...)
    img_dst : image array, (dst_num_rows, dst_num_cols, ...) or
              shape tuple, (dst_num_rows, dst_num_cols, ...)

    Returns
    -------
    scale_factors : tuple of x and y scale factgors.

    """
    if issubclass(tuple, type(img_src)):
        height_src, width_src = img_src[:2]
    else:
        height_src, width_src = img_src.shape[:2]

    if issubclass(tuple, type(img_dst)):
        height_dst, width_dst = img_dst[:2]
    else:
        height_dst, width_dst = img_dst.shape[:2]

    height_scl = height_dst / height_src
    width_scl = width_dst / width_src

    return height_scl, width_scl


def shape_match(img_src, img_dst):
    """Compute similarity transform to make size of source image match that of destination image.

    Parameters
    ----------
    img_src : image array, (src_num_rows, src_num_cols, ...) or
              shape tuple, (src_num_rows, src_num_cols, ...)
    img_dst : image array, (dst_num_rows, dst_num_cols, ...) or
              shape tuple, (dst_num_rows, dst_num_cols, ...)

    Returns
    -------
    H : homogeneous transformation matrix, (3, 3)

    """
    height_scl, width_scl = shape_match_scale(img_src, img_dst)

    H = np.asarray([[width_scl, 0., 0.],
                    [0., height_scl, 0.],
                    [0., 0., 1.]], dtype=np.float32)
    return H


def decompose(H):
    """Decompose transform matrix into component parameters.

    Parameters
    ----------
    H : Transform matrix

    Returns
    -------
    scale : Vector of three scale factors
    shear : List of shear factors for x-y, x-z, y-z axes
    angles : List of Euler angles about static x, y, z axes
    translate : Translation vector along x, y, z axes
    perspective : Perspective partition of matrix

    Notes
    -----
    Raise ValueError if matrix is of wrong type or degenerative.

    Decompose does not properely handle case when scaling is NOT along a cardinal axis.  But now
    that I think about it, this case is a combination of rotation and traditional scaling.

    """
    H = homo_in_4d(H)
    scale, shear, angles, translate, perspective = gohlke.transformations.decompose_matrix(H)

    # Sometimes the values coming out are in the form of a list, sometimes as ndarray.  This makes
    # it consistent.
    scale = np.asarray(scale)
    shear = np.asarray(shear)
    angles = np.asarray(angles)
    translate = np.asarray(translate)
    perspective = np.asarray(perspective)

    return scale, shear, angles, translate, perspective


def concatenate(*matrices):
    """Concatenate series of transformation matrices.

    Parameters
    ----------
    matrices : Sequence of (3, 3) and/or (4, 4) transformations.

    Notes
    -----
    if matrices = [H1, H2], then output of this function is the combined transform of applying H1 to
    some data, and then afterwards applying H2 to the output of the previous step.

    Returns
    -------
    H : Concatenation of input transformation matrices, (4, 4)

    """
    H = np.identity(4)
    for Q in matrices:
        Q = homo_in_4d(Q)
        H = Q.dot(H)

    return H


def invert(H, normalize=True):
    """Invert supplied transform matrix.  Normalize output array to unit homography scale
    factor, e.g. H[-1, -1] = 1.0.  Thus, this inverse is not the same as np.linalg.inv().

    Parameters
    ----------
    H : Transform matrix

    Returns
    -------
    H_inv : Inverse of matrix H

    """
    H = np.asarray(H)
    D = H.shape[0]
    H = homo_in_4d(H)

    use_gohlke = False
    if use_gohlke:
        H_inv = gohlke.transformations.inverse_matrix(H)
    else:
        H_inv = np.linalg.inv(H)

    # print('a')
    # print(H_inv)
    if D == 3:
        H_inv = homo_in_3d(H_inv)

    if normalize:
        H_inv /= H_inv[-1, -1]

    return H_inv
