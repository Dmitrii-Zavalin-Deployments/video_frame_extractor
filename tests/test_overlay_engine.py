# tests/test_overlay_engine.py
import zipfile

from PIL import Image

import overlay_engine


class MockState:
    def __init__(self, tmp_path):
        self.inputs = {}
        self.config = {}
        self.base_dir = tmp_path
        self.frames_dir = tmp_path / "frames"
        self.processed_frames_dir = tmp_path / "processed_frames"
        self.frame_paths = []
        self.processed_frame_paths = []
        self.results = {}


def create_sample_zip(zip_path, png_filename="overlay.png"):
    img = Image.new("RGBA", (20, 20), color=(0, 255, 0, 128))
    img_path = zip_path.parent / png_filename
    img.save(img_path)
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(img_path, arcname=png_filename)
    img_path.unlink()


def test_overlay_zip_fallback_config_and_positions_inputs(tmp_path):
    """Cover lines 18-19 (overlay_zip from config) and 64-65 (overlay_positions from inputs)."""
    state = MockState(tmp_path)
    zip_path = tmp_path / "overlay.zip"
    create_sample_zip(zip_path)

    state.config["overlay_zip_path"] = str(zip_path)
    state.inputs["overlay_positions"] = [{
        "overlay_transparency": 1.0,
        "background_transparency": 1.0,
        "x": 0,
        "y": 0
    }]

    frame_path = tmp_path / "frame_00000.png"
    Image.new("RGBA", (50, 50), color=(255, 255, 255, 255)).save(frame_path)
    state.frame_paths = [frame_path]

    overlay_engine.run(state)
    assert state.results["status"] == "success"


def test_overlay_zip_fallback_attribute_and_positions_attribute(tmp_path):
    """Cover lines 20-21 (overlay_zip as attribute) and 66-67 (overlay_positions as attribute)."""
    state = MockState(tmp_path)
    zip_path = tmp_path / "overlay.zip"
    create_sample_zip(zip_path)

    state.overlay_zip_path = zip_path
    state.overlay_positions = [{
        "overlay_transparency": 1.0,
        "background_transparency": 0.5,
        "x": 5,
        "y": 5
    }]

    frame_path = tmp_path / "frame_00000.png"
    Image.new("RGBA", (50, 50), color=(255, 255, 255, 255)).save(frame_path)
    state.frame_paths = [frame_path]

    overlay_engine.run(state)
    assert state.results["status"] == "success"


def test_missing_overlay_zip_path(tmp_path):
    """Cover line 24: ValueError when overlay_zip_path is missing."""
    state = MockState(tmp_path)
    overlay_engine.run(state)
    assert state.results["status"] == "error"
    assert "Required property 'overlay_zip_path'" in state.results["error"]


def test_nonexistent_overlay_zip_path(tmp_path):
    """Cover line 30: FileNotFoundError when overlay ZIP doesn't exist."""
    state = MockState(tmp_path)
    state.inputs["overlay_zip_path"] = str(tmp_path / "nonexistent.zip")
    overlay_engine.run(state)
    assert state.results["status"] == "error"
    assert "Overlay ZIP file does not exist" in state.results["error"]


def test_missing_base_dir(tmp_path):
    """Cover line 35: ValueError when base_dir is missing."""
    state = MockState(tmp_path)
    zip_path = tmp_path / "overlay.zip"
    create_sample_zip(zip_path)
    state.inputs["overlay_zip_path"] = str(zip_path)
    state.base_dir = None

    overlay_engine.run(state)
    assert state.results["status"] == "error"
    assert "Required attribute 'base_dir' is missing" in state.results["error"]


def test_bad_zip_file(tmp_path):
    """Cover lines 45-46: BadZipFile raised as ValueError."""
    state = MockState(tmp_path)
    bad_zip = tmp_path / "bad.zip"
    bad_zip.write_text("not a zip file", encoding="utf-8")
    state.inputs["overlay_zip_path"] = str(bad_zip)

    overlay_engine.run(state)
    assert state.results["status"] == "error"
    assert "Invalid or corrupted overlay zip archive" in state.results["error"]


def test_no_overlay_pngs_found(tmp_path):
    """Cover line 51: ValueError when no PNGs found in zip."""
    state = MockState(tmp_path)
    empty_zip = tmp_path / "empty.zip"
    with zipfile.ZipFile(empty_zip, "w"):
        pass
    state.inputs["overlay_zip_path"] = str(empty_zip)

    overlay_engine.run(state)
    assert state.results["status"] == "error"
    assert "No overlay PNGs found" in state.results["error"]


def test_no_frame_paths(tmp_path):
    """Cover line 58: ValueError when frame_paths is empty."""
    state = MockState(tmp_path)
    zip_path = tmp_path / "overlay.zip"
    create_sample_zip(zip_path)
    state.inputs["overlay_zip_path"] = str(zip_path)
    state.frame_paths = []

    overlay_engine.run(state)
    assert state.results["status"] == "error"
    assert "No frame paths available" in state.results["error"]


