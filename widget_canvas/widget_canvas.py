
from __future__ import division, print_function, unicode_literals

import os
import base64
import time

import IPython.html.widgets
import image
# import transform

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
        print('Boot: {}'.format(f))
        js = _read_local_js(f)
        IPython.display.display_javascript(js, raw=True)

#################################################


class CanvasImageBase(IPython.html.widgets.widget.DOMWidget):
    """
    Display images using HTML5 Canvas with IPython Notebook widget system. Input image data, if
    supplied, must be a Numpy array (or equivalent) with a shape similar to one of the following:
        (rows, columns)    - Greyscale
        (rows, columns, 1) - Greyscale
        (rows, columns, 3) - RGB
        (rows, columns, 4) - RGBA

    If data type is neither of np.uint8 or np.int16, it will be cast to uint8 by mapping
    min(data) -> 0 and max(data) -> 255.
    """

    _view_name = IPython.utils.traitlets.Unicode('CanvasImageBaseView', sync=True)

    # Image data source.
    data_encode = IPython.utils.traitlets.Unicode(sync=True)

    # Image smoothing.
    smoothing = IPython.utils.traitlets.Bool(sync=True)

    # Width and height of canvas as determined by the front-end after receiving a new image
    # from the backend.
    width = IPython.utils.traitlets.CFloat(sync=True)
    height = IPython.utils.traitlets.CFloat(sync=True)

    def __init__(self, data_image=None, fmt='webp', **kwargs):
        """
        Instantiate a new Image object.

        Display images using HTML5 Canvas with IPython Notebook widget system. Input image data, if
        supplied, must be a Numpy array (or equivalent) with a shape similar to one of the
        following:
            (rows, columns)    - Greyscale
            (rows, columns, 1) - Greyscale
            (rows, columns, 3) - RGB
            (rows, columns, 4) - RGBA

        If data type is neither of np.uint8 or np.int16, it will be cast to uint8 by mapping
        min(data) -> 0 and max(data) -> 255.
        """
        super(CanvasImageBase, self).__init__(**kwargs)

        # Store supplied init data in traitlet(s).
        self.fmt = fmt
        if data_image is not None:
            self.image = data_image

    def __repr__(self):
        template = "Size: {:d} bytes\nFormat: {:s}\n"
        value = template.format(len(self.data_encode), self.fmt)

        return value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, data_image):
        # Store the image data for later use.
        self._image = data_image

        if data_image is None:
            return

        # Compress input image data and encode via Base64.
        quality = 75  # note: Q = 75 yields great results using WebP image codec.
        data_comp, fmt = image.compress(data_image, fmt=self.fmt, quality=quality)

        data_b64 = base64.b64encode(data_comp)
        self.data_encode = 'data:image/{:s};base64,{:s}'.format(fmt, data_b64)

    def display(self):
        """
        Display to Notebook using IPython hooks.
        """
        IPython.display.display(self)

#################################################


