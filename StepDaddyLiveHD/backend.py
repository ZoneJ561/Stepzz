"""Compatibility shim for the legacy StepDaddyLiveHD backend module."""
from __future__ import annotations

from ._compat import reexport

__all__ = reexport("Stepzz.backend", globals())

del reexport
