def decompose(H):
    """
    Decompose general transform matrix into elemental transforms.

    Parameters
    ----------
    H : Transform matrix

    Returns
    -------
    H_scale, H_shear, H_rorate, H_translate, H_perspective

    Notes
    -----
    See this paper for details:

    "Projective Transformations for Image Transition Animations"

    Section 3.1 using QR decomposition, Google Docs PDF: http://goo.gl/Ohd5bA

    Homography matrix:

        | h_11  h_12  h_13 |
    H = | h_21  h_22  h_23 |
        | h_31  h_32  h_33 |

    """

    # Perspective.
    H_perspective = np.identity(3)
    H_perspective[2] = H[2]

    # Translation.
    H_translate = np.identity(3)
    H_translate[:, 2] = H[:, 2]

    # Non-homogeneous affine transform (scale, rotate, shear).
    A = H[:2, :2]

    # http://docs.scipy.org/doc/scipy/reference/tutorial/linalg.html#singular-value-decomposition
    U, s, Vh = sp.linalg.svd(A)

    m, n = A.shape
    D = sp.linalg.diagsvd(s, m, n)

    # Scale.
    H_scale = np.identity(3)
    H_scale[:2, :2] = D

    # Shear.

    # Rotate.

    return U, D, Vh


# Perspective.
H_perspective = np.identity(3)
H_perspective[2] = H[2]

# Translation.
H_translate = np.identity(3)
H_translate[:, 2] = H[:, 2]

# Non-homogeneous affine transform (scale, rotate, shear).
A = H[:2, :2]

# http://docs.scipy.org/doc/scipy/reference/tutorial/linalg.html#singular-value-decomposition
U, s, Vh = sp.linalg.svd(A)

m, n = A.shape
D = sp.linalg.diagsvd(s, m, n)

# Scale.
H_scale = np.identity(3)
H_scale[:2, :2] = D

# Rotation.
H_rotate = np.identity(3)

# Shear.
H_shear = np.identity(3)


print('\nPerspective:  {}, {}'.format(pa, pb))
print('{}'.format(H_perspective))

print('\nScale: {}, {}'.format(scale[0], scale[1]))
print('{}'.format(H_scale))

print('\nShear: {}, {:.3f} [{}]'.format(s_factor, s_angle, np.rad2deg(s_angle)))
print('{}'.format(H_shear))

print('\nRotation: {:.3f} [{}]'.format(r_angle, np.rad2deg(r_angle)))
print('{}'.format(H_rotate))

print('\nTranslate: {}, {}'.format(offset[0], offset[1]))
print('{}'.format(H_translate))
