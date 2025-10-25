import os
import sys
from pathlib import Path

import reflex as rx


# Ensure the project root is on the Python path so ``Steppz`` can be
# imported even when Reflex executes from a different working directory (for
# example inside a container where the app is copied to ``/app``).
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from Steppz import secret_manager


proxy_content = os.environ.get("PROXY_CONTENT", "TRUE").upper() == "TRUE"
socks5 = os.environ.get("SOCKS5", "")
playlist_secret = secret_manager.load_secret()

print(f"PROXY_CONTENT: {proxy_content}\nSOCKS5: {socks5}")

config = rx.Config(
    app_name="Steppz",
    proxy_content=proxy_content,
    socks5=socks5,
    show_built_with_reflex=False,
    playlist_secret=playlist_secret,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
