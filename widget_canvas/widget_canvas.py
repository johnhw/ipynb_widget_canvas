
from __future__ import division, print_function, unicode_literals, absolute_import

import os
import numpy as np

import IPython
from ipywidgets import widgets
import traitlets

from . import image


def inject():
    """
    Inject JavaScript component into browser front end.
    """
    fname = 'widget_canvas.js'
    path_module = os.path.abspath(os.path.dirname(__file__))

    f = os.path.join(path_module, fname)
    js = IPython.display.Javascript(filename=f)  # data=None, url=None, filename=None, lib=None

    IPython.display.display(js)

# Inject JavaScript when module is first loaded.
inject()


class CanvasImage(widgets.widget.DOMWidget):
    """
    Display images using HTML5 Canvas with IPython Notebook widget system.
    """
    # _model_name:   Name of Backbone model registered in the front-end to create and sync with.
    # _model_module: A requirejs module name in which to find _model_name.
    # _view_name:    Default view registered in the front-end to use to represent the widget.
    # _view_module:  A requirejs module in which to find _view_name.

    _view_name = traitlets.Unicode('CanvasImageView', sync=True)

    # Encoded image data and metadata
    _encoded = traitlets.Bytes(help='Encoded image data', sync=True)
    _format = traitlets.Unicode(help='Image encoding format', sync=True)

    # HTML/DOM/CSS screen display width and height
    height = traitlets.CInt(help='image screen display height', sync=True)
    width = traitlets.CInt(help='image screen display width', sync=True)

    # Image rendering quality. https://developer.mozilla.org/en/docs/Web/CSS/image-rendering
    pixilated = traitlets.Bool(False, help='Render images via nearest neighbor sampling', sync=True)

    # Canvas width and height, slaved to image data width and height.
    width_canvas = traitlets.CInt(help='image data width', sync=True)
    height_canvas = traitlets.CInt(help='image data height', sync=True)

    # Mouse event information
    _mouse_active = traitlets.Bool(False, help='Indicate if mouse events are active', sync=True)
    _mouse_event = traitlets.Dict(help='Front-end mouse event information', sync=True)

    def __init__(self, data=None, url=None, format='webp', quality=70, force_inject=False,
                 **kwargs):
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

        if force_inject:
            inject()

        # Internal Python handler for JS mouse events synced through _mouse_event traitlet
        # https://developer.mozilla.org/en-US/docs/Web/Reference/Events
        # https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent
        self.on_trait_change(self._handle_mouse, str('_mouse_event'))  # JS --> Python

        # Allow user to attach Python callback functions to operate in response to mouse events.
        self._mouse_event_dispatchers = {}  # Python (this module) --> user's Python function(s)
        event_kinds = ['move', 'up', 'down', 'click', 'wheel']
        for kind in event_kinds:
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
                self.update_data(data)
                HxW = data.shape[:2]

                # # Compress input image data and encode via Base64
                # self._data = image.setup_data(data)
                # data_comp = image.compress(self._data, fmt=self.format)
                # data_encoded = image.encode(data_comp)
            else:
                # Clobber image data
                self._data = None
                HxW = 0, 0
                # data_comp = None
                self._encoded = b''

            # Update traitlets
            self.height, self.width = HxW
            self.height_canvas, self.width_canvas = HxW

    def update_data(self, data):
        """
        Update data only, leave widths, height, etc. unchanged.
        """
        # Compress input image data and encode via Base64
        self._data = image.setup_data(data)

        data_comp = image.compress(self._data, fmt=self.format)
        data_encoded = image.encode(data_comp)
        self._encoded = data_encoded

    @property
    def format(self):
        """
        Image compression/encoding format, e.g. 'jpg', 'png', 'webp', etc.
        """
        return self._format

    @format.setter
    def format(self, value):
        valid_formats = ['png', 'jpg', 'jpeg', 'webp']
        if value.lower() not in valid_formats:
            raise ValueError('Invalid encoding format: {}'.format(value))

        self._format = value.lower()

    def display(self):
        """
        Display image to Notebook using IPython's rich-display infrastructure.
        """
        IPython.display.display(self)

    #####################################################
    # Respond to mouse events by calling registered Python function event handlers
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
        Respond to JavaScript mouse events by calling registered Python function event handlers
        https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent
        """
        # Event types in JavaScript: 'mousemove', 'mouseup', 'mousedown', 'click', 'wheel'
        # Event types in Python:          'move',      'up',      'down', 'click', 'wheel'
        # kind_js_to_py = {'mousemove': 'move',
        #                  'mouseup': 'up',
        #                  'mousedown': 'down',
        #                  'click': 'click',
        #                  'wheel': 'wheel'}

        # Preprocess event data
        # event['type'] = kind_js_to_py[event['type']]  # update event types
        event = self._scale_xy_screen_to_data(event)

        # Handle the event
        try:
            kind = event['type']
            self._mouse_event_dispatchers[kind](self, event)
        except KeyError:
            raise ValueError('Really unexpected event type: {}'.format(kind))

    #######################################################
    # Register Python fnctions as mouse event handlers
    #
    #   callback : function to be called with two arguments: widget instance and event information.
    #   remove : bool (optional), set to true to unregister the callback function.
    #
    #   https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent
    #   https://developer.mozilla.org/en-US/docs/Web/Events/wheel
    def on_mouse(self, callback, kinds=None, remove=False):
        """
        Register a callback function for one or more mouse kinds of events.
        Valid mouse event kinds: 'move', 'up', 'down', 'click', 'wheel'

        Default kinds=None will register the callback with all mouse event types.
        Setting kind to a string or a list of strings will register the callback with
        just the specified kinds.

        Set keyword remove=True in order to unregister an existing callback function.
        Arguments to the supplied callback function are the widget instance and event information.
        """

        # Enable mouse event handling at front end.  Still need a way to turn off mouse event
        # handling when/if all event handler functions are disabled.
        self._mouse_active = True

        # Default to all defined event dispatchers
        if not kinds:
            # Default all mouse event kinds: 'move', 'up', 'down', 'click', 'wheel'
            kinds = self._mouse_event_dispatchers.keys()

        if isinstance(kinds, str):
            kinds = [kinds]

        for k in kinds:
            if k not in self._mouse_event_dispatchers:
                raise ValueError('Invalid callback type: {}'.format(k))

            # Register/un-register user-defined callback function
            self._mouse_event_dispatchers[k].register_callback(callback, remove=remove)

    def on_mouse_move(self, callback, remove=False):
        self.on_mouse(callback, 'move', remove=remove)

    def on_mouse_up(self, callback, remove=False):
        self.on_mouse(callback, 'up', remove=remove)

    def on_mouse_down(self, callback, remove=False):
        self.on_mouse(callback, 'down', remove=remove)

    def on_mouse_click(self, callback, remove=False):
        self.on_mouse(callback, 'click', remove=remove)

    def on_mouse_wheel(self, callback, remove=False):
        self.on_mouse(callback, 'wheel', remove=remove)


#################################################

if __name__ == '__main__':
    pass
