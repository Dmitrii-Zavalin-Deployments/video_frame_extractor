import os
import subprocess

# Define paths
LOCAL_FOLDER = "./BlenderInputFiles"
OUTPUT_FOLDER = "./RenderedOutput"

def run_blender_render():
    """Executes Blender rendering in CLI mode with optimized settings."""
    
    print("🔄 Starting enhanced Blender rendering process...")

    # Ensure output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Find .blend files
    blend_files = [f for f in os.listdir(LOCAL_FOLDER) if f.endswith(".blend")]

    if not blend_files:
        print("⚠️ No .blend files found! Skipping rendering.")
        return  # Gracefully exit

    # Select first .blend file
    blend_file = os.path.join(LOCAL_FOLDER, blend_files[0])

    # Construct Blender command with embedded Python execution
    blender_script = f"""
import bpy

# Load the .blend file
bpy.ops.wm.open_mainfile(filepath='{blend_file}')

# Auto-detect main object to render
scene_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
if not scene_objects:
    print("❌ No renderable objects found! Exiting.")
    quit()

obj = scene_objects[0]  # Select first detected mesh

# Apply transformations
obj.scale *= 1.5
obj.rotation_euler.z += 3.14 / 4  # Smooth rotation

# Ensure lighting setup
light_name = 'AutoSunLight'
if not bpy.data.objects.get(light_name):
    light_data = bpy.data.lights.new(name=light_name, type='SUN')
    light_object = bpy.data.objects.new(name=light_name, object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    light_object.location = (5, -5, 5)  # Positioning light dynamically

# Optimize render settings
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 256  # Higher samples for better quality

# Render frames dynamically
frame_start = bpy.context.scene.frame_start
frame_end = bpy.context.scene.frame_end

print(f"Rendering {frame_end - frame_start + 1} frames...")
for frame in range(frame_start, frame_end + 1):
    bpy.context.scene.frame_set(frame)
    bpy.context.scene.render.filepath = '{OUTPUT_FOLDER}/frame_' + str(frame).zfill(4)
    bpy.ops.render.render(write_still=True)

print("✅ Blender rendering process completed successfully!")
"""

    # Execute Blender command in CLI mode
    command = f"blender -b {blend_file} --python-expr \"{blender_script}\""
    subprocess.run(command, shell=True, check=True)

if __name__ == "__main__":
    run_blender_render()



