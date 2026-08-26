# tests/conftest.py
import json
import zipfile

import cv2
import numpy as np
import pytest
from PIL import Image


@pytest.fixture
def setup_pipeline_environment(tmp_path, monkeypatch):
    """Sets up a complete working directory structure with real synthetic video,

    overlay ZIP archive, configuration, and schemas for direct main execution.
    """
    # Change working directory to tmp_path so config/ and schema/ are resolved cleanly
    monkeypatch.chdir(tmp_path)

    # 1. Create directory structure
    schema_dir = tmp_path / "schema"
    config_dir = tmp_path / "config"
    data_dir = tmp_path / "data" / "testing-input-output"

    schema_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    # 2. Generate JSON schemas
    input_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "background_video_path": {"type": "string"},
            "overlay_zip_path": {"type": "string"},
            "output_zip_path": {"type": "string"}
        },
        "required": ["background_video_path", "overlay_zip_path", "output_zip_path"]
    }
    (schema_dir / "input_schema.json").write_text(json.dumps(input_schema), encoding="utf-8")

    config_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "overlay_positions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "overlay_transparency": {"type": "number"},
                        "background_transparency": {"type": "number"},
                        "x": {"type": "integer"},
                        "y": {"type": "integer"}
                    },
                    "required": ["overlay_transparency", "background_transparency", "x", "y"]
                }
            }
        },
        "required": ["overlay_positions"]
    }
    (schema_dir / "config_schema.json").write_text(json.dumps(config_schema), encoding="utf-8")

    # 3. Generate config.json
    config_data = {
        "overlay_positions": [
            {
                "overlay_transparency": 0.8,
                "background_transparency": 1.0,
                "x": 10,
                "y": 10
            }
        ]
    }
    (config_dir / "config.json").write_text(json.dumps(config_data), encoding="utf-8")

    # 4. Synthesize a valid MP4 video using OpenCV
    video_path = data_dir / "sample_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(video_path), fourcc, 5.0, (100, 100))
    for i in range(5):
        frame = np.full((100, 100, 3), i * 40, dtype=np.uint8)
        out.write(frame)
    out.release()

    # 5. Synthesize a valid overlay ZIP file containing PNGs
    overlay_png_path = data_dir / "overlay_temp.png"
    img = Image.new("RGBA", (50, 50), color=(255, 0, 0, 128))
    img.save(overlay_png_path)

    overlay_zip_path = data_dir / "overlays.zip"
    with zipfile.ZipFile(overlay_zip_path, "w") as zf:
        zf.write(overlay_png_path, arcname="overlay_01.png")
    overlay_png_path.unlink()

    # 6. Generate input.json
    output_zip_path = data_dir / "final_output.zip"
    input_data = {
        "background_video_path": str(video_path),
        "overlay_zip_path": str(overlay_zip_path),
        "output_zip_path": str(output_zip_path)
    }
    (data_dir / "input.json").write_text(json.dumps(input_data), encoding="utf-8")

    return {
        "base_dir": data_dir,
        "input_file": "input.json",
        "output_file": "output.json",
        "output_zip_path": output_zip_path
    }
