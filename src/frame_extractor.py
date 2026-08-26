# src/frame_extractor.py
import logging
from pathlib import Path

import cv2

logger = logging.getLogger(__name__)


def run(state):
    logger.info("Starting frame extraction pipeline.")
    try:
        # No-Default Policy: Retrieve background_video_path across inputs, config, and state attributes
        video_path_str = None
        if hasattr(state, "inputs") and state.inputs and "background_video_path" in state.inputs:
            video_path_str = state.inputs["background_video_path"]
        elif hasattr(state, "config") and state.config and "background_video_path" in state.config:
            video_path_str = state.config["background_video_path"]
        elif hasattr(state, "background_video_path") and state.background_video_path:
            video_path_str = str(state.background_video_path)

        if not video_path_str:
            raise ValueError("Required property 'background_video_path' is missing from both input.json and config.json.")

        video_path = Path(video_path_str)
        logger.debug("Resolved background video path: %s", video_path)

        if not video_path.exists():
            raise FileNotFoundError(f"Video file does not exist at path: {video_path}")

        # Ensure frames_dir exists under No-Default / strict requirements
        frames_dir = getattr(state, "frames_dir", None)
        if frames_dir is None:
            raise ValueError("Required attribute 'frames_dir' is missing from state.")

        frames_path = Path(frames_dir)
        frames_path.mkdir(parents=True, exist_ok=True)

        if not hasattr(state, "frame_paths") or state.frame_paths is None:
            state.frame_paths = []

        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open video with OpenCV: {video_path}")

        frame_index = 0
        logger.info("Extracting frames from video source...")
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_filename = f"frame_{frame_index:05d}.png"
            frame_path = frames_path / frame_filename
            
            success = cv2.imwrite(str(frame_path), frame)
            if not success:
                logger.warning("Failed to write extracted frame to disk: %s", frame_path)
            else:
                state.frame_paths.append(frame_path)

            frame_index += 1

        cap.release()
        logger.info("Successfully extracted %d frame(s).", len(state.frame_paths))

        if not state.frame_paths:
            raise RuntimeError("No frames were successfully extracted from the video.")

        if not hasattr(state, "results") or state.results is None:
            state.results = {}
        state.results["status"] = "success"
        state.results["error"] = ""

    except (OSError, ValueError, KeyError, RuntimeError) as e:
        logger.exception("Exception encountered during frame extraction")
        if not hasattr(state, "results") or state.results is None:
            state.results = {}
        state.results["status"] = "error"
        state.results["error"] = str(e)
