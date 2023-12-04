import numpy as np
import matplotlib.pyplot as plt

def generate_2d_phantom(dimensions, outer_radius, inner_radius, outer_value, inner_value):
    """
    Generates a 2D phantom with a cylinder inside another cylinder. That's basically a 2d thigh

    Parameters:
    - dimensions: a tuple (height, width) for the size of the phantom.
    - outer_radius: the radius of the outer cylinder.
    - inner_radius: the radius of the inner cylinder.
    - outer_value: the value to fill in the outer cylinder.
    - inner_value: the value to fill in the inner cylinder.

    Returns:
    - A 2D numpy array representing the phantom with cylindrical regions.
    """
    
    phantom = np.zeros(dimensions)
    center = (dimensions[0] // 2, dimensions[1] // 2)

    for y in range(dimensions[0]):
        for x in range(dimensions[1]):
            dist_from_center = np.sqrt((x - center[1]) ** 2 + (y - center[0]) ** 2)
            
            if dist_from_center < inner_radius:
                phantom[y, x] = inner_value
            
            elif dist_from_center < outer_radius:
                phantom[y, x] = outer_value
    
    return phantom
