import numpy as np

def simulate_xray_transmission(phantom, energy, angle, distance_sp, distance_sd, mu_outer, mu_inner, outer_value, inner_value):
    """
    Simulates the X-ray transmission through a 2D cylinder phantom.

    Parameters:
    - phantom: 2D numpy array representing the phantom.
    - energy: The energy of the X-ray beam in keV (not used in this simple model).
    - angle: The angle of the X-ray beam in degrees.
    - distance_sp: The distance from the source to the phantom in cm.
    - distance_sd: The distance from the source to the detector in cm.
    - mu_outer: The attenuation coefficient for the outer cylinder.
    - mu_inner: The attenuation coefficient for the inner cylinder.


    Returns:
    - A 1D numpy array representing the X-ray transmission profile.
    
    Not even sure if this works properly yet.
    """
    # Convert angle to radians 
    angle_rad = np.deg2rad(angle)

    # Initialize image profile
    image_profile = np.zeros(phantom.shape[1])
    
    center_y = phantom.shape[0] // 2
    center_x = phantom.shape[1] // 2
    
    # Loop is based off the asumption that the phantom is centered in the array & x-ray source is alligned with the center
    for i in range(phantom.shape[1]):           #column itteration 
        if phantom[center_y, i] == inner_value:     
            mu = mu_inner
        elif phantom[center_y, i] == outer_value:
            mu = mu_outer   
        else:
            mu = 0
            
        intensity_trans = np.exp(-mu * distance_sp)
        
        # Applying geometic mag factor
        magnification_factor = distance_sd / (distance_sp + distance_sd)
        image_profile[i] = intensity_trans * magnification_factor
        
    return image_profile