import numpy as np

def simulate_xray_transmission(phantom, energy, angle, distance_sp, distance_sd, mu_value):
    """
    Simulates the X-ray transmission through a 2D phantom.

    Parameters:
    - phantom: 2D numpy array representing the phantom.
    - energy: The energy of the X-ray beam in keV (not used in this simple model).
    - angle: The angle of the X-ray beam in degrees.
    - distance_sp: The distance from the source to the phantom in cm.
    - distance_sd: The distance from the source to the detector in cm.
    - mu_value: The attenuation coefficient for the material.

    Returns:
    - A 1D numpy array representing the X-ray transmission profile.
    """
    # Convert angle to radians for computation
    angle_rad = np.deg2rad(angle)

    # Calculate the path length within the phantom for each X-ray
    path_lengths = np.linalg.norm(phantom.shape) / np.cos(angle_rad)  # Simplified for demonstration

    # Apply the exponential attenuation model
    intensity_initial = 1.0  # Let's assume the initial intensity is 1 for simplicity
    intensity_transmitted = intensity_initial * np.exp(-mu_value * path_lengths)

    # The "image" in this case is a 1D profile since we have a 2D phantom
    image_profile = intensity_transmitted

    # Account for the geometric magnification factor
    magnification_factor = distance_sd / distance_sp
    image_profile *= magnification_factor

    return image_profile