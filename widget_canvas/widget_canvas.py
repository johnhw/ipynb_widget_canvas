
from __future__ import division, print_function, unicode_literals

import os
import base64
import time

import IPython.html.widgets
import image


#################################################
# Helper functions
#
_path_module = os.path.abspath(os.path.dirname(__file__))
_path_js = os.path.join(_path_module, 'js')


def _read_local_js(fname):
    """
    Read a JavaScript file from application's local JS folder.  Return a string.
    """
    b, e = os.path.splitext(os.path.basename(fname))
    f = os.path.join(_path_js, b + '.js')

    if not os.path.isfile(f):
        raise IOError('File not found: {}'.format(f))

    with open(f) as fo:
        text = fo.read()

    return text


def _bootstrap_js():
    """
    Load application-specific JavaScript source code and inject into current Notebook session.
    """
    files = ['widget_canvas.js']

    for f in files:
        js = _read_local_js(f)
        IPython.display.display_javascript(js, raw=True)

#################################################


class CanvasWidget(IPython.html.widgets.widget.DOMWidget):
    """
    Interface to the HTML Canvas Element using IPython Notebook widget system.
    """
    _view_name = IPython.utils.traitlets.Unicode('CanvasView', sync=True)

    # Image data source.
    src = IPython.utils.traitlets.Unicode(sync=True)

    # Canvas dimensions.
    _width = IPython.utils.traitlets.CFloat(sync=True)
    _height = IPython.utils.traitlets.CFloat(sync=True)

    # Mouse event information.
    _mouse = IPython.utils.traitlets.Dict(sync=True)

    def __init__(self, src=None, width=None, height=None, **kwargs):
        """
        Instantiate a new CanvasWidget object.
        """
        super(CanvasWidget, self).__init__(**kwargs)

        if src is None:
            src = ''

        # Setup internal Python handler for front-end mouse events synced through
        # the self._mouse Traitlet.
        self.on_trait_change(self._handle_mouse, str('_mouse'))

        # Setup dispatchers to manage user-defined Python event handlers.
        self._mouse_move_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        self._mouse_click_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        self._mouse_drag_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()

        self._flag_mouse_down = False

        # Store supplied src data in traitlet.
        self.src = src
        if height:
            self._height = height

        if width:
            self._width = width

    def display(self):
        """
        Display to Notebook using IPython hooks.
        """
        IPython.display.display(self)

    #####################################################
    # Methods to handle Traitlet data sync events.
    def _handle_mouse(self, name_trait, info_event):  # info_old, info_new):
        """
        Handle mouse events
        JavaScript front-end events handled via Python back-end callback functions.
        """

        # Call all registered back-end event handlers with updated information.
        if info_event['type'] == 'mousemove':
            if self._flag_mouse_down:
                info_event['type'] = 'mousedrag'
                self._mouse_drag_dispatcher(info_event)
            else:
                self._mouse_move_dispatcher(info_event)
        elif info_event['type'] == str('mousedown'):
            self._flag_mouse_down = True
        elif info_event['type'] == 'mouseup':
            if self._flag_mouse_down:
                self._mouse_click_dispatcher(info_event)
            self._flag_mouse_down = False
        else:
            pass

    #######################################################
    # Methods to register user's Python event handler functions.
    #
    # The signature for each callback registration function is similar:
    #   callback : function to be called with event information as argument.
    #   remove : bool (optional), set to true to unregister the callback function.
    #
    def on_mouse_move(self, callback, remove=False):
        """Repond to motion."""
        self._mouse_move_dispatcher.register_callback(callback, remove=remove)

    def on_mouse_down(self, callback, remove=False):
        """Repond to mouse button down."""
        self._mouse_move_dispatcher.register_callback(callback, remove=remove)

    def on_mouse_up(self, callback, remove=False):
        """Repond to mouse button up."""
        self._mouse_move_dispatcher.register_callback(callback, remove=remove)

    def on_mouse_click(self, callback, remove=False):
        """Repond to mouse button click: button down followed by button up."""
        self._mouse_click_dispatcher.register_callback(callback, remove=remove)

    def on_mouse_drag(self, callback, remove=False):
        """Repond to drag motion: motion while button is down."""
        self._mouse_drag_dispatcher.register_callback(callback, remove=remove)


class ImageWidget(CanvasWidget):
    """
    Display and manipulate images using HTML5 Canvas with IPython Notebook widget system.
    This class builds upon CanvasWidget making it easier to work with images.

    Input image data, if supplied, must be a Numpy array (or equivalent) with a shape similar to
    one of the following:
        (rows, columns)    - Greyscale
        (rows, columns, 1) - Greyscale
        (rows, columns, 3) - RGB
        (rows, columns, 4) - RGBA

    If data type is neither of np.uint8 or np.int16, it will be cast to uint8 by mapping
    min(data) -> 0 and max(data) -> 255.
    """
    def __init__(self, data=None, **kwargs):
        """
        Instantiate a new CanvasImageWidget object.
        """
        super(ImageWidget, self).__init__(**kwargs)
        self.image = data

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, data_image):
        # Store the image data for later use.
        self._image = data_image

        if data_image is None:
            return

        # Image width and height.
        self._height = data_image.shape[0]
        self._width = data_image.shape[1]

        # Compress and encode input image data.  Store the result in baseclass' src traitlet for
        # syncing with front-end.
        data_comp, fmt = image.png_compress(data_image)

        # Encode via base64.
        data_b64 = base64.b64encode(data_comp)

        # Build src string and put it into Traitlet for synchronizing with front-end.
        self.src = 'data:image/{:s};base64,{:s}'.format(fmt, data_b64)


#################################################

# Bootstrap Widget's JavaScript code into Notebook browser environment.
_bootstrap_js()
time.sleep(0.01)  # sleep to give time for JavaScript stuff to get set up in the background.
