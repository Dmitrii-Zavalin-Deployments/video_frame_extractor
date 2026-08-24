# src/overlay_engine.py
import zipfile
from pathlib import Path
from PIL import Image

def run(state):
    # Unzip overlay images
    overlay_zip = state.inputs["overlay_zip_path"]
    overlay_extract_dir = state.base_dir / "overlay_images"
    overlay_extract_dir.mkdir(exist_ok=True)

    with zipfile.ZipFile(overlay_zip, "r") as zf:
        zf.extractall(overlay_extract_dir)

    # Search recursively to handle nested folders inside the zip archive
    overlay_images = sorted(list(overlay_extract_dir.rglob("*.png")))
    if not overlay_images:
        raise ValueError("No overlay PNGs found in overlay ZIP.")

    frames_per_image = state.config["frames_per_image"]
    overlay_positions = state.config["overlay_positions"]

    # Apply overlays
    for i, frame_path in enumerate(state.frame_paths):
        frame = Image.open(frame_path).convert("RGBA")

        overlay_index = min(i // frames_per_image, len(overlay_images) - 1)
        overlay_img = Image.open(overlay_images[overlay_index]).convert("RGBA")

        pos_index = min(i // frames_per_image, len(overlay_positions) - 1)
        pos = overlay_positions[pos_index]

        # Transparency
        overlay_alpha = pos["overlay_transparency"]
        background_alpha = pos["background_transparency"]

        # Apply background transparency
        frame = frame.copy()
        frame.putalpha(int(background_alpha * 255))

        # Resize overlay if needed (pitch/roll/yaw ignored for now)
        overlay_img = overlay_img.copy()
        overlay_img.putalpha(int(overlay_alpha * 255))

        # Position
        x = int(pos["x"])
        y = int(pos["y"])

        frame.paste(overlay_img, (x, y), overlay_img)

        # Save processed frame
        out_path = state.processed_frames_dir / frame_path.name
        frame.save(out_path)
        state.processed_frame_paths.append(out_path)
