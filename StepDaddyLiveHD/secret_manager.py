"""Compatibility shim exposing the Stepzz secret manager under the legacy module."""
from __future__ import annotations

from ._compat import reexport

__all__ = reexport("Stepzz.secret_manager", globals())

del reexport
