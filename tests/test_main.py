# tests/test_main.py
import json
import sys
import pytest
from unittest.mock import patch, MagicMock

import main
from main import load_json, load_schema, main as main_entry


def test_load_json_file_not_found(tmp_path):
    """Cover line 20: FileNotFoundError raised when target JSON file does not exist."""
    non_existent_file = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError, match="Required JSON file not found at path"):
        load_json(non_existent_file)


def test_load_schema_file_not_found(tmp_path):
    """Cover line 28: FileNotFoundError raised when target schema file does not exist."""
    non_existent_schema = tmp_path / "missing_schema.json"
    with pytest.raises(FileNotFoundError, match="Required schema file not found at path"):
        load_schema(non_existent_schema)


def test_main_file_not_found_handling(tmp_path, monkeypatch):
    """Cover lines 63-76: Handle FileNotFoundError during schema or payload loading."""
    monkeypatch.chdir(tmp_path)
    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    test_args = [
        "main.py",
        "--input_output_folder", str(data_dir),
        "--input_file_name", "missing_input.json",
        "--output_file_name", "output.json"
    ]
    monkeypatch.setattr(sys, "argv", test_args)

    main_entry()

    output_path = data_dir / "output.json"
    assert output_path.exists()
    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["results"]["status"] == "error"
    assert "Required JSON file not found" in data["results"]["error"]


def test_main_schema_validation_error_handling(tmp_path, monkeypatch):
    """Cover lines 63-76: Handle ValidationError when payload fails schema validation."""
    monkeypatch.chdir(tmp_path)
    schema_dir = tmp_path / "schema"
    config_dir = tmp_path / "config"
    data_dir = tmp_path / "data"

    schema_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    # Valid schema requiring 'required_field'
    input_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"required_field": {"type": "string"}},
        "required": ["required_field"]
    }
    config_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object"
    }
    (schema_dir / "input_schema.json").write_text(json.dumps(input_schema), encoding="utf-8")
    (schema_dir / "config_schema.json").write_text(json.dumps(config_schema), encoding="utf-8")

    # Invalid input missing 'required_field'
    (data_dir / "input.json").write_text(json.dumps({}), encoding="utf-8")
    (config_dir / "config.json").write_text(json.dumps({}), encoding="utf-8")

    test_args = [
        "main.py",
        "--input_output_folder", str(data_dir),
        "--input_file_name", "input.json",
        "--output_file_name", "output.json"
    ]
    monkeypatch.setattr(sys, "argv", test_args)

    main_entry()

    output_path = data_dir / "output.json"
    assert output_path.exists()
    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["results"]["status"] == "error"
    assert "'required_field' is a required property" in data["results"]["error"]


def test_main_json_decode_error_handling(tmp_path, monkeypatch):
    """Cover lines 63-76: Handle JSONDecodeError when payload JSON is corrupted."""
    monkeypatch.chdir(tmp_path)
    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    (data_dir / "corrupt_input.json").write_text("{invalid json", encoding="utf-8")

    test_args = [
        "main.py",
        "--input_output_folder", str(data_dir),
        "--input_file_name", "corrupt_input.json",
        "--output_file_name", "output.json"
    ]
    monkeypatch.setattr(sys, "argv", test_args)

    main_entry()

    output_path = data_dir / "output.json"
    assert output_path.exists()
    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["results"]["status"] == "error"
    assert "Expecting property name enclosed in double quotes" in data["results"]["error"]


def test_main_pipeline_stage_error_handling(setup_pipeline_environment, monkeypatch):
    """Cover lines 93-95: Pipeline stage failure halts remaining execution and writes error state."""
    env = setup_pipeline_environment
    data_dir = env["base_dir"]

    test_args = [
        "main.py",
        "--input_output_folder", str(data_dir),
        "--input_file_name", env["input_file"],
        "--output_file_name", env["output_file"]
    ]
    monkeypatch.setattr(sys, "argv", test_args)

    # Mock stage execution where frame_extractor fails
    def failing_frame_extractor(state):
        state.results["status"] = "error"
        state.results["error"] = "Frame extraction simulated failure"

    mock_overlay = MagicMock()

    with patch("frame_extractor.run", side_effect=failing_frame_extractor), \
         patch("overlay_engine.run", mock_overlay):
        
        main_entry()

        output_path = data_dir / env["output_file"]
        assert output_path.exists()
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["results"]["status"] == "error"
        assert "Frame extraction simulated failure" in data["results"]["error"]
        mock_overlay.assert_not_called()
