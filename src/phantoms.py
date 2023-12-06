import numpy as np
import matplotlib.pyplot as plt

def create_leg_phantom(dimensions, leg_radius, bone_radius, leg_value = 1, bone_value = 2):
    """
    Creates a 3D matrix representing a leg phantom with a cylindrical leg and bone.

    Parameters:
    - dimensions: Tuple of (depth, height, width), the size of the 3D phantom.
    - leg_radius: Radius of the leg cylinder.
    - bone_radius: Radius of the bone cylinder.
    - leg_value: Value to assign to the leg area in the phantom.
    - bone_value: Value to assign to the bone area in the phantom.

    Returns:
    - 3D numpy array representing the leg phantom.
    """
    phantom = np.zeros(dimensions)
    center = (dimensions[1] // 2, dimensions[2] // 2)

    for z in range(dimensions[0]):
        for y in range(dimensions[1]):
            for x in range(dimensions[2]):
                dist_from_center = np.sqrt((x - center[1])**2 + (y - center[0])**2)
                if dist_from_center < bone_radius:
                    phantom[z, y, x] = bone_value
                elif dist_from_center < leg_radius:
                    phantom[z, y, x] = leg_value
    return phantom

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


def add_orthogonal_split(phantom, split_depth, split_value = 0):
    """
    Adds an orthogonal split to the 3D leg phantom to simulate a fracture.

    Parameters:
    - phantom: 3D numpy array representing the leg phantom.
    - split_depth: Depth at which the split starts in the z-axis.
    - split_value: Value to assign to the split area in the phantom.

    Returns:
    - 3D numpy array representing the leg phantom with an orthogonal split.
    """
    
    bone_value = 2
    
    for z in range(split_depth, phantom.shape[0]):
        bone_areas = phantom[z] >= bone_value
        phantom[z, bone_areas] = split_value
        
    return phantom

def generate_xray_image(phantom_3d):
    """
    Generates a 2D X-ray image by summing the 3D phantom along the depth axis.

    Parameters:
    - phantom_3d: 3D numpy array representing the leg phantom.

    Returns:
    - 2D numpy array representing the X-ray image.
    """
    
    return np.sum(phantom_3d, axis=0)