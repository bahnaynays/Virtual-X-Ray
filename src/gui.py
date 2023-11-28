import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from phantoms import generate_2d_phantom, display_phantom
from simulation import simulate_xray_transmission

class XRaySimulationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('X-Ray Simulation')

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Energy
        self.energy_label = QLabel('Beam Energy (keV):')
        layout.addWidget(self.energy_label)

        self.energy_entry = QLineEdit()
        self.energy_entry.setText("60.0")
        layout.addWidget(self.energy_entry)

        # X-Ray Angle
        self.angle_label = QLabel('X-Ray Angle (degrees):')
        layout.addWidget(self.angle_label)

        self.angle_entry = QLineEdit()
        self.angle_entry.setText("0.0")
        layout.addWidget(self.angle_entry)

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
        self.mu_options = {'Water': 0.2, 'Bone': 0.5, 'Metal': 1.0}
        self.mu_dropdown.addItems(self.mu_options.keys())
        layout.addWidget(self.mu_dropdown)

        # Start Simulation Button
        self.start_button = QPushButton('Start Simulation', self)
        self.start_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_button)

    def start_simulation(self):
        energy = float(self.energy_entry.text())
        angle = float(self.angle_entry.text())
        distance_sp = float(self.distance_sp_entry.text())
        distance_sd = float(self.distance_sd_entry.text())
        mu_value = self.mu_options[self.mu_dropdown.currentText()]

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

        # Display the profile
        self.display_xray_profile(xray_profile)

    def display_xray_profile(self, profile):
        # You can integrate Matplotlib with PyQt for displaying the profile
        # This part will need to be adjusted for PyQt
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