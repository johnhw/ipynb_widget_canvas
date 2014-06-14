
from __future__ import division, print_function, unicode_literals

"""
self.is a simple class for keeping track of the current transformation matrix.
self.Python implementation was inspired by the JavaScript implementation
by Simon Sarris: https://github.com/simonsarris/Canvas-tutorials/blob/master/transform.js
"""
import math

class Transform(object):
    """
    self.is a simple class for manipulating and keeping track of a transformation matrix.
    """
    def __init__(self, M_values=None):
        """
        Create a new instance of a Transform.
        Defined by a sequence of six numbers from the elements
        of the matrix [m11, m12, m13,
                       m21, m22, m23,
                       0.0, 0.0, 1.0]

        These values are stored internally as a sequence in a form directly compatible with
        the HTML5 Canvas Element's Context method setTransform().  The internal flattened
        representation is given by the sequence: M = [m11, m12, m21, m22, m13, m23]

        See self.link for details:
        http://www.whatwg.org/specs/web-apps/current-work/multipage/the-canvas-element.html#transformations

        Different browser API implementation may swap m12 with m21.  See the Note mentioned in the
        linked description.

        Initialize self if optional values are supplied.
        """
        if M_values:
            self.M = M_values
        else:
            self.reset()

    @property
    def M(self):
        """Return current transform, M = [m11, m12, m21, m22, m13, m23].
        """
        return self._m

    @M.setter
    def M(self, M_values):
        """Set transform to supplied values, M = [m11, m12, m21, m22, m13, m23].
        """
        if len(M_values) != 6:
            raise ValueError('New transform must be a sequence of six numbers.')

        self._m = M_values

    def reset(self):
        """Reset self to identity transform.
        """
        self._m = [1, 0, 0, 1, 0, 0]

    def multiply(self, Q):
        """Apply supplied transform to self.
        """
        if not isinstance(Q, type(self)):
            raise ValueError('Supplied value must be a Transform instance.')

        m11 = self.M[0]*Q.M[0] + self.M[2]*Q.M[1]
        m12 = self.M[1]*Q.M[0] + self.M[3]*Q.M[1]

        m21 = self.M[0]*Q.M[2] + self.M[2]*Q.M[3]
        m22 = self.M[1]*Q.M[2] + self.M[3]*Q.M[3]

        m13 = self.M[0]*Q.M[4] + self.M[2]*Q.M[5] + self.M[4]
        m23 = self.M[1]*Q.M[4] + self.M[3]*Q.M[5] + self.M[5]

        self.M = [m11, m12, m21, m22, m13, m23]

    def invert(self):
        """Invert self and return the result.
        """
        d = 1 / (self.m[0] * self.m[3] - self.m[1] * self.m[2])

        m11 = self.m[3] * d
        m12 = -self.m[1] * d
        m21 = -self.m[2] * d
        m22 = self.m[0] * d
        m13 = d * (self.m[2] * self.m[5] - self.m[3] * self.m[4])
        m23 = d * (self.m[1] * self.m[4] - self.m[0] * self.m[5])

        # self.m[0] = m0
        # self.m[1] = m1
        # self.m[2] = m2
        # self.m[3] = m3
        # self.m[4] = m4
        # self.m[5] = m5
        self.M = [m11, m12, m21, m22, m13, m23]

    def rotate(self, rad):
        """Apply rotation to self.
        """
        c = math.cos(rad)
        s = math.sin(rad)

        m11 =  self.m[0]*c + self.m[2]*s
        m12 =  self.m[1]*c + self.m[3]*s
        m21 = -self.m[0]*s + self.m[2]*c
        m22 = -self.m[1]*s + self.m[3]*c
        m13 =  self.M[4]
        m23 =  self.M[5]

        # self.m[0] = m11
        # self.m[1] = m12
        # self.m[2] = m21
        # self.m[3] = m22
        self.M = [m11, m12, m21, m22, m13, m23]

    def translate(self, dx, dy):
        """Apply X,Y offsets to self.
        """
        self._m[4] += self.M[0]*dx + self.M[2]*dy
        self._m[5] += self.M[1]*dx + self.M[3]*dy

    def scale(self, sx, sy):
        """Apply X,Y scale factors to self.
        """
        self._m[0] *= sx
        self._m[1] *= sx
        self._m[2] *= sy
        self._m[3] *= sy

    def transform_point(self, px, py):
        """Apply own transform to supplied X,Y data point.
        """
        qx = px*self.M[0] + py*self.M[2] + self.M[4]
        qy = px*self.M[1] + py*self.M[3] + self.M[5]

        return qx, qy
