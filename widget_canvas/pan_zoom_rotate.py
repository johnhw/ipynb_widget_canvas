
from __future__ import division, print_function, unicode_literals

"""
Example helper functions that demonstrate connecting 2D affine transforms to mouse events.  Note
that these are NOT all meant to be used simultaneously.
"""

import numpy as np


def update(widget):
    """
    A little helper function to make applying new transforms less mysterious.
    """
    widget._transform = widget.transform.values


def reset(widget):
    """
    Reset widget transform back to identity matrix.
    """
    widget.transform.reset()
    update(widget)


def handle_scroll_to_zoom(widget, ev):
    """
    Take care of processing mouse wheel scroll events and calling widget's zoom transform
    functions.
    """

    # On my mouse I register values of either +100 or -100.  Sometimes with smooth scrolling
    # enabled in the browser I see a large number of scroll events with values closer to
    # +/- 1 or 2.
    amount = ev['deltaY']/100.  # vertical motion values from scroll wheel

    if amount == 0:
        # Do nothing.
        return

    # Discrete change in zoom level per unit scroll amount.
    factor = 1.1

    if amount > 0:
        scl = amount * factor
    else:
        scl = 1. / (amount * factor)

    # Current cursor location about which to center zoom transform.
    x_window, y_window = ev['canvas_xy']

    Q = widget.transform.invert(copy=True)
    x_data, y_data = Q.transform_point(x_window, y_window)

    # Chain together multiple transforms, then apply to model.
    widget.transform.translate(x_data, y_data).scale(scl).translate(-x_data, -y_data)

    update(widget)


def handle_scroll_to_rotate(widget, ev):
    """
    Take care of processing mouse wheel scroll events and calling widget's rotation transform
    functions.
    """

    # On my mouse I register values of either +100 or -100.  Sometimes with smooth scrolling
    # enabled in the browser I see a large number of scroll events with values closer to
    # +/- 1 or 2.
    amount = ev['deltaY']/100.  # vertical motion values from scroll wheel

    if amount == 0:
        # Do nothing.
        return

    # Discrete change in angle per unit scroll amount.
    theta_unit_deg = 10.  # degrees

    theta_applied = np.deg2rad(amount * theta_unit_deg)

    # Current cursor location about which to center zoom transform.
    x_window, y_window = ev['canvas_xy']

    Q = widget.transform.invert(copy=True)
    x_data, y_data = Q.transform_point(x_window, y_window)

    # Chain together multiple transforms, then apply to model.
    widget.transform.translate(x_data, y_data).rotate(theta_applied).translate(-x_data, -y_data)

    update(widget)


def handle_drag_to_pan(widget, ev):
    """
    Take care of processing mouse drqag events and calling widget's offset transform functions.
    """
    dx_window, dy_window = ev['drag_delta_xy']

    # Compute translation in data coordinates.
    Q = widget.transform.invert(copy=True)
    x0_data, y0_data = Q.m13, Q.m23
    dx_data, dy_data = Q.transform_point(dx_window, dy_window)

    # Apply translation to model.
    widget.transform.translate(dx_data-x0_data, dy_data-y0_data)

    update(widget)
