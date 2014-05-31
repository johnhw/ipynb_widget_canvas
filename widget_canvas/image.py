
from __future__ import division, print_function, unicode_literals

import PIL
import PIL.Image
import numpy as np

"""
This is a simple module for reading and writing image data using PIL or Pillow.  Image data is
processed to/from Numpy arrays.  Output file format is determined solely from user-supplied
filename's extension.  No fancy data processing of any kind!!
"""


def read(fname):
    """Read image file, return a Numpy array."""

    img = PIL.Image.open(fname)
    data = np.asarray(img)

    return data


def write(fname, data):
    """Write a Numpy image array to a file."""

    img = PIL.Image.fromarray(data)
    img.save(fname)
