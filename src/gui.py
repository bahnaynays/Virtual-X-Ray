import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from phantoms import generate_2d_phantom
from simulation import simulate_xray_transmission
from phantoms import create_leg_phantom, add_orthogonal_split, generate_xray_image, add_fracture

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
        
        # Creates 3d leg phantom
        dimensions = (256, 256, 256)
        leg_radius = 100
        bone_radius = 50
        leg_phantom = create_leg_phantom(dimensions, leg_radius, bone_radius)
        
        # Fracture
        split_depth = 64
        fracture = True
        
        if fracture:
            leg_phantom = add_orthogonal_split(leg_phantom, split_depth)
            orthogonal_fracture_phantom = add_fracture(leg_phantom, bone_radius, split_width=5, angle=0)
            angled_fracture_phantom = add_fracture(leg_phantom, bone_radius, split_width=5, angle=45)
        
        #generate 2D X-ray image from the phantom
        xray_image = generate_xray_image(leg_phantom)
        
        self.display_xray_image(xray_image)
        
        # Display fractures
        self.display_fractures(orthogonal_fracture_phantom, angled_fracture_phantom, slice_index=128)

        
        # Shows a 3D leg phantom slice on it's own window
        self.display_3d_leg_phantom_slice(leg_phantom, slice_index=128)


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
        
    def display_fractures(self, orthogonal_fracture_phantom, angled_fracture_phantom, slice_index):
    
        self.fractures_dialog = QDialog(self)
        self.fractures_dialog.setWindowTitle("Leg Phantom Fractures")
        fractures_layout = QVBoxLayout()
        fractures_canvas = FigureCanvas(Figure(figsize=(10, 5)))  # Adjust the size as needed
        fractures_layout.addWidget(fractures_canvas)
        self.fractures_dialog.setLayout(fractures_layout)
    
        # Setup the plots for orthogonal and angled fractures
        ax1 = fractures_canvas.figure.add_subplot(121)
        ax2 = fractures_canvas.figure.add_subplot(122)
    
        # Display orthogonal fracture slice
        ax1.imshow(orthogonal_fracture_phantom[slice_index, :, :], cmap='gray')
        ax1.set_title('Orthogonal Fracture')
        ax1.axis('off')

        # Display angled fracture slice
        ax2.imshow(angled_fracture_phantom[slice_index, :, :], cmap='gray')
        ax2.set_title('Angled Fracture')
        ax2.axis('off')
    
        # Draw the canvas and show the dialog
        fractures_canvas.draw()
        self.fractures_dialog.show()
        
    def display_3d_leg_phantom_slice(self, phantom_3d, slice_index):
        """
        Displays a 2D slice of the 3D leg phantom on the Matplotlib canvas.
        
        Parameters:
        - phantom_3d: 3D numpy array representing the leg phantom.
        - slice_index: Index of the slice to be displayed.
        """
        #print(f"Slice {slice_index} value range: {np.min(phantom_3d[slice_index])} to {np.max(phantom_3d[slice_index])}")

        min_val = np.min(phantom_3d)
        max_val = np.max(phantom_3d)

        # Show the dialog
        self.leg_phantom_slice_dialog = QDialog(self)
        self.leg_phantom_slice_dialog.setWindowTitle("3D Leg Phantom Slice")
        leg_phantom_slice_layout = QVBoxLayout()
        leg_phantom_slice_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        leg_phantom_slice_layout.addWidget(leg_phantom_slice_canvas)
        self.leg_phantom_slice_dialog.setLayout(leg_phantom_slice_layout)
        leg_phantom_slice_ax = leg_phantom_slice_canvas.figure.add_subplot(111)

        # Display the slice using the grayscale colormap and appropriate vmin and vmax
        leg_phantom_slice_ax.imshow(phantom_3d[slice_index, :, :], cmap='gray', vmin=min_val, vmax=max_val)
        leg_phantom_slice_ax.axis('off')
        leg_phantom_slice_canvas.draw()
        self.leg_phantom_slice_dialog.show()
        
        
        
    def display_xray_image(self, xray_image):
        # Create a separate window for the X-ray image
        self.xray_image_dialog = QDialog(self)
        self.xray_image_dialog.setWindowTitle("X-Ray Image")
        xray_image_layout = QVBoxLayout()
        xray_image_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        xray_image_layout.addWidget(xray_image_canvas)
        self.xray_image_dialog.setLayout(xray_image_layout)
        xray_image_ax = xray_image_canvas.figure.add_subplot(111)
        xray_image_ax.imshow(xray_image, cmap='gray')
        xray_image_ax.axis('off')
        xray_image_canvas.draw()
        self.xray_image_dialog.show()
        
    def display_phantom(self, phantom):
        """
        Displays 2D phantom on Matplotlib canvas
        
        Parameters:
        - phantom: 2D numpy array representing the phantom.
        """
        
       # Create a separate window for the 2D phantom
        self.phantom_dialog = QDialog(self)
        self.phantom_dialog.setWindowTitle("2D Phantom")
        phantom_layout = QVBoxLayout()
        phantom_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        phantom_layout.addWidget(phantom_canvas)
        self.phantom_dialog.setLayout(phantom_layout)
        phantom_ax = phantom_canvas.figure.add_subplot(111)
        phantom_ax.imshow(phantom, cmap='gray')
        phantom_ax.axis('off')
        phantom_canvas.draw()
        self.phantom_dialog.show()

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
