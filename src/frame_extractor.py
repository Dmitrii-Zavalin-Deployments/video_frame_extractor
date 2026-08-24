# src/frame_extractor.py
import cv2
from pathlib import Path

def run(state):
    video_path = state.inputs["background_video_path"]
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        state.results["status"] = "error"
        state.results["error"] = f"Cannot open video: {video_path}"
        return

    frame_index = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_path = state.frames_dir / f"frame_{frame_index:05d}.png"
        cv2.imwrite(str(frame_path), frame)
        state.frame_paths.append(frame_path)

        frame_index += 1

    cap.release()

