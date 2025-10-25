import reflex as rx
import os

from StepDaddyLiveHD import secret_manager


proxy_content = os.environ.get("PROXY_CONTENT", "TRUE").upper() == "TRUE"
socks5 = os.environ.get("SOCKS5", "")
playlist_secret = secret_manager.load_secret()

print(f"PROXY_CONTENT: {proxy_content}\nSOCKS5: {socks5}")

config = rx.Config(
    app_name="StepDaddyLiveHD",
    proxy_content=proxy_content,
    socks5=socks5,
    show_built_with_reflex=False,
    playlist_secret=playlist_secret,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
