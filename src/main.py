# src/main.py
import argparse
import json
import logging
from pathlib import Path

from jsonschema import ValidationError, validate

import frame_extractor
import overlay_engine
import zip_builder
from state import State

logger = logging.getLogger(__name__)


def load_json(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Required JSON file not found at path: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_schema(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Required schema file not found at path: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    # Configure basic logging for CLI/CI execution if not configured elsewhere
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    parser = argparse.ArgumentParser(description="Run media processing and packaging pipeline.")
    parser.add_argument("--input_output_folder", required=True)
    parser.add_argument("--input_file_name", required=True)
    parser.add_argument("--output_file_name", required=True)
    args = parser.parse_args()

    logger.info("Initializing pipeline execution framework.")
    base = Path(args.input_output_folder)

    input_json_path = base / args.input_file_name
    config_json_path = Path("config/config.json")
    output_json_path = base / args.output_file_name

    try:
        # No-Default Policy / Strict loading of inputs and configurations
        logger.info("Loading input configuration and operational payloads...")
        input_data = load_json(input_json_path)
        config_data = load_json(config_json_path)

        logger.info("Validating input data and configuration against strict schemas...")
        validate(input_data, load_schema("schema/input_schema.json"))
        validate(config_data, load_schema("schema/config_schema.json"))

    except (ValidationError, FileNotFoundError, json.JSONDecodeError) as e:
        logger.exception("Schema validation or file loading failed")
        error_state = {
            "inputs": locals().get("input_data", {}),
            "config": locals().get("config_data", {}),
            "results": {
                "status": "error",
                "error": str(e)
            }
        }
        output_json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(error_state, f, indent=2)
        return

    # Create state instance
    logger.info("Initializing operational state instance...")
    state = State(input_data, config_data, args.input_output_folder)

    # Run pipeline stages sequentially under strict monitoring
    stages = [
        ("Frame Extractor", frame_extractor.run),
        ("Overlay Engine", overlay_engine.run),
        ("Zip Builder", zip_builder.run)
    ]

    for stage_name, stage_func in stages:
        logger.info("Executing pipeline stage: %s", stage_name)
        stage_func(state)
        if hasattr(state, "results") and state.results and state.results.get("status") == "error":
            logger.error("Pipeline failed at stage '%s' with error: %s", stage_name, state.results.get("error"))
            state.write_output_json(output_json_path)
            return

    # Write final successful output.json
    logger.info("Pipeline completed successfully. Writing final output state to %s", output_json_path)
    state.write_output_json(output_json_path)


if __name__ == "__main__":  # pragma: no cover
    main()
