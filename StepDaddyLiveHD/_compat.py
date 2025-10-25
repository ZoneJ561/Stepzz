"""Helpers for mirroring Stepzz modules under the legacy StepDaddyLiveHD name."""
from __future__ import annotations

from importlib import import_module
from types import ModuleType
from typing import Dict, Iterable, List


def _iter_exports(module: ModuleType) -> Iterable[str]:
    """Yield the public export names for ``module``."""

    exported = getattr(module, "__all__", None)
    if exported is not None:
        yield from exported
        return

    for name in module.__dict__:
        if not name.startswith("_"):
            yield name


def reexport(module_path: str, namespace: Dict[str, object]) -> List[str]:
    """Populate ``namespace`` with the public exports from ``module_path``.

    Parameters
    ----------
    module_path:
        The dotted path to the Stepzz module that should be mirrored.
    namespace:
        The ``globals()`` dictionary of the legacy shim module.

    Returns
    -------
    list[str]
        The exported symbol names that were injected into ``namespace``.
    """

    module = import_module(module_path)
    exported = list(_iter_exports(module))
    namespace.update({name: getattr(module, name) for name in exported})
    return exported
