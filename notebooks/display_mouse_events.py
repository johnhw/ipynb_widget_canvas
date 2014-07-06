
from __future__ import print_function, unicode_literals, division

import IPython
from IPython.html.widgets import HTMLWidget, TextareaWidget, ContainerWidget

import widget_canvas as canvas

# Bootstrap styles
# http://getbootstrap.com/components/#labels
style_A = 'label label-default'
style_B = 'label label-primary'
style_C = 'label label-success'
style_D = 'label label-info'
style_E = 'label label-warning'
style_F = 'label label-danger'


def display(image):
    """
    Build a simple compound display for playing with mouse events.
    """

    #############################################
    # Create the widgets.

    # Image widget.
    wid_image = canvas.ImageWidget(image)
    wid_image.set_css({'border': 'solid black 1px'})

    # Mouse X & Y canvas coordinates.
    wid_move_XY = HTMLWidget(value='XY:')
    wid_move_XY.set_css({'width': '250px', 'margin-left': '10px', 'font-family': 'monospace'})

    wid_drag_XY = HTMLWidget(value='XY:')
    wid_drag_XY.set_css({'width': '250px', 'margin-left': '10px', 'font-family': 'monospace'})

    # Status indicators.
    wid_move = HTMLWidget(value='Move')
    wid_move.set_css({'width': '35px'})

    wid_drag = HTMLWidget(value='Drag')
    wid_drag.set_css({'width': '35px'})

    wid_down_up = HTMLWidget(value='Button: Up')
    wid_down_up.set_css({'width': '100px'})

    wid_click = HTMLWidget(value='Click')
    wid_scroll = HTMLWidget(value='Scroll')

    # Event information.
    wid_event_text = TextareaWidget()
    wid_event_text.set_css({'width': '500', 'height': '130', 'font-family': 'monospace'})

    #############################################
    # Assemble widgets inside containers.
    container_move = ContainerWidget(children=[wid_move, wid_move_XY])
    container_drag = ContainerWidget(children=[wid_drag, wid_drag_XY])

    container_info = ContainerWidget(children=[container_move, container_drag, wid_down_up,
                                               wid_click, wid_scroll, wid_event_text])
    container_info.set_css({'margin-left': '10px'})

    container_main = ContainerWidget(children=[wid_image, container_info])

    #############################################
    # Build event handlers.
    def handle_event(ev):
        """Just a generic event handler."""
        wid_event_text.value = 'Event:\n{}'.format(ev)

    def handle_motion(ev):
        wid_move.value = '<b>Move</b>'
        X, Y = ev['canvas_xy']
        wid_move_XY.value = 'XY: {:04.0f}, {:04.0f}'.format(X, Y)

        wid_drag.value = 'Drag'
        wid_drag_XY.value = 'XY:'

    def handle_drag(ev):
        wid_move.value = 'Move'
        wid_drag.value = '<b>Drag</b>'
        X, Y = ev['drag_xy']

        wid_drag_XY.value = 'XY: {:04.0f}, {:04.0f}'.format(X, Y)
        wid_move_XY.value = 'XY:'

    def handle_down(ev):
        wid_down_up.value = 'Button: Down'

    def handle_up(ev):
        wid_down_up.value = 'Button: Up'

    _click_classes = [style_E, style_F]
    ix = [0]

    def handle_click(ev):
        wid_click.remove_class(_click_classes[ix[0]])

        ix[0] = (ix[0] + 1) % 2
        wid_click.add_class(_click_classes[ix[0]])

    _scroll_classes = [style_B, style_C]
    iw = [0]

    def handle_scroll(ev):
        wid_scroll.remove_class(_scroll_classes[iw[0]])

        iw[0] = (iw[0] + 1) % 2
        wid_scroll.add_class(_scroll_classes[iw[0]])

    #############################################
    # Attach event handlers.
    wid_image.on_mouse_move(handle_motion)
    wid_image.on_mouse_move(handle_event)

    wid_image.on_mouse_drag(handle_drag)
    wid_image.on_mouse_drag(handle_event)

    wid_image.on_mouse_down(handle_down)
    wid_image.on_mouse_down(handle_event)

    wid_image.on_mouse_up(handle_up)
    wid_image.on_mouse_up(handle_event)

    wid_image.on_mouse_click(handle_click)
    wid_image.on_mouse_click(handle_event)

    wid_image.on_mouse_wheel(handle_scroll)
    wid_image.on_mouse_wheel(handle_event)

    #############################################
    # Display the widgets.
    IPython.display.display(container_main)

    # Change class values after widget has been displayed to screen.
    wid_click.add_class(_click_classes[ix[0]])
    wid_scroll.add_class(_scroll_classes[iw[0]])

    # List of widgets to be set to `hbox` style.
    mod_hbox = [container_main, container_move, container_drag]
    for w in mod_hbox:
        w.remove_class('vbox')
        w.add_class('hbox')

    return wid_image
