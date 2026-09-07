"""Windows release launcher for WEBSTER Mark D."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "WEBSTER_REFERENCE"
if str(REFERENCE) not in sys.path:
    sys.path.insert(0, str(REFERENCE))

from main import main  # noqa: E402


if __name__ == "__main__":
    main()
