# tests/test_state.py
from pathlib import Path
import pytest
from unittest.mock import patch

from state import State


def test_state_init_success(tmp_path):
    """Test successful initialization of State."""
    input_data = {"output_zip_path": str(tmp_path / "output.zip")}
    config_data = {}
    state = State(input_data, config_data, tmp_path)
    
    assert state.inputs == input_data
    assert state.config == config_data
    assert state.output_zip_path == tmp_path / "output.zip"
    assert state.results["status"] == "pending"


def test_state_init_invalid_input_data_type(tmp_path):
    """Cover line 14: TypeError when input_data is not a dictionary."""
    with pytest.raises(TypeError, match="Required argument 'input_data' must be a valid dictionary."):
        State("not_a_dict", {}, tmp_path)


def test_state_init_invalid_config_data_type(tmp_path):
    """Cover line 16: TypeError when config_data is not a dictionary."""
    with pytest.raises(TypeError, match="Required argument 'config_data' must be a valid dictionary."):
        State({}, "not_a_dict", tmp_path)


def test_state_init_missing_input_output_folder(tmp_path):
    """Cover line 18: ValueError when input_output_folder is missing or empty."""
    with pytest.raises(ValueError, match="Required argument 'input_output_folder' is missing or empty."):
        State({}, {}, "")


def test_state_init_os_error_on_mkdir(tmp_path):
    """Cover lines 39-41: RuntimeError raised when working directories cannot be created."""
    with patch("pathlib.Path.mkdir", side_effect=OSError("Permission denied")):
        with pytest.raises(RuntimeError, match="Could not create working directories"):
            State({"output_zip_path": "output.zip"}, {}, tmp_path)


def test_state_output_zip_path_in_config(tmp_path):
    """Cover lines 51-52: output_zip_path fallback to config dictionary."""
    input_data = {}
    config_data = {"output_zip_path": str(tmp_path / "config_output.zip")}
    state = State(input_data, config_data, tmp_path)
    assert state.output_zip_path == tmp_path / "config_output.zip"


def test_state_missing_output_zip_path(tmp_path):
    """Cover line 55: ValueError when output_zip_path is missing from both inputs and config."""
    with pytest.raises(ValueError, match="Required property 'output_zip_path' is missing"):
        State({}, {}, tmp_path)


def test_write_output_json_success(tmp_path):
    """Test writing output JSON successfully."""
    input_data = {"output_zip_path": str(tmp_path / "output.zip")}
    state = State(input_data, {}, tmp_path)
    out_file = tmp_path / "output.json"
    
    state.write_output_json(out_file)
    assert out_file.exists()


def test_write_output_json_os_error(tmp_path):
    """Cover lines 76-78: RuntimeError raised when writing output JSON fails due to OSError."""
    input_data = {"output_zip_path": str(tmp_path / "output.zip")}
    state = State(input_data, {}, tmp_path)
    out_file = tmp_path / "output.json"

    with patch("builtins.open", side_effect=OSError("Disk full")):
        with pytest.raises(RuntimeError, match="Could not write output JSON"):
            state.write_output_json(out_file)
