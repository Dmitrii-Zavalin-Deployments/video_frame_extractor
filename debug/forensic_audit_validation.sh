#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "          FORENSIC AUDIT & REPAIR SCRIPT          "
echo "=================================================="

# 1. Diagnostics: Environment & Installed Packages
echo -e "\n[1/3] Running Environment Diagnostics..."
python3 --version
pip --version
echo "--- Installed Python Packages ---"
pip list

# 2. Source Audits: Smoking-gun file inspections
echo -e "\n[2/3] Performing Source Audits..."
if [ -f "src/frame_extractor.py" ]; then
    echo "--- Contents of src/frame_extractor.py ---"
    cat -n src/frame_extractor.py
else
    echo "Warning: src/frame_extractor.py not found."
fi

if [ -f "requirements.txt" ]; then
    echo "--- Contents of requirements.txt ---"
    cat -n requirements.txt
else
    echo "Warning: requirements.txt not found."
fi

# 3. Automated Repairs: Injecting missing dependencies & fixing environment
echo -e "\n[3/3] Executing Automated Repairs..."

# Ensure requirements.txt includes opencv-python-headless if it exists
if [ -f "requirements.txt" ]; then
    if ! grep -qi "opencv-" requirements.txt; then
        echo "Injecting 'opencv-python-headless' into requirements.txt..."
        sed -i '$a opencv-python-headless' requirements.txt
        echo "Updated requirements.txt:"
        cat -n requirements.txt
    else
        echo "OpenCV is already referenced in requirements.txt."
    fi
else
    echo "Creating a requirements.txt with OpenCV..."
    echo "opencv-python-headless" > requirements.txt
fi

# Force-install the missing dependency immediately for the current CI run
echo "Installing missing OpenCV dependency..."
pip install --upgrade opencv-python-headless

echo "=================================================="
echo "          AUDIT & REPAIR COMPLETE                 "
echo "=================================================="