"""Compatibility shim for the legacy StepDaddyLiveHD card component."""
from __future__ import annotations

from .._compat import reexport

__all__ = reexport("Stepzz.components.card", globals())

del reexport
