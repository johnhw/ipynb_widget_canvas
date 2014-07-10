
from __future__ import division, print_function, unicode_literals

import numpy as np

"""
This is a simple class for keeping track of the current transformation matrix.
self.Python implementation was inspired by the JavaScript implementation
by Simon Sarris: https://github.com/simonsarris/Canvas-tutorials/blob/master/transform.js
"""


class Transform(object):
    """
    This is a simple class for manipulating and keeping track of a transformation matrix.
    """
    def __init__(self, values=None, auto_notify=False, notify_callback=None):
        """
        Create a new instance of a Transform.
        Defined by a sequence of six numbers from the elements
        of the matrix M = [m11, m12, m21, m22, m13, m23] that represent
        a square matrix of the form: M = [m11, m12, m13,
                                          m21, m22, m23,
                                          0.0, 0.0, 1.0]

        These values are stored internally as a sequence in a form directly compatible with
        the HTML5 Canvas Element's Context method setTransform().  The internal flattened
        representation is given by the sequence: M = [m11, m12, m21, m22, m13, m23]

        See link for details:
        http://www.whatwg.org/specs/web-apps/current-work/multipage/the-canvas-element.html

        Different browser API implementation may swap m12 with m21.  See the Note mentioned in the
        linked description.

        Initialize self if optional values are supplied.

        Optional callback function to be called when transform values are updated.
        """
        self.notify_callback = notify_callback
        self.auto_notify = auto_notify

        if values:
            self.values = values
        else:
            self.reset()

        self.values_old = self.values

    def __repr__(self):
        """
        Set transform to supplied values, M = [m11, m12, m21, m22, m13, m23].
        """
        template = '{:6.2f} {:6.2f} {:6.2f}\n{:6.2f} {:6.2f} {:6.2f}\n'
        result = template.format(self.m11, self.m12, self.m13,
                                 self.m21, self.m22, self.m23)
        return result

    def _repr_latex_(self):
        """
        Pretty self-representation using IPython Notebook display system.
        """
        template = """
                \\begin{{equation*}}
                M = \\begin{{vmatrix}} {:7.3f} & {:7.3f} & {:7.3f} \\\\
                                       {:7.3f} & {:7.3f} & {:7.3f} \\end{{vmatrix}}
                \\end{{equation*}}
                """

        result = template.format(self.m11, self.m12, self.m13,
                                 self.m21, self.m22, self.m23)
        return result

    ####################################################3

    @property
    def values(self):
        """Current transform, M = [m11, m12, m21, m22, m13, m23].
        """
        return self.m11, self.m12, self.m21, self.m22, self.m13, self.m23

    @values.setter
    def values(self, values_new):
        """Set new vales for transform.  Can supply either 2, 4 or 6 values.

        values_new = [m13, m22], or
        values_new = [m11, m12, m21, m22], or
        values_new = [m11, m12, m21, m22, m13, m23]
        """
        values_old = self.values

        N = len(values_new)
        if N == 6:
            # Replace all six terms.
            self.m11, self.m12, self.m21, self.m22, self.m13, self.m23 = values_new
        elif N == 4:
            # Replace scale and shear terms, exclude offset terms.
            self.m11, self.m12, self.m21, self.m22 = values_new
        elif N == 2:
            # Replace offset terms only.
            self.m13, self.m23 = values_new
        else:
            raise ValueError('New values must be size two, four or six: {:d}'.format(N))

        self.values_old = values_old

        if self.auto_notify:
            self.notify()

    def reset(self):
        """Reset self to identity transform.
        """
        self.m11, self.m12, self.m21, self.m22, self.m13, self.m23 = 1, 0, 0, 1, 0, 0

        return self

    def copy(self):
        """Return independent copy of self.
        """
        Q = Transform(self.values)

        return Q

    def notify(self):
        """Call user-supplied callback function with updated transform state values.
        """
        # Only do something if values have changed and callback function is defined.
        if self.values != self.values_old and self.notify_callback:
            self.notify_callback(self.values)

    #############################################

    def _matrix_multiply(self, Q):
        """Apply supplied transform(s) to copy of self.
        """
        if not isinstance(Q, type(self)):
            raise ValueError('Supplied value must be a Transform instance: {}'.format(Q))

        m11 = self.m11*Q.m11 + self.m21*Q.m12
        m12 = self.m12*Q.m11 + self.m22*Q.m12

        m21 = self.m11*Q.m21 + self.m21*Q.m22
        m22 = self.m12*Q.m21 + self.m22*Q.m22

        m13 = self.m11*Q.m13 + self.m21*Q.m23 + self.m13
        m23 = self.m12*Q.m13 + self.m22*Q.m23 + self.m23

        P = Transform([m11, m12, m21, m22, m13, m23])

        return P

    def multiply(self, *args):
        """Apply supplied transform(s) to copy of self.
        """
        P = self.copy()
        for Q in args:
            P = P._matrix_multiply(Q)
            # P = Q._matrix_multiply(P)  # ???

        return P

    def invert(self, copy=False):
        """Invert self.
        """
        d = 1. / (self.m11*self.m22 - self.m12*self.m21)

        m11 = self.m22*d
        m12 = -self.m12*d
        m21 = -self.m21*d
        m22 = self.m11*d
        m13 = d*(self.m21*self.m23 - self.m22*self.m13)
        m23 = d*(self.m12*self.m13 - self.m11*self.m23)

        values = m11, m12, m21, m22, m13, m23

        if copy:
            # Return inverse transform as independent copy.
            Q = Transform(values)
        else:
            # Return self with inverse applied.
            self.values = values
            Q = self

        return Q

    def rotate(self, rad):
        """Rotate self about origin.
        """
        print('r')
        c = np.cos(rad)
        s = np.sin(rad)

        m11 = self.m11*c + self.m21*s
        m12 = self.m12*c + self.m22*s
        m21 = -self.m11*s + self.m21*c
        m22 = -self.m12*s + self.m22*c

        self.values = m11, m12, m21, m22

        return self

    def scale(self, sx, sy=None):
        """Apply X,Y scale factors to self.
        """
        print('s')
        if not sy:
            sy = sx

        m11 = self.m11 * sx
        m12 = self.m12 * sx
        m21 = self.m21 * sy
        m22 = self.m22 * sy

        self.values = m11, m12, m21, m22

        return self

    def translate(self, dx, dy):
        """Offset self.
        """
        delta_13 = self.m11*dx + self.m21*dy
        delta_23 = self.m12*dx + self.m22*dy

        # Translate relative to current position.
        m13 = self.m13 + delta_13
        m23 = self.m23 + delta_23

        self.values = m13, m23

        return self

    def is_singular(self):
        value_test = self.m11*self.m22 - self.m12*self.m21

        eps = 1.e-6
        if abs(value_test) <= eps:
            return True
        else:
            return False

    def decompose(self):
        """
        Decompose transform matrix into discrete components.

        M = [m11, m12, m21, m22, m13, m23]
              0    1    2    3    4    5
              A    C    B    D

        float A = aMatrix.xx,
              B = aMatrix.yx,
              C = aMatrix.xy,
              D = aMatrix.yy;
        """

        if self.is_singular():
            raise ValueError('Singular matrix.')

        # Working copy of current transform values.
        m11, m12, m21, m22, m13, m23 = self.values

        scale_x = (m11**2 + m21**2)**.5
        m11 /= scale_x
        m21 /= scale_x

        shear = m11*m12 + m21*m22
        m12 -= m11*shear
        m22 -= m21*shear

        scale_y = (m12**2 + m22**2)**.5
        m12 /= scale_y
        m22 /= scale_y
        shear /= scale_y

        scale = scale_x, scale_y

        # m11*m22 - m21*m12 should now be 1 or -1
        value_test = m11*m22 - m21*m12
        eps = 1.e-6
        if abs(value_test - 1) > eps:
            raise ValueError('Invalid determinant: {:f}'.format(value_test))

        if m11*m22 < m21*m12:
            # Flip signs.
            m11 = -m11
            m21 = -m21
            m12 = -m12
            m22 = -m22
            shear = -shear
            scale_x = -scale_x

        # Angle of rotation.
        rotation = np.arctan2(m21, m11)

        # Offsets.
        offset = m13, m23

        return scale, shear, rotation, offset

    def transform_point(self, px, py):
        """Apply own transform to supplied X,Y data point.

        M = [m11, m12, m21, m22, m13, m23]
              0    1    2    3    4    5
        """
        # if not py:
        #     px, py = px
        qx = px*self.m11 + py*self.m21 + self.m13
        qy = px*self.m12 + py*self.m22 + self.m23

        return qx, qy
