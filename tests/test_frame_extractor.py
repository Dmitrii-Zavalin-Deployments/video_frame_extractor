# tests/test_frame_extractor.py
from unittest.mock import MagicMock, patch

import frame_extractor


class MockState:
    def __init__(self, tmp_path):
        self.inputs = {}
        self.config = {}
        self.base_dir = tmp_path
        self.frames_dir = tmp_path / "frames"
        self.frame_paths = []
        self.results = {}


def test_fallback_config_path(tmp_path):
    """Cover lines 17-18: Video path fallback to state.config."""
    video = tmp_path / "sample.mp4"
    video.touch()

    state = MockState(tmp_path)
    state.config["background_video_path"] = str(video)

    with patch("cv2.VideoCapture") as mock_cap, patch("cv2.imwrite", return_value=True):
        cap_inst = MagicMock()
        cap_inst.isOpened.side_effect = [True, True, False]
        cap_inst.read.return_value = (True, "fake_frame")
        mock_cap.return_value = cap_inst

        frame_extractor.run(state)
        assert state.results["status"] == "success"


def test_fallback_attribute_path(tmp_path):
    """Cover lines 19-20: Video path fallback to state attribute."""
    video = tmp_path / "sample.mp4"
    video.touch()

    state = MockState(tmp_path)
    state.background_video_path = video

    with patch("cv2.VideoCapture") as mock_cap, patch("cv2.imwrite", return_value=True):
        cap_inst = MagicMock()
        cap_inst.isOpened.side_effect = [True, True, False]
        cap_inst.read.return_value = (True, "fake_frame")
        mock_cap.return_value = cap_inst

        frame_extractor.run(state)
        assert state.results["status"] == "success"


def test_missing_video_path(tmp_path):
    """Cover line 23 & 75-80: Missing background_video_path raises ValueError."""
    state = MockState(tmp_path)
    frame_extractor.run(state)
    assert state.results["status"] == "error"
    assert "Required property 'background_video_path'" in state.results["error"]


def test_nonexistent_video_path(tmp_path):
    """Cover line 29 & 75-80: Video file does not exist on disk."""
    state = MockState(tmp_path)
    state.inputs["background_video_path"] = str(tmp_path / "nonexistent.mp4")
    
    frame_extractor.run(state)
    assert state.results["status"] == "error"
    assert "Video file does not exist" in state.results["error"]


def test_missing_frames_dir(tmp_path):
    """Cover line 34 & 75-80: Missing frames_dir attribute on state."""
    video = tmp_path / "sample.mp4"
    video.touch()

    state = MockState(tmp_path)
    state.inputs["background_video_path"] = str(video)
    del state.frames_dir

    frame_extractor.run(state)
    assert state.results["status"] == "error"
    assert "Required attribute 'frames_dir'" in state.results["error"]


def test_init_frame_paths_and_results_none_on_success(tmp_path):
    """Cover lines 40 & 71: Handle state.frame_paths is None and state.results is None."""
    video = tmp_path / "sample.mp4"
    video.touch()

    state = MockState(tmp_path)
    state.inputs["background_video_path"] = str(video)
    state.frame_paths = None
    state.results = None

    with patch("cv2.VideoCapture") as mock_cap, patch("cv2.imwrite", return_value=True):
        cap_inst = MagicMock()
        cap_inst.isOpened.side_effect = [True, True, False]
        cap_inst.read.return_value = (True, "fake_frame")
        mock_cap.return_value = cap_inst

        frame_extractor.run(state)
        assert state.results["status"] == "success"
        assert len(state.frame_paths) == 1


def test_video_cannot_be_opened(tmp_path):
    """Cover line 44 & 75-80: OpenCV VideoCapture fails to open video stream."""
    video = tmp_path / "sample.mp4"
    video.touch()

    state = MockState(tmp_path)
    state.inputs["background_video_path"] = str(video)

    with patch("cv2.VideoCapture") as mock_cap:
        cap_inst = MagicMock()
        cap_inst.isOpened.return_value = False
        mock_cap.return_value = cap_inst

        frame_extractor.run(state)
        assert state.results["status"] == "error"
        assert "Cannot open video with OpenCV" in state.results["error"]


def test_imwrite_failure_and_no_frames_extracted(tmp_path):
    """Cover line 58 & 68: cv2.imwrite fails and empty frame_paths raises RuntimeError."""
    video = tmp_path / "sample.mp4"
    video.touch()

    state = MockState(tmp_path)
    state.inputs["background_video_path"] = str(video)

    with patch("cv2.VideoCapture") as mock_cap, patch("cv2.imwrite", return_value=False):
        cap_inst = MagicMock()
        cap_inst.isOpened.side_effect = [True, True, False]
        cap_inst.read.return_value = (True, "fake_frame")
        mock_cap.return_value = cap_inst

        frame_extractor.run(state)
        assert state.results["status"] == "error"
        assert "No frames were successfully extracted" in state.results["error"]


def test_exception_when_results_is_none(tmp_path):
    """Cover lines 77-78: Exception block when state.results is None."""
    state = MockState(tmp_path)
    state.inputs["background_video_path"] = str(tmp_path / "nonexistent.mp4")
    state.results = None

    frame_extractor.run(state)
    assert state.results["status"] == "error"
    assert "Video file does not exist" in state.results["error"]
