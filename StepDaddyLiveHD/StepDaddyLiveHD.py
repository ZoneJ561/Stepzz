"""Compatibility module for Reflex app discovery.

Reflex expects a module matching ``<app_name>.<app_name>`` when loading an
application during build steps such as ``reflex export``.  The project keeps the
application definition in :mod:`StepDaddyLiveHD.app`, so this module simply
re-exports the ``app`` instance from there.  Keeping this thin wrapper avoids
``ModuleNotFoundError`` during Docker builds while preserving the existing
package layout.
"""

from .app import app

__all__ = ["app"]
