#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from moments_to_pages.cli import main

raise SystemExit(main(["retry", *sys.argv[1:]]))
