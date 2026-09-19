"""Hub page: lesson 02."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_LESSON = Path(__file__).resolve().parents[1] / "02-tool-use"
sys.path.insert(0, str(_LESSON))

_SPEC = importlib.util.spec_from_file_location("lesson_02_app", _LESSON / "app.py")
_MOD = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(_MOD)
_MOD.render()
