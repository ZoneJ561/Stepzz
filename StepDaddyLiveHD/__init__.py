"""Compatibility package that mirrors the Stepzz application namespace."""
from __future__ import annotations

from ._compat import reexport

__all__ = reexport("Stepzz", globals())

del reexport
