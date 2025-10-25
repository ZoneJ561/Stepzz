"""Compatibility shim for the legacy StepDaddyLiveHD admin page."""
from __future__ import annotations

from .._compat import reexport

__all__ = reexport("Stepzz.pages.admin", globals())

del reexport
