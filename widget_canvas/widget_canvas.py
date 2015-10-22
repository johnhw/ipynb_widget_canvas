
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

    If data type is not np.uint8, it will be cast to uint8 by scaling min(data) -> 0 and
    max(data) -> 255.
    """
    # _model_name:   Name of Backbone model registered in the front-end to create and sync with.
    # _model_module: A requirejs module name in which to find _model_name.
    # _view_name:    Default view registered in the front-end to use to represent the widget.
    # _view_module:  A requirejs module in which to find _view_name.

    _view_name = traitlets.Unicode('CanvasImageView', sync=True)
    _view_module = traitlets.Unicode('nbextensions/widget_canvas/widget_canvas', sync=True)
    # _model_name = traitlets.Unicode('CanvasImageModel', sync=True)
    # _model_module = traitlets.Unicode('nbextensions/widget_canvas/widget_canvas', sync=True)

    # Encoded image data and metadata
    _encoded = traitlets.Bytes(help='Encoded image data', sync=True)
    _format = traitlets.Unicode(help='Image encoding format', sync=True)

    # HTML/DOM/CSS screen display width and height
    height = traitlets.CInt(help='image screen display height', sync=True)
    width = traitlets.CInt(help='image screen display width', sync=True)

    # Canvas width and height, slaved to image data width and height.
    width_canvas = traitlets.CInt(help='image data width', sync=True)
    height_canvas = traitlets.CInt(help='image data height', sync=True)

    # Mouse event information
    _mouse_event = traitlets.Dict(help='Front-end mouse event information', sync=True)

    def __init__(self, data=None, url=None, format='webp', quality=70, **kwargs):
        """
        Instantiate a new Canvas Image Widget object.

        Display images using HTML5 Canvas with IPython Notebook widget system. Keyword `value`
        contains the input image data.  It must be a Numpy array (or equivalent) with a shape
        similar to one of the following:
            (rows, columns)    - Greyscale
            (rows, columns, 1) - Greyscale
            (rows, columns, 3) - RGB
            (rows, columns, 4) - RGBA

        If data type is neither of np.uint8 or np.int16, it will be cast to uint8 by scaling
        min(data) -> 0 and max(data) -> 255.

        If you supply a URL that points to an image then that image will be fetched and stored
        locally as a uint8 byte array.
        """
        super(CanvasImage, self).__init__(**kwargs)

        # Internal Python handler for JS mouse events synced through _mouse_event traitlet
        # https://developer.mozilla.org/en-US/docs/Web/Reference/Events
        # https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent
        self.on_trait_change(self._handle_mouse, str('_mouse_event'))  # JS --> Python

        # Allow user to attach Python callback functions to operate in response to mouse events.
        self._mouse_event_dispatchers = {}  # Python (this module) --> user's Python function(s)
        for kind in ['mousemove', 'mouseup', 'mousedown', 'click', 'wheel']:
            # independent dispatcher for each 'kind' of event.
            self._mouse_event_dispatchers[kind] = widgets.widget.CallbackDispatcher()

        # Store init data in traitlet(s)
        self.format = format
        self.quality = quality

        if url:
            # Fetch image from URL and decompress into local numpy array
            data_comp, format_orig = image.download(url)
            data = image.decompress(data_comp)

        # Set image data
        self.data = data

    @property
    def data(self):
        """
        Image data stored as a numpy array.
        """
        return self._data

    @data.setter
    def data(self, data):
        with self.hold_sync():
            # Hold syncing state changes until the context manager is released
            if issubclass(type(data), np.ndarray):
                # Compress input image data and encode via Base64
                self._data = data.copy()  # to copy or not to copy, that's a good question!
                HxW = data.shape[:2]

                data_comp = image.compress(self._data, fmt=self.format)
                data_encoded = image.encode(data_comp)
            else:
                # Clobber image data
                self._data = None
                HxW = 0, 0
                # data_comp = None
                data_encoded = b''

            # Update traitlets
            # self._canvas_height, self._canvas_width = HxW
            self.height, self.width = HxW
            self.height_canvas, self.width_canvas = HxW
            self._encoded = data_encoded

    # @property
    # def width(self):
    #     """
    #     Widget display width
    #     """
    #     return self._width

    # @width.setter
    # def width(self, value):
    #     if value:
    #         self._width = value
    #     else:
    #         # Reset to data original value
    #         self._width = self._data.shape[1]

    # @property
    # def height(self):
    #     """
    #     Widget display height
    #     """
    #     return self._height

    # @height.setter
    # def height(self, value):
    #     if value:
    #         self._height = value
    #     else:
    #         # Reset to data original value
    #         self._height = self._data.shape[0]

    @property
    def format(self):
        """
        Image compression/encoding format, e.g. 'jpg', 'png', 'webp', etc.
        """
        return self._format

    _valid_formats = ['png', 'jpg', 'jpeg', 'webp']

    @format.setter
    def format(self, value):
        if value.lower() not in self._valid_formats:
            raise ValueError('Invalid encoding format: {}'.format(value))
        self._format = value.lower()

    def display(self):
        """
        Display image to Notebook using IPython infrastructure.
        """
        IPython.display.display(self)

    #####################################################
    # Python response to mouse events generated by JavaScript front-end.
    def _scale_xy_screen_to_data(self, event):
        """
        Event XY values are generated in screen coordinates.  This function convert the values
        to data XY coordinates.
        """
        event['canvasY'] = round(event['canvasY'] * self._data.shape[0] / self.height)
        event['canvasX'] = round(event['canvasX'] * self._data.shape[1] / self.width)

        return event

    def _handle_mouse(self, name_trait, event):  # info_old, info_new):
        """
        Python response to mouse events generated by JavaScript front-end.
        https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent
        """
        # Event type should match one of ['mousemove', 'mouseup', 'mousedown', 'click', 'wheel']
        try:
            kind = event['type']
            event = self._scale_xy_screen_to_data(event)
            self._mouse_event_dispatchers[kind](self, event)
        except KeyError:
            msg = 'Invalid event type: {}'.format(event['type'])
            raise ValueError(msg)

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
        Register callback function for mouse 'move' events, arguments to callback are the widget
        instance and event information.
        """
        self._mouse_event_dispatchers['mousemove'].register_callback(callback, remove=remove)

    def on_mouse_up(self, callback, remove=False):
        """
        Register callback function for mouse 'up' events, arguments to callback are the widget
        instance and event information.
        """
        self._mouse_event_dispatchers['mouseup'].register_callback(callback, remove=remove)

    def on_mouse_down(self, callback, remove=False):
        """
        Register callback function for mouse 'down' events, arguments to callback are the widget
        instance and event information.
        """
        self._mouse_event_dispatchers['mousedown'].register_callback(callback, remove=remove)

    def on_click(self, callback, remove=False):
        """
        Register callback function for mouse 'click' events, arguments to callback are the widget
        instance and event information.
        """
        self._mouse_event_dispatchers['click'].register_callback(callback, remove=remove)

    def on_wheel(self, callback, remove=False):
        """
        Register callback function for mouse 'wheel' events, arguments to callback are the widget
        instance and event information.
        """
        self._mouse_event_dispatchers['wheel'].register_callback(callback, remove=remove)

#################################################

if __name__ == '__main__':
    pass
