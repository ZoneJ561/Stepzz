"""Stepzz Reflex application package (alias of StepDaddyLiveHD)."""

from __future__ import annotations

import importlib
import sys
from types import ModuleType

__all__ = ["app", "secret_manager"]


def _load_secret_manager() -> ModuleType:
    module = importlib.import_module("StepDaddyLiveHD.secret_manager")
    sys.modules[__name__ + ".secret_manager"] = module
    return module


def __getattr__(name: str):
    if name == "app":
        from StepDaddyLiveHD.app import app as _app

        globals()["app"] = _app
        return _app
    if name == "secret_manager":
        module = _load_secret_manager()
        globals()["secret_manager"] = module
        return module
    raise AttributeError(name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
