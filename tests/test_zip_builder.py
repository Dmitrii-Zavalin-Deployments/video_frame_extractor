# tests/test_zip_builder.py
from pathlib import Path

from PIL import Image

import zip_builder


class MockState:
    def __init__(self, tmp_path):
        self.inputs = {}
        self.config = {}
        self.base_dir = tmp_path
        self.output_zip_path = None
        self.processed_frame_paths = []
        self.results = {}


def test_zip_builder_success_with_state_output_zip(tmp_path):
    """Test successful ZIP creation using state.output_zip_path directly."""
    state = MockState(tmp_path)
    state.output_zip_path = tmp_path / "output.zip"

    frame_path = tmp_path / "processed_00000.png"
    Image.new("RGB", (20, 20), color=(255, 0, 0)).save(frame_path)
    state.processed_frame_paths = [frame_path]

    zip_builder.run(state)

    assert state.results["status"] == "success"
    assert state.output_zip_path.exists()


def test_zip_builder_fallback_inputs(tmp_path):
    """Cover lines 15-16: output_zip_path fallback to state.inputs."""
    state = MockState(tmp_path)
    state.output_zip_path = None
    state.inputs["output_zip_path"] = str(tmp_path / "input_output.zip")

    frame_path = tmp_path / "processed_00000.png"
    Image.new("RGB", (20, 20), color=(0, 255, 0)).save(frame_path)
    state.processed_frame_paths = [frame_path]

    zip_builder.run(state)

    assert state.results["status"] == "success"
    assert Path(state.inputs["output_zip_path"]).exists()


def test_zip_builder_fallback_config(tmp_path):
    """Cover lines 17-18: output_zip_path fallback to state.config."""
    state = MockState(tmp_path)
    state.output_zip_path = None
    state.config["output_zip_path"] = str(tmp_path / "config_output.zip")

    frame_path = tmp_path / "processed_00000.png"
    Image.new("RGB", (20, 20), color=(0, 0, 255)).save(frame_path)
    state.processed_frame_paths = [frame_path]

    zip_builder.run(state)

    assert state.results["status"] == "success"
    assert Path(state.config["output_zip_path"]).exists()


def test_zip_builder_missing_output_zip_path(tmp_path):
    """Cover lines 20-21: ValueError when output_zip_path is missing from all sources."""
    state = MockState(tmp_path)
    state.output_zip_path = None
    state.processed_frame_paths = [tmp_path / "dummy.png"]

    zip_builder.run(state)

    assert state.results["status"] == "error"
    assert "Required property 'output_zip_path' is missing" in state.results["error"]


def test_zip_builder_no_processed_frames(tmp_path):
    """Cover lines 29-30: ValueError when processed_frame_paths is empty."""
    state = MockState(tmp_path)
    state.output_zip_path = tmp_path / "output.zip"
    state.processed_frame_paths = []

    zip_builder.run(state)

    assert state.results["status"] == "error"
    assert "No processed frame paths provided" in state.results["error"]


def test_zip_builder_frame_not_found_on_disk(tmp_path):
    """Cover lines 36-37: FileNotFoundError when a processed frame file doesn't exist."""
    state = MockState(tmp_path)
    state.output_zip_path = tmp_path / "output.zip"
    state.processed_frame_paths = [tmp_path / "nonexistent_frame.png"]

    zip_builder.run(state)

    assert state.results["status"] == "error"
    assert "Processed frame file does not exist on disk" in state.results["error"]


def test_zip_builder_success_results_none(tmp_path):
    """Cover lines 42-43: Initializing state.results when None on success."""
    state = MockState(tmp_path)
    state.output_zip_path = tmp_path / "output.zip"

    frame_path = tmp_path / "processed_00000.png"
    Image.new("RGB", (20, 20)).save(frame_path)
    state.processed_frame_paths = [frame_path]
    state.results = None

    zip_builder.run(state)

    assert state.results["status"] == "success"


def test_zip_builder_exception_results_none(tmp_path):
    """Cover lines 49-50: Initializing state.results when None in exception handler."""
    state = MockState(tmp_path)
    state.output_zip_path = tmp_path / "output.zip"
    state.processed_frame_paths = []
    state.results = None

    zip_builder.run(state)

    assert state.results["status"] == "error"
    assert "No processed frame paths provided" in state.results["error"]
