# src/overlay_engine.py
import logging
from pathlib import Path
import zipfile

from PIL import Image

logger = logging.getLogger(__name__)


def run(state):
    logger.info("Starting overlay engine pipeline.")
    try:
        # No-Default Policy: Retrieve overlay_zip_path across inputs, config, and state attributes
        overlay_zip_str = None
        if hasattr(state, "inputs") and state.inputs and "overlay_zip_path" in state.inputs:
            overlay_zip_str = state.inputs["overlay_zip_path"]
        elif hasattr(state, "config") and state.config and "overlay_zip_path" in state.config:
            overlay_zip_str = state.config["overlay_zip_path"]
        elif hasattr(state, "overlay_zip_path") and state.overlay_zip_path:
            overlay_zip_str = str(state.overlay_zip_path)

        if not overlay_zip_str:
            raise ValueError("Required property 'overlay_zip_path' is missing from both input.json and config.json.")

        overlay_zip = Path(overlay_zip_str)
        logger.debug("Resolved overlay zip path: %s", overlay_zip)

        if not overlay_zip.exists():
            raise FileNotFoundError(f"Overlay ZIP file does not exist at path: {overlay_zip}")

        # No-Default Policy: Check base_dir
        base_dir = getattr(state, "base_dir", None)
        if base_dir is None:
            raise ValueError("Required attribute 'base_dir' is missing from state.")
        base_path = Path(base_dir)

        overlay_extract_dir = base_path / "overlay_images"
        overlay_extract_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Extracting overlay ZIP archive...")
        try:
            with zipfile.ZipFile(overlay_zip, "r") as zf:
                zf.extractall(overlay_extract_dir)
        except zipfile.BadZipFile as bzf:
            raise ValueError(f"Invalid or corrupted overlay zip archive: {overlay_zip}") from bzf

        # Search recursively to handle nested folders inside the zip archive
        overlay_images = sorted(list(overlay_extract_dir.rglob("*.png")))
        if not overlay_images:
            raise ValueError("No overlay PNGs found in overlay ZIP archive.")

        logger.info("Found %d overlay image(s).", len(overlay_images))

        # Validate frame_paths
        frame_paths = getattr(state, "frame_paths", [])
        if not frame_paths:
            raise ValueError("No frame paths available in state to apply overlays onto.")

        # No-Default Policy: Retrieve overlay_positions
        overlay_positions = None
        if hasattr(state, "config") and state.config and "overlay_positions" in state.config:
            overlay_positions = state.config["overlay_positions"]
        elif hasattr(state, "inputs") and state.inputs and "overlay_positions" in state.inputs:
            overlay_positions = state.inputs["overlay_positions"]
        elif hasattr(state, "overlay_positions") and state.overlay_positions:
            overlay_positions = state.overlay_positions

        if not overlay_positions:
            raise ValueError("Required property 'overlay_positions' is missing from config.json and input.json.")

        # Validate processed_frames_dir
        processed_frames_dir = getattr(state, "processed_frames_dir", None)
        if processed_frames_dir is None:
            raise ValueError("Required attribute 'processed_frames_dir' is missing from state.")
        processed_frames_path = Path(processed_frames_dir)
        processed_frames_path.mkdir(parents=True, exist_ok=True)

        if not hasattr(state, "processed_frame_paths") or state.processed_frame_paths is None:
            state.processed_frame_paths = []

        # Dynamically compute frames_per_image based on total frame count and number of overlay images
        total_frames = len(frame_paths)
        num_images = len(overlay_images)
        rem = total_frames % num_images
        next_multiple = total_frames if rem == 0 else total_frames + (num_images - rem)
        frames_per_image = next_multiple // num_images
        logger.debug("Computed frames_per_image: %d (Total frames: %d, Overlays: %d)", frames_per_image, total_frames, num_images)

        # Apply overlays
        logger.info("Applying overlays to %d frame(s)...", total_frames)
        for i, frame_path in enumerate(frame_paths):
            frame_path_obj = Path(frame_path)
            if not frame_path_obj.exists():
                logger.warning("Frame file does not exist on disk: %s", frame_path_obj)
                continue

            frame = Image.open(frame_path_obj).convert("RGBA")

            overlay_index = min(i // frames_per_image, num_images - 1)
            overlay_img = Image.open(overlay_images[overlay_index]).convert("RGBA")

            pos_index = min(i // frames_per_image, len(overlay_positions) - 1)
            pos = overlay_positions[pos_index]

            required_keys = ["overlay_transparency", "background_transparency", "x", "y"]
            for rk in required_keys:
                if rk not in pos:
                    raise KeyError(f"Missing required key '{rk}' in overlay_positions configuration at index {pos_index}.")

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
            out_path = processed_frames_path / frame_path_obj.name
            frame.save(out_path)
            state.processed_frame_paths.append(out_path)

        if not state.processed_frame_paths:
            raise RuntimeError("No frames were successfully processed by the overlay engine.")

        logger.info("Successfully processed %d frame(s) with overlays.", len(state.processed_frame_paths))

        if not hasattr(state, "results") or state.results is None:
            state.results = {}
        state.results["status"] = "success"
        state.results["error"] = ""

    except (OSError, ValueError, KeyError, RuntimeError, TypeError) as e:
        logger.exception("Exception encountered during overlay execution")
        if not hasattr(state, "results") or state.results is None:
            state.results = {}
        state.results["status"] = "error"
        state.results["error"] = str(e)
