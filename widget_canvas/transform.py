
from __future__ import division, print_function, unicode_literals

import math

"""
This is a simple class for keeping track of the current transformation matrix.
self.Python implementation was inspired by the JavaScript implementation
by Simon Sarris: https://github.com/simonsarris/Canvas-tutorials/blob/master/transform.js
"""


class Transform(object):
    """
    This is a simple class for manipulating and keeping track of a transformation matrix.
    """
    def __init__(self, values=None):
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
        http://www.whatwg.org/specs/web-apps/current-work/multipage/the-canvas-element.html#transformations

        Different browser API implementation may swap m12 with m21.  See the Note mentioned in the
        linked description.

        Initialize self if optional values are supplied.
        """
        self.m11 = 0
        self.m12 = 0
        self.m13 = 0
        self.m21 = 0
        self.m22 = 0
        self.m23 = 0

        self.reset()
        if values:
            self.values = values

    def __repr__(self):
        """
        Set transform to supplied values, M = [m11, m12, m21, m22, m13, m23].
        """
        template = '{:6.2f} {:6.2f} {:6.2f}\n{:6.2f} {:6.2f} {:6.2f}\n'
        result = template.format(self.m11, self.m12, self.m13,
                                 self.m21, self.m22, self.m23)
        return result

    def _repr_latex_(self):
        template = """
                \\begin{{equation*}}
                M = \\begin{{vmatrix}} {:6.2f} & {:6.2f} & {:6.2f} \\\\
                                       {:6.2f} & {:6.2f} & {:6.2f} \\end{{vmatrix}}
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
        """Set new vales for transform, values_new = [m11, m12, m21, m22, m13, m23].
        """
        if len(values_new) != 6:
            raise ValueError('New values must be size six: {:d}'.format(len(values_new)))

        self.m11, self.m12, self.m21, self.m22, self.m13, self.m23 = values_new

    def reset(self):
        """Reset self to identity transform.
        """
        self.m11, self.m12, self.m13, self.m12, self.m22, self.m23 = 1, 0, 0, 0, 1, 0

        return self

    def copy(self):
        """Return independent copy of self.
        """
        Q = Transform()
        Q.values = self.values

        return Q

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

        return P

    def invert(self):
        """Invert self.
        """
        d = 1. / (self.m11*self.m22 - self.m12*self.m21)

        m11 =  self.m22*d
        m12 = -self.m12*d
        m21 = -self.m21*d
        m22 =  self.m11*d
        m13 = d*(self.m21*self.m23 - self.m22*self.m13)
        m23 = d*(self.m12*self.m13 - self.m11*self.m23)

        self.m11 = m11
        self.m12 = m12
        self.m13 = m13
        self.m21 = m21
        self.m22 = m22
        self.m23 = m23

        return self

    def rotate(self, rad):
        """Rotate self about origin.
        """
        c = math.cos(rad)
        s = math.sin(rad)

        m11 =  self.m11*c + self.m21*s
        m12 =  self.m12*c + self.m22*s
        m21 = -self.m11*s + self.m21*c
        m22 = -self.m12*s + self.m22*c

        self.m11 = m11
        self.m12 = m12
#         self.m13 = m13
        self.m21 = m21
        self.m22 = m22
#         self.m23 = m23

        return self

    def translate(self, dx, dy):
        """Offset self.
        """
        self.m13 -= self.m11*dx + self.m21*dy
        self.m23 -= self.m12*dx + self.m22*dy

        return self

    def scale(self, sx, sy=None):
        """Apply X,Y scale factors to self.
        """
        if not sy:
            sy = sx

        self.m11 *= sx
        self.m12 *= sx
        self.m21 *= sy
        self.m22 *= sy

        return self

    def transform_point(self, px, py=None):
        """Apply own transform to supplied X,Y data point.

        M = [m11, m12, m21, m22, m13, m23]
              0    1    2    3    4    5
        """
        if not py:
            px, py = px
        qx = px*self.m11 + py*self.m21 + self.m13
        qy = px*self.m12 + py*self.m22 + self.m23

        return qx, qy
