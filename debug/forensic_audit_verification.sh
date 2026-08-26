#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "=== [DIAGNOSTIC] Grep for Ruff lint target lines ==="
echo "=================================================="
grep -n "sorted(list(" src/overlay_engine.py || true
grep -n "background_alpha" src/overlay_engine.py || true
grep -n "overlay_alpha" src/overlay_engine.py || true
grep -n "isinstance" src/state.py || true

echo ""
echo "=================================================="
echo "=== [AUDIT] Smoking-gun source audit (cat -n) ==="
echo "=================================================="
echo "--- src/overlay_engine.py (around line 45-55) ---"
sed -n '42,55p' src/overlay_engine.py | cat -n
echo "--- src/overlay_engine.py (around line 110-128) ---"
sed -n '110,128p' src/overlay_engine.py | cat -n
echo "--- src/state.py (around line 10-20) ---"
sed -n '10,20p' src/state.py | cat -n

echo ""
echo "=================================================="
echo "=== [REPAIR] Applying programmatic fixes for Ruff violations ==="
echo "=================================================="
python3 - << 'EOF'
import pathlib

# 1. Fix src/overlay_engine.py
path_oe = pathlib.Path("src/overlay_engine.py")
content_oe = path_oe.read_text(encoding="utf-8")

# Fix C414: Unnecessary list() call within sorted()
content_oe = content_oe.replace(
    'overlay_images = sorted(list(overlay_extract_dir.rglob("*.png")))',
    'overlay_images = sorted(overlay_extract_dir.rglob("*.png"))'
)

# Fix B023: Bind loop variable background_alpha in lambda
content_oe = content_oe.replace(
    'a = a.point(lambda p: int(p * background_alpha))',
    'a = a.point(lambda p, bg=background_alpha: int(p * bg))'
)

# Fix B023: Bind loop variable overlay_alpha in lambda
content_oe = content_oe.replace(
    'a = a.point(lambda p: int(p * overlay_alpha))',
    'a = a.point(lambda p, oa=overlay_alpha: int(p * oa))'
)

path_oe.write_text(content_oe, encoding="utf-8")
print("Successfully patched src/overlay_engine.py")

# 2. Fix src/state.py (TRY004: Prefer TypeError for isinstance checks)
path_state = pathlib.Path("src/state.py")
content_state = path_state.read_text(encoding="utf-8")

content_state = content_state.replace(
    'raise ValueError("Required argument \'input_data\' must be a valid dictionary.")',
    'raise TypeError("Required argument \'input_data\' must be a valid dictionary.")'
)
content_state = content_state.replace(
    'raise ValueError("Required argument \'config_data\' must be a valid dictionary.")',
    'raise TypeError("Required argument \'config_data\' must be a valid dictionary.")'
)

path_state.write_text(content_state, encoding="utf-8")
print("Successfully patched src/state.py")
EOF