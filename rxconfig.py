import os

import reflex as rx


proxy_content = os.environ.get("PROXY_CONTENT", "TRUE").upper() == "TRUE"
socks5 = os.environ.get("SOCKS5", "")
playlist_secret = os.environ.get("PLAYLIST_SECRET_CODE", "").strip()

print(
    "PROXY_CONTENT: {}\nSOCKS5: {}\nPLAYLIST_SECRET_SET: {}".format(
        proxy_content, socks5, bool(playlist_secret)
    )
)

config = rx.Config(
    app_name="StepDaddyLiveHD",
    proxy_content=proxy_content,
    socks5=socks5,
    show_built_with_reflex=False,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)

config.playlist_secret = playlist_secret
