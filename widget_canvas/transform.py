
from __future__ import division, print_function, unicode_literals

"""
This is a simple class for keeping track of the current transformation matrix.
self.Python implementation was inspired by the JavaScript implementation
by Simon Sarris: https://github.com/simonsarris/Canvas-tutorials/blob/master/transform.js
"""
import math


class Transform(object):
    """
    This is a simple class for manipulating and keeping track of a transformation matrix.
    """
    def __init__(self, values=None):
        """
        Create a new instance of a Transform.
        Defined by a sequence of six numbers from the elements
        of the matrix [m11, m12, m13,
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
        self.reset()
        if values:
            self.values = values

    def __repr__(self):
        """
        Set transform to supplied values, M = [m11, m12, m21, m22, m13, m23].
        """
        return '{0:6.2f} {1:6.2f} {4:6.2f}\n{2:6.2f} {3:6.2f} {5:6.2f}\n'.format(self[0], self[1], self[2],
                                                                           self[3], self[4], self[5])

    ####################################################3

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        if type(key) is not int:
            raise ValueError('Index type must be int. Received: {}'.format(type(key)))

        if not (0 <= key <= 5):
            raise ValueError('Index must be between 0 and 5: {:d}'.format(key))

        self._values[key] = value

    def __iter__(self):
        return self._values.__iter__()

    def __contains__(self, value):
        return value in self._values

    def iterkeys(self):
        return self.__iter__()

    @property
    def values(self):
        """Current transform, M = [m11, m12, m21, m22, m13, m23].
        """
        return self._values

    def reset(self):
        """Reset self to identity transform.
        """
        self._values = [1, 0, 0, 1, 0, 0]

    def multiply(self, Q):
        """Apply supplied transform to self.
        """
        if not isinstance(Q, type(self)):
            raise ValueError('Supplied value must be a Transform instance.')

        m11 = self[0]*Q[0] + self[2]*Q[1]
        m12 = self[1]*Q[0] + self[3]*Q[1]

        m21 = self[0]*Q[2] + self[2]*Q[3]
        m22 = self[1]*Q[2] + self[3]*Q[3]

        m13 = self[0]*Q[4] + self[2]*Q[5] + self[4]
        m23 = self[1]*Q[4] + self[3]*Q[5] + self[5]

        for k, v in enumerate([m11, m12, m21, m22, m13, m23]):
            self[k] = v

    def invert(self):
        """Invert self.
        """
        d = 1. / (self[0]*self[3] - self[1]*self[2])

        m11 =  self[3]*d
        m12 = -self[1]*d
        m21 = -self[2]*d
        m22 =  self[0]*d
        m13 = d*(self[2]*self[5] - self[3]*self[4])
        m23 = d*(self[1]*self[4] - self[0]*self[5])

        for k, v in enumerate([m11, m12, m21, m22, m13, m23]):
            self[k] = v

    def rotate(self, rad):
        """Apply rotation to self.
        """
        c = math.cos(rad)
        s = math.sin(rad)

        m11 =  self[0]*c + self[2]*s
        m12 =  self[1]*c + self[3]*s
        m21 = -self[0]*s + self[2]*c
        m22 = -self[1]*s + self[3]*c

        for k, v in enumerate([m11, m12, m21, m22]):
            self[k] = v

    def translate(self, dx, dy):
        """Apply X,Y offsets to self.
        """
        self[4] += self[0]*dx + self[2]*dy
        self[5] += self[1]*dx + self[3]*dy

    def scale(self, sx, sy=None):
        """Apply X,Y scale factors to self.
        """
        if not sy:
            sy = sx

        self[0] *= sx
        self[1] *= sx
        self[2] *= sy
        self[3] *= sy

    def transform_point(self, px, py):
        """Apply own transform to supplied X,Y data point.
        """
        qx = px*self.values[0] + py*self.values[2] + self.values[4]
        qy = px*self.values[1] + py*self.values[3] + self.values[5]

        return qx, qy
