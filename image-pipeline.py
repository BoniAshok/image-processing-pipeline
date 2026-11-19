#!/usr/bin/env python3
"""
Backward-compatibility wrapper script for image-pipeline.py.
Forwards execution to src/image_pipeline/cli.py.
"""
import sys
from pathlib import Path

# Ensure src/ is on sys.path
repo_root = Path(__file__).resolve().parent
src_dir = repo_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from image_pipeline.cli import main

if __name__ == "__main__":
    main()
