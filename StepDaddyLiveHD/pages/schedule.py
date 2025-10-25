"""Compatibility shim for the legacy StepDaddyLiveHD schedule page."""
from __future__ import annotations

from .._compat import reexport

__all__ = reexport("Stepzz.pages.schedule", globals())

del reexport
