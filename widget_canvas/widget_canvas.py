from __future__ import division, print_function, unicode_literals

import IPython.html.widgets

# import utility


class CanvasWidget(IPython.html.widgets.widget.DOMWidget):
    """
    Interface to the HTML Canvas Element using IPython Notebook widget system.
    """
    _view_name = IPython.utils.traitlets.Unicode('CanvasView', sync=True)

    # Image data source.
    _src = IPython.utils.traitlets.Unicode(sync=True)

    # Canvas dimensions.
    _width = IPython.utils.traitlets.CFloat(sync=True)
    _height = IPython.utils.traitlets.CFloat(sync=True)

    # Mouse event information.
    _mouse = IPython.utils.traitlets.Dict(sync=True)

    def __init__(self, src=None, **kwargs):
        super(CanvasWidget, self).__init__(**kwargs)

        if src is None:
            src = ''

        # Setup internal Python handler for front-end mouse events synced through
        # the self._mouse traitlet.
        self.on_trait_change(self._handle_mouse, '_mouse')

        # Setup dispatchers to manage external user-defined event handlers.
        self._mouse_move_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        self._mouse_click_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        self._mouse_drag_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()

        self._flag_mouse_down = False

        # Store supplied src data in traitlet.
        self._src = src

    #####################################################
    # Traitlet data sync event handlers.
    def _handle_mouse(self, name_trait, info_event):  # info_old, info_new):
        """
        JavaScript --> Python
        Handle mouse events generated by front-end model.
        """
        # Call all registered back-end event handlers with updated information.
        if info_event['type'] == 'mousemove':
            if self._flag_mouse_down:
                self._mouse_drag_dispatcher(info_event)
            else:
                self._mouse_move_dispatcher(info_event)
        elif info_event['type'] == 'mousedown':
            self._flag_mouse_down = True
        elif info_event['type'] == 'mouseup':
            if self._flag_mouse_down:
                self._mouse_click_dispatcher(info_event)
            self._flag_mouse_down = False
        else:
            pass

    #######################################################
    # Back-end callback setup methods.
    def on_mouse_move(self, callback, remove=False):
        """
        Register a Python back-end event callback.

        Parameters
        ----------
        callback : fn(self, *args, **kwargs)
        remove : bool (optional), set to true to remove the callback from the list of callbacks.
        """
        self._mouse_move_dispatcher.register_callback(callback, remove=remove)

    def on_mouse_click(self, callback, remove=False):
        """
        Register a Python back-end event callback.

        Parameters
        ----------
        callback : fn(self, *args, **kwargs)
        remove : bool (optional), set to true to remove the callback from the list of callbacks.
        """
        self._mouse_click_dispatcher.register_callback(callback, remove=remove)

    def on_mouse_drag(self, callback, remove=False):
        """
        Register a Python back-end event callback.

        Parameters
        ----------
        callback : fn(self, *args, **kwargs)
        remove : bool (optional), set to true to remove the callback from the list of callbacks.
        """
        self._mouse_drag_dispatcher.register_callback(callback, remove=remove)


class CanvasImageWidget(CanvasWidget):
    """
    Display and manipulate images using HTML5 Canvas and with IPython Notebook
    widget system.
    """
    def __init__(self, data=None, **kwargs):
        super(CanvasImageWidget, self).__init__(**kwargs)
        self.image = data

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, data):
        if data is None:
            return

        # Store the image data for later use??
        self._image = data

        height, width = data.shape[:2]
        self._height = height
        self._width = width

        # Compress and encode input image data.  Store in baseclass' _src traitlet
        # for syncing with front-end.
        self._src = utility.encode_image(data)


#######
# Helper functions.

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
    data_comp, fmt = png_compress(data_image)

    # Encode via base64.
    data_b64 = base64.b64encode(data_comp)

    # Build src string.
    src = 'data:image/{:s};base64,{:s}'.format(fmt, data_b64)

    return src