class CanvasImageFancy(CanvasImageBase):
    """
    Display images using HTML5 Canvas with IPython Notebook widget system. Input image data, if
    supplied, must be a Numpy array (or equivalent) with a shape similar to one of the following:
        (rows, columns)    - Greyscale
        (rows, columns, 1) - Greyscale
        (rows, columns, 3) - RGB
        (rows, columns, 4) - RGBA

    If data type is neither of np.uint8 or np.int16, it will be cast to uint8 by mapping
    min(data) -> 0 and max(data) -> 255.
    """

    _view_name = IPython.utils.traitlets.Unicode('CanvasImageFancyView', sync=True)

    # Image transformation values.
    _transform_values = IPython.utils.traitlets.List(sync=True)

    # Mouse and keyboard event information.
    _mouse = IPython.utils.traitlets.Dict(sync=True)

    def __init__(self, data_image=None, **kwargs):
        """
        Instantiate a new Image object.

        Display images using HTML5 Canvas with IPython Notebook widget system. Input image data, if
        supplied, must be a Numpy array (or equivalent) with a shape similar to one of the
        following:
            (rows, columns)    - Greyscale
            (rows, columns, 1) - Greyscale
            (rows, columns, 3) - RGB
            (rows, columns, 4) - RGBA

        If data type is neither of np.uint8 or np.int16, it will be cast to uint8 by mapping
        min(data) -> 0 and max(data) -> 255.
        """
        super(CanvasImageFancy, self).__init__(data_image=data_image, **kwargs)

        # Setup internal Python handler for front-end mouse events synced through
        # the Traitlet self._mouse.
        self.on_trait_change(self._handle_mouse, str('_mouse'))

        # Setup dispatchers to manage user-defined Python event handlers.
        # mouse_move_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        # mouse_drag_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        # mouse_click_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        # mouse_down_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        # mouse_up_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()
        # mouse_wheel_dispatcher = IPython.html.widgets.widget.CallbackDispatcher()

        self._mouse_event_dispatchers = {'move': IPython.html.widgets.widget.CallbackDispatcher(),
                                         'drag': IPython.html.widgets.widget.CallbackDispatcher(),
                                         'down': IPython.html.widgets.widget.CallbackDispatcher(),
                                         'up': IPython.html.widgets.widget.CallbackDispatcher(),
                                         'click': IPython.html.widgets.widget.CallbackDispatcher(),
                                         'wheel': IPython.html.widgets.widget.CallbackDispatcher()}

        # Mouse state helper variables.
        self._flag_mouse_down = False
        self._drag_origin_xy = None
        self._drag_xy = None        # distance from drag_origin
        self._drag_delta_xy = None  # distance from position of previous mouse drag motion event
        self._drag_prior_mouse_xy = 0, 0

        self.mouse_xy = 0, 0

        # Manage image 2D affine transform information.
        # self._transform = transform.Transform()

    @property
    def transform(self):
        print('get')
        return self._transform

    @transform.setter
    def transform(self, value):
        print('set')
        self._transform = value

    #####################################################
    # Methods to handle Traitlet data sync events.
    #
    def _handle_mouse(self, name_trait, event):  # info_old, info_new):
        """Python back-end handling of JavaScript front-end generated mouse events.
        """

        # Update internal storage for mouse coordinates.
        self.mouse_xy = event['canvasX'], event['canvasY']
        event['canvas_xy'] = self.mouse_xy
        event.pop('canvasX', None)
        event.pop('canvasY', None)

        # Call all registered back-end event handlers with updated information.
        if event['type'] == 'mousemove':
            # The mouse has moved, but what kind of move, eh?
            if self._flag_mouse_down:
                # Mouse Drag Event: the mouse moved with the button down.
                if not self._drag_origin_xy:
                    raise ValueError('drag origin should have been defined prior to \
                                      calling this function')

                self._drag_prior_mouse_xy = self._drag_xy

                self._drag_xy = (self.mouse_xy[0] - self._drag_origin_xy[0],
                                 self.mouse_xy[1] - self._drag_origin_xy[1])

                self._drag_delta_xy = (self._drag_xy[0] - self._drag_prior_mouse_xy[0],
                                       self._drag_xy[1] - self._drag_prior_mouse_xy[1])

                # Assemble drag event details.
                event['type'] = str('mousedrag')
                event['drag_origin_xy'] = self._drag_origin_xy
                event['drag_xy'] = self._drag_xy
                event['drag_delta_xy'] = self._drag_delta_xy

                # Call dispatcher.
                self._mouse_drag_dispatcher(self, event)
            else:
                # Mouse Move Event, ie. the button is up.
                # Call dispatcher.
                self._mouse_move_dispatcher(self, event)

        elif event['type'] == 'mousedown':
            # Mouse Down Event.

            # Update drag event variable.
            # Just in case the mouse moves afterwards and generates a proper drag event.
            self._drag_prior_mouse_xy = self.mouse_xy
            self._drag_origin_xy = self.mouse_xy
            self._drag_xy = 0, 0

            # Update state variable and call dispatcher.
            self._flag_mouse_down = True
            self._mouse_down_dispatcher(self, event)

        elif event['type'] == 'mouseup':
            # Mouse Up Event.

            # Call dispatcher.
            self._mouse_up_dispatcher(self, event)

            if self._flag_mouse_down:
                # Mouse Click Event, mouse down + mouse up = mose click.
                # Call dispatcher.
                self._mouse_click_dispatcher(self, event)

            # Update mouse state variables.
            self._flag_mouse_down = False
            self._drag_origin_xy = None
            self._drag_delta_xy = None
            self._drag_xy = None
            self._drag_prior_mouse_xy = None

        elif event['type'] == 'wheel':
            # Mouse Wheel Event.
            # Call dispatcher.
            self._mouse_wheel_dispatcher(self, event)

        else:
            pass

    #######################################################
    # Allow user to register Python event handler functions.
    #
    # The signature for registration function is:
    #   event_type: a string identifying event type.
    #   callback : function to be called with two arguments: widget instance and event information.
    #   remove : bool (optional), set to true to unregister the callback function.
    #
    def show_mouse_event_types(self):
        """Helper function to return list of valid mouse event types.
        """
        return self._mouse_event_dispatchers.keys()

    def on_mouse(self, callback, event_type=None, remove=False):
        """Register mouse event callback function with appropriate dispatcher.
        If event_type is not specified, register with all.
        """
        if event_type:
            try:
                d = self._mouse_event_dispatchers[event_type]
            except KeyError:
                raise ValueError('Invalid event type: {}'.format(event_type))
            except:
                raise

            # Call dispatcher for user-specified event type.
            d.register_callback(callback, remove=remove)
        else:
            # Call dispatcher for all specified event types.
            for d in self._mouse_event_dispatchers.values():
                d.register_callback(callback, remove=remove)


    # def on_mouse_move(self, callback, remove=False):
    #     """Repond to mouse motion.
    #     """
    #     self._mouse_move_dispatcher.register_callback(callback, remove=remove)
    # def on_mouse_drag(self, callback, remove=False):
    #     """Repond to drag motion: motion while button is down.
    #     """
    #     self._mouse_drag_dispatcher.register_callback(callback, remove=remove)
    # def on_mouse_down(self, callback, remove=False):
    #     """Repond to mouse button down.
    #     """
    #     self._mouse_down_dispatcher.register_callback(callback, remove=remove)
    # def on_mouse_up(self, callback, remove=False):
    #     """Repond to mouse button up.
    #     """
    #     self._mouse_up_dispatcher.register_callback(callback, remove=remove)
    # def on_mouse_click(self, callback, remove=False):
    #     """Repond to mouse button click: button down followed by button up.
    #     """
    #     self._mouse_click_dispatcher.register_callback(callback, remove=remove)
    # def on_mouse_wheel(self, callback, remove=False):
    #     """Repond to mouse wheel scroll event.
    #     """
    #     self._mouse_wheel_dispatcher.register_callback(callback, remove=remove)

#################################################

# Bootstrap Widget's JavaScript code into Notebook browser environment.
_bootstrap_js()
time.sleep(0.01)  # sleep a tiny bit to give time for JavaScript stuff to set up in the background.
