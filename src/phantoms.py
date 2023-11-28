import numpy as np
import matplotlib.pyplot as plt

def generate_2d_phantom(dimensions, outer_rect, inner_rect, outer_value=1, inner_value=2):
    """
    Generates a 2D phantom with a rectangle inside another rectangle. That's basically a 2d thigh

    Parameters:
    - dimensions: a tuple (height, width) for the size of the phantom.
    - outer_rect: a tuple (top_left, bottom_right) specifying the outer rectangle.
    - inner_rect: a tuple (top_left, bottom_right) specifying the inner rectangle.
    - outer_value: the value to fill in the outer rectangle.
    - inner_value: the value to fill in the inner rectangle.

    Returns:
    - A 2D numpy array representing the phantom with rectangles.
    """
    phantom = np.zeros(dimensions)

    # Draw outer rectangle
    outer_top_left, outer_bottom_right = outer_rect
    phantom[outer_top_left[0]:outer_bottom_right[0], outer_top_left[1]:outer_bottom_right[1]] = outer_value

    # Draw inner rectangle
    inner_top_left, inner_bottom_right = inner_rect
    phantom[inner_top_left[0]:inner_bottom_right[0], inner_top_left[1]:inner_bottom_right[1]] = inner_value

    return phantom
