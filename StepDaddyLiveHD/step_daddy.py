"""Compatibility shim for the legacy StepDaddyLiveHD step_daddy module."""
from __future__ import annotations

from ._compat import reexport

__all__ = reexport("Stepzz.step_daddy", globals())

del reexport
