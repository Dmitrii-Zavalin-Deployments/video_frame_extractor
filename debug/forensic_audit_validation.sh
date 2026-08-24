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
if [ -f "src/overlay_engine.py" ]; then
    echo "--- Contents of src/overlay_engine.py ---"
    cat -n src/overlay_engine.py
else
    echo "Warning: src/overlay_engine.py not found."
fi

if [ -f "requirements.txt" ]; then
    echo "--- Contents of requirements.txt ---"
    cat -n requirements.txt
else
    echo "Warning: requirements.txt not found."
fi

# 3. Automated Repairs: Injecting missing dependencies & fixing environment
echo -e "\n[3/3] Executing Automated Repairs..."

# Ensure requirements.txt includes Pillow if it exists
if [ -f "requirements.txt" ]; then
    if ! grep -qi "Pillow" requirements.txt; then
        echo "Injecting 'Pillow' into requirements.txt..."
        sed -i '$a Pillow' requirements.txt
        echo "Updated requirements.txt:"
        cat -n requirements.txt
    else
        echo "Pillow is already referenced in requirements.txt."
    fi
else
    echo "Creating a requirements.txt with Pillow..."
    echo "Pillow" > requirements.txt
fi

# Force-install the missing dependency immediately for the current CI run
echo "Installing missing Pillow dependency..."
pip install --upgrade Pillow

echo "=================================================="
echo "          AUDIT & REPAIR COMPLETE                 "
echo "=================================================="