def test_missing_overlay_positions(tmp_path):
    """Cover line 70: ValueError when overlay_positions is missing."""
    state = MockState(tmp_path)
    zip_path = tmp_path / "overlay.zip"
    create_sample_zip(zip_path)
    state.inputs["overlay_zip_path"] = str(zip_path)

    frame_path = tmp_path / "frame_00000.png"
    Image.new("RGBA", (50, 50)).save(frame_path)
    state.frame_paths = [frame_path]

    overlay_engine.run(state)
    assert state.results["status"] == "error"
    assert "Required property 'overlay_positions'" in state.results["error"]


def test_missing_processed_frames_dir(tmp_path):
    """Cover line 75: ValueError when processed_frames_dir is missing."""
    state = MockState(tmp_path)
    zip_path = tmp_path / "overlay.zip"
    create_sample_zip(zip_path)
    state.inputs["overlay_zip_path"] = str(zip_path)
    state.config["overlay_positions"] = [{"overlay_transparency": 1.0, "background_transparency": 1.0, "x": 0, "y": 0}]

    frame_path = tmp_path / "frame_00000.png"
    Image.new("RGBA", (50, 50)).save(frame_path)
    state.frame_paths = [frame_path]
    state.processed_frames_dir = None

    overlay_engine.run(state)
    assert state.results["status"] == "error"
    assert "Required attribute 'processed_frames_dir'" in state.results["error"]


def test_processed_frame_paths_none_initialization(tmp_path):
    """Cover line 80: Initializing processed_frame_paths when None."""
    state = MockState(tmp_path)
    zip_path = tmp_path / "overlay.zip"
    create_sample_zip(zip_path)
    state.inputs["overlay_zip_path"] = str(zip_path)
    state.config["overlay_positions"] = [{"overlay_transparency": 0.5, "background_transparency": 0.8, "x": 0, "y": 0}]

    frame_path = tmp_path / "frame_00000.png"
    Image.new("RGBA", (50, 50)).save(frame_path)
    state.frame_paths = [frame_path]
    state.processed_frame_paths = None

    overlay_engine.run(state)
    assert state.results["status"] == "success"
    assert len(state.processed_frame_paths) == 1


def test_frame_file_does_not_exist_warning_and_continue(tmp_path):
    """Cover lines 95-96: Warning and continue when frame file doesn't exist on disk."""
    state = MockState(tmp_path)
    zip_path = tmp_path / "overlay.zip"
    create_sample_zip(zip_path)
    state.inputs["overlay_zip_path"] = str(zip_path)
    state.config["overlay_positions"] = [{"overlay_transparency": 1.0, "background_transparency": 1.0, "x": 0, "y": 0}]

    nonexistent_frame = tmp_path / "nonexistent_frame.png"
    state.frame_paths = [nonexistent_frame]

    overlay_engine.run(state)
    assert state.results["status"] == "error"
    assert "No frames were successfully processed" in state.results["error"]


def test_missing_required_key_in_overlay_positions(tmp_path):
    """Cover line 109: KeyError when required key is missing from overlay_positions."""
    state = MockState(tmp_path)
    zip_path = tmp_path / "overlay.zip"
    create_sample_zip(zip_path)
    state.inputs["overlay_zip_path"] = str(zip_path)
    state.config["overlay_positions"] = [{"overlay_transparency": 1.0, "x": 0, "y": 0}]  # missing background_transparency

    frame_path = tmp_path / "frame_00000.png"
    Image.new("RGBA", (50, 50)).save(frame_path)
    state.frame_paths = [frame_path]

    overlay_engine.run(state)
    assert state.results["status"] == "error"
    assert "Missing required key 'background_transparency'" in state.results["error"]


def test_success_with_results_none(tmp_path):
    """Cover line 146: Initializing state.results when None on success."""
    state = MockState(tmp_path)
    zip_path = tmp_path / "overlay.zip"
    create_sample_zip(zip_path)
    state.inputs["overlay_zip_path"] = str(zip_path)
    state.config["overlay_positions"] = [{"overlay_transparency": 1.0, "background_transparency": 1.0, "x": 0, "y": 0}]

    frame_path = tmp_path / "frame_00000.png"
    Image.new("RGBA", (50, 50)).save(frame_path)
    state.frame_paths = [frame_path]
    state.results = None

    overlay_engine.run(state)
    assert state.results["status"] == "success"


def test_exception_handler_with_results_none(tmp_path):
    """Cover lines 152-153: Initializing state.results when None in exception handler."""
    state = MockState(tmp_path)
    state.inputs["overlay_zip_path"] = str(tmp_path / "nonexistent.zip")
    state.results = None

    overlay_engine.run(state)
    assert state.results["status"] == "error"
    assert "Overlay ZIP file does not exist" in state.results["error"]
