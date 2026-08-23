#!/bin/bash

echo "📽️ Starting optimized video creation with FFmpeg..."

# Ensure FFmpeg is installed
sudo apt update
sudo apt install -y ffmpeg

# Define paths
OUTPUT_FOLDER="./frames"  # Updated folder containing rendered frames
VIDEO_FILE="./simulation_final_video.mp4"

# Create video from rendered frames with optimal settings
ffmpeg -framerate 30 -i ${OUTPUT_FOLDER}/frame_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p -preset slow ${VIDEO_FILE}

echo "✅ Video creation completed! Video saved at ${VIDEO_FILE}"
