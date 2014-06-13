
from __future__ import division, print_function, unicode_literals

"""
This is a simple class for keeping track of the current transformation matrix.
This Python implementation was inspired by the JavaScript implementation
by Simon Sarris: https://github.com/simonsarris/Canvas-tutorials/blob/master/transform.js
"""


class Transform(object):
    """
    This is a simple class for manipulating and keeping track of a transformation matrix.
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

        See this link for details:
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
  var d = 1 / (this.m[0] * this.m[3] - this.m[1] * this.m[2]);
  var m0 = this.m[3] * d;
  var m1 = -this.m[1] * d;
  var m2 = -this.m[2] * d;
  var m3 = this.m[0] * d;
  var m4 = d * (this.m[2] * this.m[5] - this.m[3] * this.m[4]);
  var m5 = d * (this.m[1] * this.m[4] - this.m[0] * this.m[5]);
  this.m[0] = m0;
  this.m[1] = m1;
  this.m[2] = m2;
  this.m[3] = m3;
  this.m[4] = m4;
  this.m[5] = m5;

        def rotate(self, rad):
            """Apply rotation to self.
            """

  var c = Math.cos(rad);
  var s = Math.sin(rad);
  var m11 = this.m[0] * c + this.m[2] * s;
  var m12 = this.m[1] * c + this.m[3] * s;
  var m21 = this.m[0] * -s + this.m[2] * c;
  var m22 = this.m[1] * -s + this.m[3] * c;
  this.m[0] = m11;
  this.m[1] = m12;
  this.m[2] = m21;
  this.m[3] = m22;

        def translate(self, dx, dy):
            """Apply X,Y offsets to self.
            """
  this.m[4] += this.m[0] * x + this.m[2] * y;
  this.m[5] += this.m[1] * x + this.m[3] * y;

        def scale(self, sx, sy):
            """Apply X,Y scale factors to self.
            """
  this.m[0] *= sx;
  this.m[1] *= sx;
  this.m[2] *= sy;
  this.m[3] *= sy;

        def transform_point(self, px, py):
            """Apply own transform to supplied X,Y data point.
            """
  var x = px;
  var y = py;
  px = x * this.m[0] + y * this.m[2] + this.m[4];
  py = x * this.m[1] + y * this.m[3] + this.m[5];
  return [px, py];
