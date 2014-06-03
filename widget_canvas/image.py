
from __future__ import division, print_function, unicode_literals

import StringIO
import base64
import struct

import PIL
import PIL.Image
import numpy as np

"""
This module contains helper fnctions for working with image data.
"""


# Reading and writing image data using PIL or Pillow.  Image data is
# processed to/from Numpy arrays.  Output file format is determined solely from user-supplied
# filename's extension.  No fancy data processing of any kind!!
def read(fname):
    """Read image file, return a Numpy array."""
    img = PIL.Image.open(fname)
    data = np.asarray(img)

    return data


def write(fname, data):
    """Write a Numpy image array to a file."""

    img = PIL.Image.fromarray(data)
    img.save(fname)


def png_xy(blob_str):
    """
    Read the width/height from a PNG header
    https://github.com/minrk/ipython_extensions/blob/master/extensions/retina.py
    """
    ix = blob_str.index(b'IHDR')

    # Next 8 bytes are width and height
    w4h4 = blob_str[ix + 4:ix + 12]
    width, height = struct.unpack('>ii', w4h4)

    return width, height


def png_compress(data):
    """
    Convert input image data array into a PNG compressed data representation.

    Valid data shapes:
        (rows, columns)    - Greyscale
        (rows, columns, 1) - Greyscale
        (rows, columns, 3) - RGB
        (rows, columns, 4) - RGBA

    If data type is not either np.uint8 or np.int16, then it will be converted by scaling
    min(data) -> 0 and max(data) -> 255.

    Returns a string of compressed data.
    """

    # Force data to be Numpy ndarray, if not already.
    data = np.asarray(data)

    if data.ndim < 2 or 3 < data.ndim:
        raise ValueError('Image data must have two or three dimensions: {}'.format(data.shape))

    # Force 3D array.
    num_lines, num_samples = data.shape[:2]
    if data.ndim == 2:
        data.shape = num_lines, num_samples, 1

    num_bands = data.shape[2]

    # Need to change type?
    # if not (data.dtype == np.uint8 or data.dtype == np.uint16):
    if not (data.dtype == np.uint8):
        scale = data.max() - data.min()
        if scale == 0:
            raise ValueError('scale is 0')

        data = (data.astype(np.float32) - np.min(data)) / scale * 255
        data = data.astype(np.uint8)

    # Number of bands.
    if num_bands == 1:
        mode = 'L'
    elif num_bands == 3:
        mode = 'RGB'
    elif num_bands == 4:
        mode = 'RGBA'
    else:
        raise ValueError('Incorrect number of bands.')

    # Use Pillow to compress to PNG format.
    # http://pillow.readthedocs.org/en/latest/reference/Image.html#PIL.Image.fromarray
    img = PIL.Image.fromarray(data, mode)

    # http://pillow.readthedocs.org/en/latest/reference/Image.html#PIL.Image.Image.save
    # http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html?highlight=png#png
    buf = StringIO.StringIO()
    img.save(buf, format='png', optimize=False)
    results = buf.getvalue()

    fmt = 'png'

    return results, fmt
