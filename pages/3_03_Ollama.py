"""Hub page: lesson 03."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_LESSON = Path(__file__).resolve().parents[1] / "03-ollama"
sys.path.insert(0, str(_LESSON))
sys.path.insert(0, str(_LESSON.parent))

_SPEC = importlib.util.spec_from_file_location("lesson_03_app", _LESSON / "app.py")
_MOD = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(_MOD)
_MOD.render()
