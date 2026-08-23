import pyvista as pv
import numpy as np
import json
import os

# Configuration
DATA_FILE = "data/testing-input-output/fluid_dynamics_animation.json"
OUTPUT_FOLDER = "frames"
FRAME_SIZE = (1920, 1080)  # 1080p resolution

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load fluid simulation data
with open(DATA_FILE, "r") as f:
    simulation_data = json.load(f)

# Initialize PyVista plotter
plotter = pv.Plotter(off_screen=True)

# Process each frame
for i, frame in enumerate(simulation_data["frames"]):
    # Create a structured grid from fluid dynamics data
    grid = pv.StructuredGrid(frame["x"], frame["y"], frame["z"])
    
    # Apply velocity as scalar field for visualization
    plotter.clear()
    plotter.add_mesh(grid, scalars=frame["velocity"], cmap="coolwarm")

    # Configure camera and lighting
    plotter.camera_position = "yz"
    plotter.enable_lightkit()
    plotter.show_axes()

    # Save frame as PNG
    frame_path = os.path.join(OUTPUT_FOLDER, f"frame_{i:04d}.png")
    plotter.screenshot(frame_path)

    print(f"Rendered frame {i+1}/{len(simulation_data['frames'])}")

print("✅ All frames rendered successfully!")



