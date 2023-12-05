import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from phantoms import generate_2d_phantom
from simulation import simulate_xray_transmission

class XRaySimulationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.energy_mu_map = {
            '60': {'mu_outer': '0.5', 'mu_inner': '0.3'},  # Sample values, adjust as needed
            '80': {'mu_outer': '0.6', 'mu_inner': '0.35'}, # Example values
            # We might need to ad more energy values
        }
        self
        self.initUI()

    def initUI(self):
        self.setWindowTitle('X-Ray Simulation')

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Energy Dropdown menu
        self.energy_label = QLabel('Beam Energy (keV):')
        self.layout().addWidget(self.energy_label)

        self.energy_dropdown = QComboBox()
        self.energy_dropdown.addItems(self.energy_mu_map.keys())
        self.energy_dropdown.currentTextChanged.connect(self.update_mu_vals)
        self.layout().addWidget(self.energy_dropdown)

        # X-Ray Angle
        self.angle_label = QLabel('X-Ray Angle (degrees):')
        layout.addWidget(self.angle_label)

        self.angle_entry = QLineEdit()
        self.angle_entry.setText("0.0")
        layout.addWidget(self.angle_entry)
        
        # Mu inner + outer
        self.mu_outer_label = QLabel('Attenuation Coefficient Outer (mu):')
        layout.addWidget(self.mu_outer_label)
        self.mu_outer_entry = QLineEdit()
        self.mu_outer_entry.setText("0.5")  # Set a default value or leave it empty to enforce user input
        layout.addWidget(self.mu_outer_entry)

        self.mu_inner_label = QLabel('Attenuation Coefficient Inner (mu):')
        layout.addWidget(self.mu_inner_label)
        self.mu_inner_entry = QLineEdit()
        self.mu_inner_entry.setText("0.3")  # Set a default value or leave it empty to enforce user input
        layout.addWidget(self.mu_inner_entry)
        
        # Outer Radius Dropdown Menu
        self.outer_radius_label = QLabel('Outer Radius (cm):')
        self.layout().addWidget(self.outer_radius_label)
        self.outer_radius_dropdown = QComboBox()
        self.outer_radius_dropdown.addItems(["15", "25"]) #temporary placeholder
        self.layout().addWidget(self.outer_radius_dropdown)

        # Inner Radius Dropdown Menu
        self.inner_radius_label = QLabel('Inner Radius (cm):')
        self.layout().addWidget(self.inner_radius_label)
        self.inner_radius_dropdown = QComboBox()
        self.inner_radius_dropdown.addItems(["6", "12"]) #temporary placeholder
        self.layout().addWidget(self.inner_radius_dropdown)

        # Source to Phantom Distance
        self.distance_sp_label = QLabel('Source to Phantom Distance (cm):')
        layout.addWidget(self.distance_sp_label)

        self.distance_sp_entry = QLineEdit()
        self.distance_sp_entry.setText("100.0")
        layout.addWidget(self.distance_sp_entry)

        # Source to Detector Distance
        self.distance_sd_label = QLabel('Source to Detector Distance (cm):')
        layout.addWidget(self.distance_sd_label)

        self.distance_sd_entry = QLineEdit()
        self.distance_sd_entry.setText("200.0")
        layout.addWidget(self.distance_sd_entry)

        # Material Dropdown
        self.mu_label = QLabel('Select Phantom Material:')
        layout.addWidget(self.mu_label)

        self.mu_dropdown = QComboBox()
        self.mu_options = {'Bone': 0.5}
        self.mu_dropdown.addItems(self.mu_options.keys())
        layout.addWidget(self.mu_dropdown)

        # Start Simulation Button
        self.start_button = QPushButton('Start Simulation', self)
        self.start_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_button)
        
        #Matplotlib displaying phantom
        self.canvas = FigureCanvas(Figure(figsize=(5,3)))
        layout.addWidget(self.canvas)
        
    def update_mu_vals(self, energy):
        mu_values = self.energy_mu_map[energy]
        self.mu_outer_entry.setText(mu_values['mu_outer'])
        self.mu_inner_entry.setText(mu_values['mu_inner'])

    def start_simulation(self):
        energy = float(self.energy_dropdown.currentText())
        angle = float(self.angle_entry.text())
        distance_sp = float(self.distance_sp_entry.text())
        distance_sd = float(self.distance_sd_entry.text())
        outer_radius = float(self.outer_radius_dropdown.currentText())
        inner_radius = float(self.inner_radius_dropdown.currentText())
        mu_outer = float(self.mu_outer_entry.text())
        mu_inner = float(self.mu_inner_entry.text())
        
        OUTER_VALUE = 1
        INNER_VALUE = 2

        # Generate a simple 2D phantom for the simulation
        phantom = generate_2d_phantom(
            dimensions = (100, 100),
            outer_radius = outer_radius,
            inner_radius = inner_radius,
            outer_value = OUTER_VALUE,  # These are the values used when drawing the phantom
            inner_value = INNER_VALUE
        )
        
        #Displays the phantom
        self.display_phantom(phantom)

        # Simulate the X-ray transmission and get the 1D profile
        xray_profile = simulate_xray_transmission(
            phantom,
            energy,
            angle, 
            distance_sp, 
            distance_sd, 
            mu_outer, 
            mu_inner,
            OUTER_VALUE,
            INNER_VALUE
        )

        # Display the profile
        self.display_xray_profile(xray_profile)
        
    def display_phantom(self, phantom):
        """
        Displays 2D phantom on Matplotlib canvas
        
        Parameters:
        - phantom: 2D numpy array representing the phantom.
        """
        
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.imshow(phantom, cmap='gray')
        ax.axis('off')
        self.canvas.draw()

    def display_xray_profile(self, profile):
        # Can integrate Matplotlib with PyQt for displaying the profile
        # This part will need to be adjusted for PyQt
        
        #look into this further
        import matplotlib.pyplot as plt
        plt.figure("X-Ray Profile")
        plt.plot(profile)
        plt.xlabel('Detector Position')
        plt.ylabel('Intensity')
        plt.title('Simulated X-Ray Transmission Profile')
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = XRaySimulationApp()
    ex.show()
    sys.exit(app.exec_())
