
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
#################################################


class CanvasWidget(IPython.html.widgets.widget.DOMWidget):
    """
    Interface to the HTML Canvas Element using IPython Notebook widget system.
    """
    _view_name = IPython.utils.traitlets.Unicode('CanvasView', sync=True)

    # Image data source.
    src = IPython.utils.traitlets.Unicode(sync=True)

    # Width and height of canvas as rendered by the browser.  Size units are 'CSS Pixels'. This is
    # analagous to a portal or window.  These parameters default to the image's inherent width and
    # height in data pixels.
    width = IPython.utils.traitlets.CFloat(sync=True)
    height = IPython.utils.traitlets.CFloat(sync=True)

    # Image transformation.
    transformation = IPython.utils.traitlets.List(sync=True)

    # Mouse and keyboard event information.
    _mouse = IPython.utils.traitlets.Dict(sync=True)

    def __init__(self, src='', **kwargs):
        """
        Instantiate a new CanvasWidget object.
        """
        super(CanvasWidget, self).__init__(**kwargs)

        # Setup internal Python handler for front-end mouse events synced through
        # the Traitlet self._mouse.
        self.on_trait_change(self._handle_mouse, str('_mouse'))

        # Setup dispatchers to manage user-defined Python event handlers.
        self._mouse_move_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        self._mouse_drag_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        self._mouse_click_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        self._mouse_down_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        self._mouse_up_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        self._mouse_wheel_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()

        # Helper variables for mouse state.
        self._flag_mouse_down = False
        self._drag_origin = None

        # Store supplied init data in traitlet(s).
        if src:
            self.src = src

    def display(self):
        """
        Display to Notebook using IPython hooks.
        """
        IPython.display.display(self)

    #####################################################
    # Methods to handle Traitlet data sync events.
    #
    def _handle_mouse(self, name_trait, event):  # info_old, info_new):
        """Python back-end handling of JavaScript front-end generated mouse events.
        """

        # Call all registered back-end event handlers with updated information.
        if event['type'] == 'mousemove':
            # The mouse has moved.
            if self._flag_mouse_down:
                # Mouse has moved with button down.  This is really a `mousedrag` event.
                if not self._drag_origin:
                    raise ValueError('drag origin should have been defined prior to \
                                      calling this function')

                event['type'] = str('mousedrag')
                event['dragX'] = event['canvasX'] - self._drag_origin[0]
                event['dragY'] = event['canvasY'] - self._drag_origin[1]

                self._mouse_drag_dispatcher(event)
            else:
                # Mouse has moved with button up.
                self._mouse_move_dispatcher(event)

        elif event['type'] == 'mousedown':
            # Mouse button has been clicked down.

            # Update drag origin in case the mouse moves afterwards and generates a drag event.
            if not self._drag_origin:
                self._drag_origin = [event['canvasX'], event['canvasY']]

            self._flag_mouse_down = True
            self._mouse_down_dispatcher(event)

        elif event['type'] == 'mouseup':
            # Mouse button has been lifted.
            self._mouse_up_dispatcher(event)

            if self._flag_mouse_down:
                # Mouse changing from "down" to "up" generates a "click" event.
                self._mouse_click_dispatcher(event)

            # Clear state flags.
            self._flag_mouse_down = False
            self._drag_origin = None

        elif event['type'] == 'wheel':
            # Wheel scroll event.
            self._mouse_wheel_dispatcher(event)

        else:
            pass

    #######################################################
    # User-facing methods to register Python event handler functions.
    #
    # The signature for each registration function is similar:
    #   callback : function to be called with event information as argument.
    #   remove : bool (optional), set to true to unregister the callback function.
    #
    def on_mouse_move(self, callback, remove=False):
        """Repond to mouse motion.
        """
        self._mouse_move_dispatcher.register_callback(callback, remove=remove)

    def on_mouse_drag(self, callback, remove=False):
        """Repond to drag motion: motion while button is down.
        """
        self._mouse_drag_dispatcher.register_callback(callback, remove=remove)

    def on_mouse_down(self, callback, remove=False):
        """Repond to mouse button down.
        """
        self._mouse_down_dispatcher.register_callback(callback, remove=remove)

    def on_mouse_up(self, callback, remove=False):
        """Repond to mouse button up.
        """
        self._mouse_up_dispatcher.register_callback(callback, remove=remove)

    def on_mouse_click(self, callback, remove=False):
        """Repond to mouse button click: button down followed by button up.
        """
        self._mouse_click_dispatcher.register_callback(callback, remove=remove)

    def on_mouse_wheel(self, callback, remove=False):
        """Repond to mouse wheel scroll event.
        """
        self._mouse_wheel_dispatcher.register_callback(callback, remove=remove)


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
    def __init__(self, data_image=None, **kwargs):
        """
        Instantiate a new CanvasImageWidget object.
        """
        super(ImageWidget, self).__init__(**kwargs)
        self.image = data_image

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
        self.height = data_image.shape[0]
        self.width = data_image.shape[1]

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
