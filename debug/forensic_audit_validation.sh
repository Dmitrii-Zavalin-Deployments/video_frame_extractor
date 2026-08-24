#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "      FORENSIC AUDIT: No overlay PNGs found       "
echo "=================================================="

# 1. Diagnostics: Inspect ZIP file contents directly via Python
echo -e "\n[1/3] Running Diagnostics (ZIP content analysis)..."
if [ -f "data/testing-input-output/overlay_object.zip" ]; then
    python3 -c "
import zipfile
try:
    with zipfile.ZipFile('data/testing-input-output/overlay_object.zip', 'r') as zf:
        print('Files inside overlay_object.zip:')
        for name in zf.namelist():
            print(' -', name)
except Exception as e:
    print('Error reading zip archive:', e)
"
else
    echo "Warning: data/testing-input-output/overlay_object.zip not found."
fi

# 2. Source Audits: Inspecting src/overlay_engine.py with line numbers
echo -e "\n[2/3] Performing Source Audits (src/overlay_engine.py)..."
if [ -f "src/overlay_engine.py" ]; then
    cat -n src/overlay_engine.py
else
    echo "Warning: src/overlay_engine.py not found."
fi

# 3. Automated Repairs: Switch to recursive globbing via sed
echo -e "\n[3/3] Executing Automated Repairs..."
if [ -f "src/overlay_engine.py" ]; then
    if grep -q "\.glob(\"\*\.png\")" src/overlay_engine.py; then
        echo "Patching shallow .glob(\"*.png\") to recursive .rglob(\"*.png\") to handle nested folder structures..."
        sed -i 's/\.glob("\*\.png")/\.rglob("\*\.png")/g' src/overlay_engine.py
        echo "Updated source snippet:"
        grep -n "rglob" src/overlay_engine.py || true
    else
        echo "Glob pattern is already recursive or structure differs."
    fi
else
    echo "Cannot patch; source file missing."
fi

echo "=================================================="
echo "          AUDIT & REPAIR COMPLETE                 "
echo "=================================================="