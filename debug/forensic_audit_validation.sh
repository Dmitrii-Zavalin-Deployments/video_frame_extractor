#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "    DIAGNOSTIC: Inspecting output_frames.zip      "
echo "=================================================="

ZIP_PATH="data/testing-input-output/output_frames.zip"

if [ -f "$ZIP_PATH" ]; then
    echo "Listing contents of: $ZIP_PATH"
    python3 -c "
import zipfile
with zipfile.ZipFile('$ZIP_PATH', 'r') as zf:
    files = zf.namelist()
    print(f'Total files inside archive: {len(files)}')
    for name in files:
        print(f'   - {name}')
        if name.endswith('.zip'):
            print(f'     ⚠️ WARNING: Nested zip detected inside archive!')
"
else
    echo "❌ $ZIP_PATH not found locally. Run your validation pipeline first."
fi

echo "=================================================="