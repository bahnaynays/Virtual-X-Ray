import numpy as np
import matplotlib.pyplot as plt

def generate_2d_phantom(dimensions, object_centers, object_radii):
    #generates 2d phantom with circular objects
    
    phantom = np.zeros(dimensions)
    for center, radius in zip(object_centers, object_radii):
        for y in range(dimensions[1]):
            for x in range(dimensions[0]):
                if(x - center[0])**2 + (y - center[1])**2 < radius**2:
                    phantom[y,x] = 1
                    
    return phantom

def display_phantom(phantom):
    plt.imshow(phantom, cmap='gray')
    plt.axis('off')
    plt.show()
    
