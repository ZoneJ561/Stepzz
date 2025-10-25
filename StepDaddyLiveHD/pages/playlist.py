import reflex as rx
from rxconfig import config
from StepDaddyLiveHD.components import navbar


def validate_access_code(candidate: str, secret: str) -> tuple[bool, str]:
    """Return whether the candidate grants access and an optional error message."""

    if not secret:
        return True, ""

    if candidate.strip() == secret:
        return True, ""

    return False, "Invalid access code."


class PlaylistState(rx.State):
    access_code: str = ""
    authorized_code: str = ""
    is_authorized: bool = False
    error_message: str = ""

    def set_access_code(self, value: str):
        self.access_code = value

    def verify_code(self):
        secret = getattr(config, "playlist_secret", "")
        is_authorized, error_message = validate_access_code(self.access_code, secret)

        self.is_authorized = is_authorized
        self.error_message = error_message
        if is_authorized:
            self.authorized_code = self.access_code.strip()
        else:
            self.authorized_code = ""

    def revoke_access(self):
        self.is_authorized = False
        self.access_code = ""
        self.error_message = ""
        self.authorized_code = ""

    @rx.var
    def playlist_url(self) -> str:
        code = self.authorized_code.strip()
        if code:
            return f"{config.api_url}/{code}/playlist.m3u8"
        return f"{config.api_url}/playlist.m3u8"


def _access_form() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Enter Access Code", size="6", margin_bottom="0.5rem"),
            rx.text(
                "Access to the playlist is restricted. Please enter the secret code provided by the administrator.",
                text_align="center",
            ),
            rx.input(
                placeholder="Secret code",
                type="password",
                value=PlaylistState.access_code,
                on_change=PlaylistState.set_access_code,
                size="3",
            ),
            rx.button(
                "Unlock Playlist",
                on_click=PlaylistState.verify_code,
                size="3",
                width="100%",
            ),
            rx.cond(
                PlaylistState.error_message != "",
                rx.text(
                    PlaylistState.error_message,
                    color="tomato",
                    font_weight="medium",
                ),
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        padding="2rem",
        width="100%",
        max_width="500px",
        border_radius="xl",
        box_shadow="lg",
    )


def _playlist_content() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.cond(
                config.proxy_content,
                rx.fragment(),
                rx.card(
                    rx.hstack(
                        rx.icon(
                            "info",
                        ),
                        rx.text(
                            "Proxy content is disabled on this instance. Some clients may not work.",
                        ),
                    ),
                    width="100%",
                    background_color=rx.color("accent", 7),
                ),
            ),
            rx.heading("Welcome to StepDaddyLiveHD", size="7", margin_bottom="1rem"),
            rx.text(
                "StepDaddyLiveHD allows you to watch various TV channels via IPTV. "
                "You can download the playlist file below and use it with your favorite media player.",
            ),

            rx.divider(margin_y="1.5rem"),

            rx.heading("How to Use", size="5", margin_bottom="0.5rem"),
            rx.text(
                "1. Copy the link below or download the playlist file",
                margin_bottom="0.5rem",
                font_weight="medium",
            ),
            rx.text(
                "2. Open it with your preferred media player or IPTV app",
                margin_bottom="1.5rem",
                font_weight="medium",
            ),

            rx.hstack(
                rx.button(
                    "Download Playlist",
                    rx.icon("download", margin_right="0.5rem"),
                    on_click=rx.redirect(PlaylistState.playlist_url, is_external=True),
                    size="3",
                ),
                rx.button(
                    "Copy Link",
                    rx.icon("clipboard", margin_right="0.5rem"),
                    on_click=[
                        rx.set_clipboard(PlaylistState.playlist_url),
                        rx.toast("Playlist URL copied to clipboard!"),
                    ],
                    size="3",
                    color_scheme="gray",
                ),
                width="100%",
                justify="center",
                spacing="4",
                margin_bottom="1rem",
            ),

            rx.box(
                rx.text(
                    PlaylistState.playlist_url,
                    font_family="mono",
                    font_size="sm",
                ),
                padding="0.75rem",
                background="gray.100",
                border_radius="md",
                width="100%",
                text_align="center",
            ),

            rx.divider(margin_y="1rem"),

            rx.heading("Compatible Players", size="5", margin_bottom="1rem"),
            rx.text(
                "You can use the m3u8 playlist with most media players and IPTV applications:",
                margin_bottom="1rem",
            ),
            rx.card(
                rx.vstack(
                    rx.heading("VLC Media Player", size="6"),
                    rx.text("Popular free and open-source media player"),
                    rx.spacer(),
                    rx.link(
                        "Download",
                        href="https://www.videolan.org/vlc/",
                        target="_blank",
                        color="blue.500",
                    ),
                    height="100%",
                    justify="between",
                    align="center",
                ),
                padding="1rem",
                width="100%",
            ),

            rx.card(
                rx.vstack(
                    rx.heading("IPTVnator", size="6"),
                    rx.text("Cross-platform IPTV player application"),
                    rx.spacer(),
                    rx.link(
                        "Download",
                        href="https://github.com/4gray/iptvnator",
                        target="_blank",
                        color="blue.500",
                    ),
                    height="100%",
                    justify="between",
                    align="center",
                ),
                padding="1rem",
                width="100%",
            ),

            rx.card(
                rx.vstack(
                    rx.heading("Jellyfin", size="6"),
                    rx.text("Free media system to manage your media"),
                    rx.spacer(),
                    rx.link(
                        "Download",
                        href="https://jellyfin.org/",
                        target="_blank",
                        color="blue.500",
                    ),
                    height="100%",
                    justify="between",
                    align="center",
                ),
                padding="1rem",
                width="100%",
            ),

            rx.divider(margin_y="1rem"),

            rx.text(
                "Need help? Most media players allow you to open network streams or IPTV playlists. "
                "Simply paste the m3u8 URL above or import the downloaded playlist file.",
                font_style="italic",
                color="gray.600",
                text_align="center",
            ),
            spacing="4",
            width="100%",
        ),
        padding="2rem",
        width="100%",
        max_width="800px",
        border_radius="xl",
        box_shadow="lg",
    )


@rx.page("/playlist")
def playlist() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.center(
                rx.cond(
                    PlaylistState.is_authorized,
                    _playlist_content(),
                    _access_form(),
                ),
            ),
            padding_top="7rem",
        ),
    )
