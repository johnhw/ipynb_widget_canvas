# -*- coding: utf-8 -*-
# transformations.py

# Copyright (c) 2006-2014, Christoph Gohlke
# Copyright (c) 2006-2014, The Regents of the University of California
# Produced at the Laboratory for Fluorescence Dynamics
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the copyright holders nor the names of any
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


from __future__ import division, print_function

import math
import numpy as np



"""
See this paper:
Projective Transformations for Image Transition Animations

Setion 3.1  using QR decomposition


"""
def decompose_matrix_3D(matrix):
    """Return sequence of transformations from transformation matrix.
    """
    M = np.array(matrix, dtype=np.float64, copy=True).T
    if abs(M[3, 3]) < _EPS:
        raise ValueError("M[3, 3] is zero")
    M /= M[3, 3]
    P = M.copy()
    P[:, 3] = 0.0, 0.0, 0.0, 1.0
    if not np.linalg.det(P):
        raise ValueError("matrix is singular")

    scale = np.zeros((3, ))
    shear = [0.0, 0.0, 0.0]
    angles = [0.0, 0.0, 0.0]

    if any(abs(M[:3, 3]) > _EPS):
        perspective = np.dot(M[:, 3], np.linalg.inv(P.T))
        M[:, 3] = 0.0, 0.0, 0.0, 1.0
    else:
        perspective = np.array([0.0, 0.0, 0.0, 1.0])

    translate = M[3, :3].copy()
    M[3, :3] = 0.0

    row = M[:3, :3].copy()
    scale[0] = vector_norm(row[0])
    row[0] /= scale[0]
    shear[0] = np.dot(row[0], row[1])
    row[1] -= row[0] * shear[0]
    scale[1] = vector_norm(row[1])
    row[1] /= scale[1]
    shear[0] /= scale[1]
    shear[1] = np.dot(row[0], row[2])
    row[2] -= row[0] * shear[1]
    shear[2] = np.dot(row[1], row[2])
    row[2] -= row[1] * shear[2]
    scale[2] = vector_norm(row[2])
    row[2] /= scale[2]
    shear[1:] /= scale[2]

    if np.dot(row[0], np.cross(row[1], row[2])) < 0:
        np.negative(scale, scale)
        np.negative(row, row)

    angles[1] = math.asin(-row[0, 2])
    if math.cos(angles[1]):
        angles[0] = math.atan2(row[1, 2], row[2, 2])
        angles[2] = math.atan2(row[0, 1], row[0, 0])
    else:
        #angles[0] = math.atan2(row[1, 0], row[1, 1])
        angles[0] = math.atan2(-row[2, 1], row[1, 1])
        angles[2] = 0.0

    return scale, shear, angles, translate, perspective


def decompose_matrix_2D(matrix):
    """Return sequence of transformations from transformation matrix.
    """
    M = np.array(matrix, dtype=np.float64, copy=True).T
    if abs(M[2, 2]) < _EPS:
        raise ValueError("M[2, 2] is zero")

    M /= M[2, 2]
    P = M.copy()
    P[:, 2] = 0.0, 0.0, 1.0

    if not np.linalg.det(P):
        raise ValueError("matrix is singular")

    scale = np.zeros((2, ))
    shear = np.asarray([0.0, 0.0])
    # angles = [0.0, 0.0]

    if any(abs(M[:2, 2]) > _EPS):
        perspective = np.dot(M[:, 2], np.linalg.inv(P.T))
        perspective = perspective[:2]
        M[:, 2] = 0.0, 0.0, 1.0
    else:
        perspective = np.array([0.0, 0.0])

    translate = M[2, :2].copy()
    M[2, :2] = 0.0

    row = M[:2, :2].copy()
    scale[0] = vector_norm(row[0])
    row[0] /= scale[0]
    shear[0] = np.dot(row[0], row[1])
    row[1] -= row[0] * shear[0]
    scale[1] = vector_norm(row[1])
    row[1] /= scale[1]
    shear[0] /= scale[1]
    # shear[1] = np.dot(row[0], row[2])
    # row[2] -= row[0] * shear[1]
    # shear[2] = np.dot(row[1], row[2])
    # row[2] -= row[1] * shear[2]
    # scale[2] = vector_norm(row[2])
    # row[2] /= scale[2]
    # shear[1:] /= scale[2]

    # if np.dot(row[0], np.cross(row[1], row[2])) < 0:
    #     np.negative(scale, scale)
    #     np.negative(row, row)

    angle = math.atan2(row[0, 1], row[0, 0])

    # angles[1] = math.asin(-row[0, 2])
    # if math.cos(angles[1]):
    #     angles[0] = math.atan2(row[1, 2], row[2, 2])
    #     angles[2] = math.atan2(row[0, 1], row[0, 0])
    # else:
    #     #angles[0] = math.atan2(row[1, 0], row[1, 1])
    #     angles[0] = math.atan2(-row[2, 1], row[1, 1])
    #     angles[2] = 0.0

    return scale, shear, angle, translate, perspective

#################################################

# epsilon for testing whether a number is close to zero
_EPS = np.finfo(float).eps * 4.0


def vector_norm(data, axis=None, out=None):
    """
    Return length, i.e. Euclidean norm, of array along axis.
    """
    data = np.array(data, dtype=np.float64, copy=True)

    if out is None:
        if data.ndim == 1:
            return math.sqrt(np.dot(data, data))

        data *= data
        out = np.atleast_1d(np.sum(data, axis=axis))

        np.sqrt(out, out)

        return out
    else:
        data *= data
        np.sum(data, axis=axis, out=out)
        np.sqrt(out, out)


if __name__ == '__main__':
    pass
