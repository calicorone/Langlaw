#!/usr/bin/env python3
"""Launch Langlaw desktop UI (main window + results window)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.langlaw_gui import main

if __name__ == "__main__":
    main()
