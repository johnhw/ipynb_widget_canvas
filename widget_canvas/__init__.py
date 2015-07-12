
from __future__ import division, print_function, unicode_literals, absolute_import

from warnings import filterwarnings
filterwarnings('ignore', module='IPython.html.widgets')

from .widget_canvas import CanvasImage

__all__ = ['CanvasImage']
