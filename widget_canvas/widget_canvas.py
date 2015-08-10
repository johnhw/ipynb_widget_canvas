
from __future__ import division, print_function, unicode_literals, absolute_import

from warnings import filterwarnings
filterwarnings('ignore', module='IPython.html.widgets')

import numpy as np

import IPython
from IPython.html import widgets
from IPython.utils import traitlets

from . import image

#################################################


class CanvasImage(widgets.widget.DOMWidget):
    """
    Display images using HTML5 Canvas with IPython Notebook widget system. Input image data, if
    supplied, must be a Numpy array (or equivalent) with a shape similar to one of the following:
        (rows, columns)    - Greyscale
        (rows, columns, 1) - Greyscale
        (rows, columns, 3) - RGB
        (rows, columns, 4) - RGBA

    If data type is not np.uint8, it will be cast to uint8 by
    mapping min(data) -> 0 and max(data) -> 255.
    """
    # _model_name:   Name of Backbone model registered in the front-end to create and sync with.
    # _model_module: A requirejs module name in which to find _model_name.
    # _view_name:    Default view registered in the front-end to use to represent the widget.
    # _view_module:  A requirejs module in which to find _view_name.

    _view_name = traitlets.Unicode('CanvasImageView', sync=True)
    _view_module = traitlets.Unicode('nbextensions/widget_canvas/widget_canvas', sync=True)
    # _model_name = traitlets.Unicode('CanvasImageModel', sync=True)
    # _model_module = traitlets.Unicode('nbextensions/widget_canvas/widget_canvas', sync=True)

    # Encoded image data.
    _encoded = traitlets.Bytes(help='Encoded image data', sync=True)
    _format = traitlets.Unicode(help='Image encoding format', sync=True)

    # Canvas rendering parameters
    # https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/imageSmoothingEnabled
    smoothing = traitlets.Bool(True, help='Enable/disable image smoothing', sync=True)

    # HTML/CSS display width and height
    width = traitlets.CInt(help='widget width', sync=True)
    height = traitlets.CInt(help='widget height', sync=True)

    # Canvas width and height, mapped later to image width and height.
    _canvas_width = traitlets.CInt(help='canvas width', sync=True)
    _canvas_height = traitlets.CInt(help='canvas height', sync=True)
    # _data_width = traitlets.CInt(help='data width', sync=True)   # work in progress...
    # _data_height = traitlets.CInt(help='data height', sync=True)

    # Mouse event information
    _mouse_event = traitlets.Dict(help='Front-end mouse event information', sync=True)

    def __init__(self, data=None, url=None, format='webp', quality=70, **kwargs):
        """
        Instantiate a new Image Widget object.

        Display images using HTML5 Canvas with IPython Notebook widget system. Keyword `value`
        contains the input image data.  It must be a Numpy array (or equivalent) with a shape
        similar to one of the following:
            (rows, columns)    - Greyscale
            (rows, columns, 1) - Greyscale
            (rows, columns, 3) - RGB
            (rows, columns, 4) - RGBA

        If data type is neither of np.uint8 or np.int16, it will be cast to uint8 by mapping
        min(data) -> 0 and max(data) -> 255.

        If you supply a URL to an image this will override any other parameters.
        """
        super(CanvasImage, self).__init__(**kwargs)

        # Internal Python handler for JS mouse events synced through _mouse_event traitlet.
        # https://developer.mozilla.org/en-US/docs/Web/Reference/Events
        # https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent
        self.on_trait_change(self._handle_mouse, str('_mouse_event'))  # JS --> Python

        # Allow user to attach Python callback functions in response to mousevents.
        self._mouse_event_dispatchers = {}  # Python (this module) --> user's Python function(s)
        for kind in ['mousemove', 'mouseup', 'mousedown', 'click', 'wheel']:
            self._mouse_event_dispatchers[kind] = widgets.widget.CallbackDispatcher()

        # Store init data in traitlet(s)
        self.format = format
        self.quality = quality

        if url:
            # Fetch image from URL and decompress into numpy array
            data_comp, format_orig = image.download(url)
            data = image.decompress(data_comp)

        # Set image data
        self.data = data

    @property
    def data(self):
        """Image data"""
        return self._data

    @data.setter
    def data(self, data):
        with self.hold_sync():
            # Hold syncing state changes until the context manager is released
            if issubclass(type(data), np.ndarray):
                # Compress input image data and encode via Base64
                self._data = data.copy()
                HxW = data.shape[:2]

                data_comp = image.compress(self._data, fmt=self.format)
                data_encoded = image.encode(data_comp)
            else:
                # Clobber image data
                self._data = None
                HxW = 0, 0
                data_encoded = b''

            # Update traitlets.
            self._canvas_height, self._canvas_width = HxW
            self.height, self.width = HxW
            self._encoded = data_encoded

    @property
    def format(self):
        """Image encoding format."""
        return self._format

    _valid_formats = ['png', 'jpg', 'jpeg', 'webp']

    @format.setter
    def format(self, value):
        """Image compression format."""
        if value.lower() not in self._valid_formats:
            raise ValueError('Invalid encoding format: {}'.format(value))
        self._format = value.lower()

    def display(self):
        """
        Display to Notebook using IPython hooks.
        """
        IPython.display.display(self)

    #####################################################
    # Python response to mouse events generated by JavaScript front-end.
    # https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent
    def _handle_mouse(self, name_trait, event):  # info_old, info_new):
        """
        Python response to mouse events generated by JavaScript front-end.
        """
        # Event type should match one of ['mousemove', 'mouseup', 'mousedown', 'click', 'wheel']
        try:
            kind = event['type']
            self._mouse_event_dispatchers[kind](self, event)
        except KeyError:
            print(event)
            raise

    #######################################################
    # Register Python mouse event handler functions.
    #
    #   callback : function to be called with two arguments: widget instance and event information.
    #   remove : bool (optional), set to true to unregister the callback function.
    #
    #   https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent
    #   https://developer.mozilla.org/en-US/docs/Web/Events/wheel
    def on_mouse_all(self, callback, remove=False):
        """
        Register callback function for all mouse events, arguments to callback are the widget
        instance and event information.
        """
        for k, d in self._mouse_event_dispatchers.items():
            d.register_callback(callback, remove=remove)

    def on_mouse_move(self, callback, remove=False):
        """
        Register callback function for mouse move, arguments to callback are the widget
        instance and event information.
        """
        self._mouse_event_dispatchers['mousemove'].register_callback(callback, remove=remove)

    def on_mouse_up(self, callback, remove=False):
        """
        Register callback function for mouse up, arguments to callback are the widget
        instance and event information.
        """
        self._mouse_event_dispatchers['mouseup'].register_callback(callback, remove=remove)

    def on_mouse_down(self, callback, remove=False):
        """
        Register callback function for mouse down, arguments to callback are the widget
        instance and event information.
        """
        self._mouse_event_dispatchers['mousedown'].register_callback(callback, remove=remove)

    def on_click(self, callback, remove=False):
        """
        Register callback function for mouse click, arguments to callback are the widget
        instance and event information.
        """
        self._mouse_event_dispatchers['click'].register_callback(callback, remove=remove)

    def on_wheel(self, callback, remove=False):
        """R
        egister callback function for mouse wheel, arguments to callback are the widget
        instance and event information.
        """
        self._mouse_event_dispatchers['wheel'].register_callback(callback, remove=remove)

#################################################

if __name__ == '__main__':
    pass
