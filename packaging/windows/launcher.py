"""Windows GUI release launcher for WEBSTER Mark D."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from WEBSTER_REFERENCE.ui.desktop_app import launch  # noqa: E402


if __name__ == "__main__":
    launch()
