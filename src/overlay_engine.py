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

        # Transparency configurations
        overlay_alpha = float(pos["overlay_transparency"])
        background_alpha = float(pos["background_transparency"])

        # Apply background frame transparency if less than 1.0
        if background_alpha < 1.0:
            r, g, b, a = frame.split()
            a = a.point(lambda p: int(p * background_alpha))
            frame = Image.merge("RGBA", (r, g, b, a))

        # Scale overlay transparency *without* destroying its transparent background mask
        r, g, b, a = overlay_img.split()
        a = a.point(lambda p: int(p * overlay_alpha))
        overlay_img = Image.merge("RGBA", (r, g, b, a))

        # Position coordinates
        x = int(pos["x"])
        y = int(pos["y"])

        # Paste overlay onto frame using its alpha channel as the mask
        frame.paste(overlay_img, (x, y), overlay_img)

        # Convert back to RGB for safe JPEG saving
        frame = frame.convert("RGB")

        # Save processed frame
        out_path = state.processed_frames_dir / frame_path.name
        frame.save(out_path)
        state.processed_frame_paths.append(out_path)
