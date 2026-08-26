# tests/test_integration.py
import json
import logging
import sys
import zipfile

from src.main import main


def test_full_pipeline_integration_success(setup_pipeline_environment, monkeypatch, caplog):
    """Executes the full main() pipeline without subprocesses or mocking,

    verifying file outcomes, frame operations, zip creation, and log outputs.
    """
    env = setup_pipeline_environment
    data_dir = env["base_dir"]
    output_json_path = data_dir / env["output_file"]

    # Configure caplog to capture module logs at INFO level
    caplog.set_level(logging.INFO)

    # Simulate command-line arguments passed to main.py
    test_args = [
        "src/main.py",
        "--input_output_folder", str(data_dir),
        "--input_file_name", env["input_file"],
        "--output_file_name", env["output_file"]
    ]
    monkeypatch.setattr(sys, "argv", test_args)

    # Direct in-process execution of main()
    main()

    # 1. Verify Output JSON Integrity
    assert output_json_path.exists(), "Output JSON file was not created."
    with open(output_json_path, "r", encoding="utf-8") as f:
        output_data = json.load(f)

    assert output_data["results"]["status"] == "success"
    assert output_data["results"]["error"] == ""
    assert "date_time" in output_data["results"]

    # 2. Verify Frames and Output ZIP Files
    extracted_frames = list((data_dir / "frames").glob("*.png"))
    processed_frames = list((data_dir / "processed_frames").glob("*.png"))
    assert len(extracted_frames) == 5, f"Expected 5 extracted frames, got {len(extracted_frames)}"
    assert len(processed_frames) == 5, f"Expected 5 processed frames, got {len(processed_frames)}"

    output_zip_path = env["output_zip_path"]
    assert output_zip_path.exists(), "Output ZIP file was not created."
    with zipfile.ZipFile(output_zip_path, "r") as zf:
        zip_contents = zf.namelist()
        assert len(zip_contents) == 5
        assert "frame_00000.png" in zip_contents

    # 3. Audit Module Loggers via pytest caplog
    log_messages = [record.message for record in caplog.records]
    
    assert any("Initializing pipeline execution framework." in msg for msg in log_messages)
    assert any("Starting frame extraction pipeline." in msg for msg in log_messages)
    assert any("Extracting frames from video source..." in msg for msg in log_messages)
    assert any("Starting overlay engine pipeline." in msg for msg in log_messages)
    assert any("Applying overlays to" in msg for msg in log_messages)
    assert any("Starting zip builder pipeline." in msg for msg in log_messages)
    assert any("Successfully created and finalized ZIP archive" in msg for msg in log_messages)
    assert any("Pipeline completed successfully." in msg for msg in log_messages)
