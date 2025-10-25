"""Compatibility shim for the legacy StepDaddyLiveHD playlist page."""
from __future__ import annotations

from .._compat import reexport

__all__ = reexport("Stepzz.pages.playlist", globals())

del reexport
