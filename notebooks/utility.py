from __future__ import division, print_function, unicode_literals

import StringIO
import base64

import PIL
import PIL.Image
import numpy as np


"""
I found a few neat PNG tricks here:
https://github.com/minrk/ipython_extensions/blob/master/extensions/retina.py
"""


def pngxy(data):
    """read the width/height from a PNG header"""
    ihdr = data.index(b'IHDR')
    # next 8 bytes are width/height
    w4h4 = data[ihdr+4:ihdr+12]
    return struct.unpack('>ii', w4h4)


def print_figure(fig, fmt='png', dpi=None):
    """Convert a figure to svg or png for inline display."""
    import matplotlib
    fc = fig.get_facecolor()
    ec = fig.get_edgecolor()
    bytes_io = BytesIO()
    dpi = dpi or matplotlib.rcParams['savefig.dpi']
    fig.canvas.print_figure(bytes_io, format=fmt, dpi=dpi,
                            bbox_inches='tight',
                            facecolor=fc, edgecolor=ec,
    )
    data = bytes_io.getvalue()
    return data


def compress_png(data):
    """
    Convert input image data array into a PNG compressed data representation.

    Valid data shapes:
        (rows, columns)    - Greyscale
        (rows, columns, 1) - Greyscale
        (rows, columns, 3) - RGB
        (rows, columns, 4) - RGBA

    If data type is not either np.uint8 or np.int16, then it will be converted by scaling
    min(data) -> 0 and max(data) -> 255.

    Returns a string.
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


def encode_image(data_image):
    """
    Generate HTML src string from image data using Base64 encoding.
        Input image data, if supplied, must be a Numpy array with a shape similar to one of
        the following:
        (rows, columns)    - Greyscale
        (rows, columns, 1) - Greyscale
        (rows, columns, 3) - RGB
        (rows, columns, 4) - RGBA

    If data type is not either np.uint8 or np.int16, then it will be converted by scaling
    min(data) -> 0 and max(data) -> 255 and cast to np.uint8.
    """

    # Compress via PNG.
    data_comp, fmt = compress_png(data_image)

    # Encode via base64.
    data_b64 = base64.b64encode(data_comp)

    # Build src string.
    src = 'data:image/{:s};base64,{:s}'.format(fmt, data_b64)

    return src
