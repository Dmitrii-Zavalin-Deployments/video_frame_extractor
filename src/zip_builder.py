# src/zip_builder.py
import zipfile

def run(state):
    try:
        with zipfile.ZipFile(state.output_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for frame_path in state.processed_frame_paths:
                zf.write(frame_path, arcname=frame_path.name)

        state.results["status"] = "success"
        state.results["error"] = ""

    except Exception as e:
        state.results["status"] = "error"
        state.results["error"] = str(e)

