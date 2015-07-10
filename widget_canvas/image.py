
from __future__ import division, print_function, unicode_literals, absolute_import

import base64
import urllib

import numpy as np
import imageio
import requests

"""
This module contains a variety of helper functions for working with image data.
"""


#################################################
# Fetch image data from a URL
def normalize_url(url):
    """
    https://docs.python.org/3.0/library/
    urllib.parse.html#urllib.parse.ParseResult.geturl
    """
    parts = urllib.parse.urlsplit(url)
    url_nice = parts.geturl()

    return url_nice


def download(url, verbose=False):
    """
    Download compressed image data from URL.

    http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests/13137873#13137873
    """
    resp = requests.get(url)
    if not resp.ok:
        msg = 'Problem fetching data: {}'.format(resp.reason)
        raise requests.RequestException(msg)

    # Binary compressed image data from response content.
    data_comp = resp.content

    # Compression format, e.g. 'image/jpeg' --> 'jpeg'
    fmt = resp.headers['content-type'].split('/')[1]

    return data_comp, fmt

#################################################


def determine_mode(data):
    """
    Determine image color mode.
    Input data is expected to be 3D: [num_lines, num_samples, num_bands].
    """
    # Force data to be Numpy ndarray, if not already.
    data = np.asarray(data)

    num_bands = data.shape[2]

    if num_bands == 1:
        mode = 'L'
    elif num_bands == 3:
        mode = 'RGB'
    elif num_bands == 4:
        mode = 'RGBA'
    else:
        raise ValueError('Incorrect number of bands.')

    return mode


def setup_data(data):
    """
    Prepare input image data for compression.

    Valid data shapes:
        (rows, columns)    - Greyscale
        (rows, columns, 1) - Greyscale
        (rows, columns, 3) - RGB
        (rows, columns, 4) - RGBA   note: Not valid for jpeg!!!!

    If data type is either np.uint8, then it will be converted by scaling
    min(data) -> 0 and max(data) -> 255.

    Returns normalized data.
    """
    # Force data to be Numpy ndarray, if not already.
    data = np.asarray(data)

    if data.ndim < 2 or 3 < data.ndim:
        raise ValueError('Image data must have two or three dimensions: {}'.format(data.shape))

    # Force 3D array.
    num_lines, num_samples = data.shape[:2]
    if data.ndim == 2:
        data.shape = num_lines, num_samples, 1

    # Need to change type?
    if not (data.dtype == np.uint8):
        scale = data.max() - data.min()
        if scale == 0:
            raise ValueError('Invalid scale range: {}'.format(scale))

        data = (data.astype(np.float32) - np.min(data)) / scale * 255
        data = data.astype(np.uint8)

    return data


def compress(data, fmt='jpg', **kwargs):
    """
    Convert input image data array into a compressed data representation.

    Valid data shapes:
        (rows, columns)    - Greyscale
        (rows, columns, 1) - Greyscale
        (rows, columns, 3) - RGB
        (rows, columns, 4) - RGBA

    fmt: 'png', 'jpeg', etc.

    Alpha channel will be ignored if fmt == 'jpeg'.

    Returns a string of compressed data.
    """
    # Very easy to compress to a buffer via imageio.
    data_comp = imageio.imwrite(imageio.RETURN_BYTES, data, format=fmt, **kwargs)

    return data_comp


def decompress(data_comp):
    """
    Decompress image from supplied byte data.
    """
    return imageio.imread(data_comp)


def encode(data_comp):
    """
    Apply base64 text encoding to already-compressed image byte data.
    """
    data_encode = base64.b64encode(data_comp)

    return data_encode


def data_url(data_encode, fmt):
    """
    Assemble into URL data string.
    """

    # The decoding step here is necesary since we need to interpret byte data as text.
    # See this link for a nice explanation.
    # http://stackoverflow.com/questions/14010551/how-to-convert-between-bytes-and-strings-in-python-3

    encoding = 'utf-8'
    template = 'data:image/{:s};charset={};base64,{:s}'

    result = template.format(fmt, encoding, data_encode.decode(encoding=encoding))

    return result

#################################################

if __name__ == '__main__':
    pass
