import importlib
import importlib.util
import os
import sys
from pathlib import Path

import reflex as rx


# Ensure the project root is on the Python path so ``Stepzz`` (or the legacy
# ``StepDaddyLiveHD`` compatibility shims) can be imported even when Reflex
# executes from a different working directory (for example inside a container
# where the app is copied to ``/app`` before the rest of the repository).
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def _resolve_secret_loader():
    """Return the ``load_secret`` function from the available app package.

    When Docker builds the image it copies ``rxconfig.py`` before the rest of
    the application code. During the ``reflex init`` step the Stepzz package is
    therefore not importable yet which previously caused the build to fail.
    ``importlib.util.find_spec`` lets us detect whether a module is available
    without raising ``ModuleNotFoundError`` so the config can fall back to a
    no-op loader until the real package has been copied into place.
    """

    for module_path in (
        "Stepzz.secret_manager",
        "StepDaddyLiveHD.secret_manager",
    ):
        spec = importlib.util.find_spec(module_path)
        if spec is not None:
            module = importlib.import_module(module_path)
            return getattr(module, "load_secret")

    def _no_secret():
        return os.environ.get("PLAYLIST_SECRET_CODE", "")

    return _no_secret


load_secret = _resolve_secret_loader()


proxy_content = os.environ.get("PROXY_CONTENT", "TRUE").upper() == "TRUE"
socks5 = os.environ.get("SOCKS5", "")
playlist_secret = load_secret()

print(f"PROXY_CONTENT: {proxy_content}\nSOCKS5: {socks5}")

config = rx.Config(
    app_name="Stepzz",
    proxy_content=proxy_content,
    socks5=socks5,
    show_built_with_reflex=False,
    playlist_secret=playlist_secret,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
