#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "    DIAGNOSTIC: Overlay & Transparency Audit      "
echo "=================================================="

python3 - << 'EOF'
import cv2
import zipfile
import math
import numpy as np
from pathlib import Path

zip_path = "data/testing-input-output/overlay_object.zip"
extract_dir = Path("/tmp/diagnostic_overlays")
extract_dir.mkdir(parents=True, exist_ok=True)

print("1. Inspecting Overlay Archive & Alpha Channels:")
if Path(zip_path).exists():
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(extract_dir)
        img_files = sorted([f for f in extract_dir.glob("*") if f.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"]])
        print(f"   Found {len(img_files)} overlay images:")
        
        for p in img_files:
            # Read with UNCHANGED to check alpha channel
            img = cv2.imread(str(p), cv2.IMREAD_UNCHANGED)
            if img is None:
                print(f"   ❌ {p.name}: Unable to read image")
                continue
            
            channels = 1 if len(img.shape) == 2 else img.shape[2]
            print(f"   - {p.name}: Shape={img.shape}, Channels={channels}")
            
            if channels == 4:
                alpha = img[:, :, 3]
                has_transparency = np.any(alpha < 255)
                print(f"     ✅ 4-channel BGRA detected. Contains transparency: {has_transparency}")
            else:
                print(f"     ⚠️ WARNING: Image has NO alpha channel ({channels} channels). The checkerboard is baked into the RGB pixels!")
else:
    print(f"❌ {zip_path} not found.")

print("\n2. Simulating Frame Distribution Math (146 frames over 5 images):")
total_frames = 146
num_images = 5
chunk_size = math.ceil(total_frames / num_images)  # 150 / 5 = 30

print(f"   Total frames: {total_frames}")
print(f"   Number of overlay images: {num_images}")
print(f"   Calculated frames per image (chunk size): {chunk_size}")

for img_idx in range(num_images):
    start_f = img_idx * chunk_size
    end_f = min(start_f + chunk_size, total_frames) - 1
    count = max(0, end_f - start_f + 1)
    print(f"   - Plane Image {img_idx + 1}: Frames {start_f:03d} to {end_f:03d} (Total: {count} frames)")
EOF

echo "=================================================="