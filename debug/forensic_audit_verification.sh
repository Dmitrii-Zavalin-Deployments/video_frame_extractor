#!/usr/bin/env bash
# debug/forensic_audit.sh
set -euo pipefail

echo ""
echo "=================================================="
echo " STEP 2: Smoking-gun source audit with cat -n"
echo "=================================================="
echo "--- tests/test_overlay_engine.py (Unused variable 'zf') ---"
sed -n '115,125p' tests/test_overlay_engine.py | cat -n

echo "--- tests/test_state.py (Nested 'with' statements SIM117) ---"
sed -n '38,45p;73,80p' tests/test_state.py | cat -n

echo ""
echo "=================================================="
echo " STEP 3: Applying automated repairs"
echo "=================================================="
python3 - << 'EOF'
from pathlib import Path

# 1. Fix unused variable 'zf' in test_overlay_engine.py
p1 = Path("tests/test_overlay_engine.py")
if p1.exists():
    content1 = p1.read_text(encoding="utf-8")
    new_content1 = content1.replace(
        'with zipfile.ZipFile(empty_zip, "w") as zf:',
        'with zipfile.ZipFile(empty_zip, "w"):'
    )
    if content1 != new_content1:
        p1.write_text(new_content1, encoding="utf-8")
        print("[FIXED] Removed unused 'zf' variable in test_overlay_engine.py")
    else:
        print("[WARNING] Target string for 'zf' replacement not found.")

# 2. Fix nested 'with' statements (SIM117) in test_state.py
p2 = Path("tests/test_state.py")
if p2.exists():
    content2 = p2.read_text(encoding="utf-8")
    
    # Replace first occurrence
    target1 = (
        '    with patch("pathlib.Path.mkdir", side_effect=OSError("Permission denied")):\n'
        '        with pytest.raises(RuntimeError, match="Could not create working directories"):'
    )
    replacement1 = (
        '    with patch("pathlib.Path.mkdir", side_effect=OSError("Permission denied")),\n'
        '         pytest.raises(RuntimeError, match="Could not create working directories"):'
    )
    
    # Replace second occurrence
    target2 = (
        '    with patch("builtins.open", side_effect=OSError("Disk full")):\n'
        '        with pytest.raises(RuntimeError, match="Could not write output JSON"):'
    )
    replacement2 = (
        '    with patch("builtins.open", side_effect=OSError("Disk full")),\n'
        '         pytest.raises(RuntimeError, match="Could not write output JSON"):'
    )

    new_content2 = content2.replace(target1, replacement1).replace(target2, replacement2)
    if content2 != new_content2:
        p2.write_text(new_content2, encoding="utf-8")
        print("[FIXED] Combined nested 'with' statements in test_state.py")
    else:
        print("[WARNING] Target strings for SIM117 replacements not found.")
EOF