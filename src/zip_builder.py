# src/zip_builder.py
import logging
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)


def run(state):
    logger.info("Starting zip builder pipeline.")
    try:
        # No-Default Policy: Retrieve output_zip_path across state attributes, inputs, and config
        output_zip_path = getattr(state, "output_zip_path", None)
        if not output_zip_path:
            if hasattr(state, "inputs") and state.inputs and "output_zip_path" in state.inputs:
                output_zip_path = Path(state.inputs["output_zip_path"])
            elif hasattr(state, "config") and state.config and "output_zip_path" in state.config:
                output_zip_path = Path(state.config["output_zip_path"])

        if not output_zip_path:
            raise ValueError("Required property 'output_zip_path' is missing from state, inputs, and config.")

        output_zip = Path(output_zip_path)
        output_zip.parent.mkdir(parents=True, exist_ok=True)
        logger.debug("Resolved output zip path: %s", output_zip)

        # No-Default Policy: Validate processed_frame_paths
        processed_frame_paths = getattr(state, "processed_frame_paths", [])
        if not processed_frame_paths:
            raise ValueError("No processed frame paths provided in state to archive.")

        logger.info("Creating ZIP archive containing %d processed frame(s)...", len(processed_frame_paths))
        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            for frame_path in processed_frame_paths:
                frame_path_obj = Path(frame_path)
                if not frame_path_obj.exists():
                    raise FileNotFoundError(f"Processed frame file does not exist on disk: {frame_path_obj}")
                zf.write(frame_path_obj, arcname=frame_path_obj.name)

        logger.info("Successfully created and finalized ZIP archive at: %s", output_zip)

        if not hasattr(state, "results") or state.results is None:
            state.results = {}
        state.results["status"] = "success"
        state.results["error"] = ""

    except (OSError, ValueError, KeyError, RuntimeError) as e:
        logger.exception("Exception encountered during ZIP building")
        if not hasattr(state, "results") or state.results is None:
            state.results = {}
        state.results["status"] = "error"
        state.results["error"] = str(e)
