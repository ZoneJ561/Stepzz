"""Compatibility shims for the legacy StepDaddyLiveHD pages."""

from Stepzz.pages import *  # noqa: F401,F403

__all__ = [name for name in globals() if not name.startswith("_")]
