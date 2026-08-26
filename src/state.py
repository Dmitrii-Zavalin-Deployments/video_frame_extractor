# src/state.py
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


class State:
    def __init__(self, input_data, config_data, input_output_folder):
        logger.info("Initializing State management instance.")
        if not isinstance(input_data, dict):
            raise ValueError("Required argument 'input_data' must be a valid dictionary.")
        if not isinstance(config_data, dict):
            raise ValueError("Required argument 'config_data' must be a valid dictionary.")
        if not input_output_folder:
            raise ValueError("Required argument 'input_output_folder' is missing or empty.")

        self.inputs = input_data
        self.config = config_data

        # Results block (matches schema including status, error, and timestamp)
        self.results = {
            "status": "pending",
            "error": "",
            "date_time": datetime.now(timezone.utc).isoformat()
        }

        # Internal working directories
        self.base_dir = Path(input_output_folder)
        self.frames_dir = self.base_dir / "frames"
        self.processed_frames_dir = self.base_dir / "processed_frames"

        try:
            self.frames_dir.mkdir(parents=True, exist_ok=True)
            self.processed_frames_dir.mkdir(parents=True, exist_ok=True)
            logger.debug("Created working directories under: %s", self.base_dir)
        except OSError as e:
            logger.exception("Failed to create working directories")
            raise RuntimeError(f"Could not create working directories at {self.base_dir}: {e}") from e

        # Internal lists
        self.frame_paths = []
        self.processed_frame_paths = []

        # No-Default Policy: Retrieve output_zip_path across inputs and config
        output_zip_str = None
        if "output_zip_path" in self.inputs:
            output_zip_str = self.inputs["output_zip_path"]
        elif "output_zip_path" in self.config:
            output_zip_str = self.config["output_zip_path"]

        if not output_zip_str:
            raise ValueError("Required property 'output_zip_path' is missing from both input.json and config.json.")

        self.output_zip_path = Path(output_zip_str)
        logger.debug("Resolved output zip path: %s", self.output_zip_path)

    def to_output_json(self):
        # Refresh date_time to reflect the precise moment output json is compiled/written
        self.results["date_time"] = datetime.now(timezone.utc).isoformat()
        return {
            "inputs": self.inputs,
            "config": self.config,
            "results": self.results
        }

    def write_output_json(self, output_path):
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info("Writing final output JSON to: %s", out_path)
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(self.to_output_json(), f, indent=2)
        except OSError as e:
            logger.exception("Failed to write output JSON file")
            raise RuntimeError(f"Could not write output JSON to {out_path}: {e}") from e
