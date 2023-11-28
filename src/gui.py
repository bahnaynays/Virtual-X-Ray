import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt

from simulation import simulate_xray_transmission
from phantoms import generate_2d_phantom, display_phantom

class XRaySimulationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('X-Ray Simulation')

        # Energy selection
        self.energy_label = tk.Label(self, text='Beam Energy (keV):')
        self.energy_label.pack()

        self.energy_var = tk.DoubleVar(value=60.0)  # Default value
        self.energy_entry = tk.Entry(self, textvariable=self.energy_var)
        self.energy_entry.pack()

        # X-Ray angle selection
        self.angle_label = tk.Label(self, text='X-Ray Angle (degrees):')
        self.angle_label.pack()

        self.angle_var = tk.DoubleVar(value=0.0)  # Default value
        self.angle_entry = tk.Entry(self, textvariable=self.angle_var)
        self.angle_entry.pack()

        # Distance from source to phantom
        self.distance_sp_label = tk.Label(self, text='Source to Phantom Distance (cm):')
        self.distance_sp_label.pack()

        self.distance_sp_var = tk.DoubleVar(value=100.0)  # Default value
        self.distance_sp_entry = tk.Entry(self, textvariable=self.distance_sp_var)
        self.distance_sp_entry.pack()

        # Distance from source to film (detector)
        self.distance_sd_label = tk.Label(self, text='Source to Detector Distance (cm):')
        self.distance_sd_label.pack()

        self.distance_sd_var = tk.DoubleVar(value=200.0)  # Default value
        self.distance_sd_entry = tk.Entry(self, textvariable=self.distance_sd_var)
        self.distance_sd_entry.pack()

        # Dropdown for μ values
        self.mu_label = tk.Label(self, text='Select Phantom Material:')
        self.mu_label.pack()

        self.mu_options = {'Water': 0.2, 'Bone': 0.5, 'Metal': 1.0}  # Example values
        self.mu_var = tk.StringVar(value='Water')  # Default selection
        self.mu_dropdown = ttk.Combobox(self, textvariable=self.mu_var, values=list(self.mu_options.keys()))
        self.mu_dropdown.pack()

        # Start simulation button
        self.start_button = tk.Button(self, text='Start Simulation', command=self.start_simulation)
        self.start_button.pack()

def start_simulation(self):
        energy = self.energy_var.get()
        angle = self.angle_var.get()
        distance_sp = self.distance_sp_var.get()
        distance_sd = self.distance_sd_var.get()
        mu_value = self.mu_options[self.mu_var.get()]

        # Generate a simple 2D phantom for the simulation
        phantom = generate_2d_phantom(
            dimensions=(100, 100),
            object_centers=[(50, 50)],
            object_radii=[20]
        )
        
        # Simulate the X-ray transmission and get the 1D profile
        xray_profile = simulate_xray_transmission(
            phantom, energy, angle, distance_sp, distance_sd, mu_value
        )
        
        # Now we need to display this profile, let's use matplotlib for simplicity
        self.display_xray_profile(xray_profile)

def display_xray_profile(self, profile):
    plt.figure("X-Ray Profile")
    plt.plot(profile)
    plt.xlabel('Detector Position')
    plt.ylabel('Intensity')
    plt.title('Simulated X-Ray Transmission Profile')
    plt.show()