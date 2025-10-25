import secrets

import reflex as rx

from StepDaddyLiveHD.components import navbar
from rxconfig import config


class PlaylistState(rx.State):
    """State for managing playlist access via a shared secret code."""

    code_input: str = ""
    access_granted: bool = False
    error: str = ""
    unlocked_secret: str = ""

    def hydrate_access(self):
        """Automatically unlock the playlist when no secret is configured."""
        if not getattr(config, "playlist_secret", ""):
            self.access_granted = True
            self.error = ""
            self.unlocked_secret = ""

    def set_code(self, value: str):
        self.code_input = value

    def verify_code(self, form_data: dict):
        """Validate the submitted secret code before revealing the playlist."""
        submitted = (
            (form_data or {}).get("secret_code", self.code_input).strip()
            if isinstance(form_data, dict)
            else self.code_input.strip()
        )
        self.code_input = submitted

        expected = getattr(config, "playlist_secret", "")
        if not expected:
            self.access_granted = True
            self.error = ""
            self.unlocked_secret = ""
            return

        if submitted and secrets.compare_digest(submitted, expected):
            self.access_granted = True
            self.error = ""
            self.unlocked_secret = submitted
            return

        self.access_granted = False
        self.unlocked_secret = ""
        self.error = "Invalid secret code. Please try again."

    @rx.var
    def secret_required(self) -> bool:
        return bool(getattr(config, "playlist_secret", ""))

    @rx.var
    def playlist_url(self) -> str:
        base = config.api_url.rstrip("/")
        if self.unlocked_secret:
            return f"{base}/{self.unlocked_secret}/playlist.m3u8"
        return f"{base}/playlist.m3u8"


def _secret_form() -> rx.Component:
    return rx.vstack(
        rx.heading("Enter secret code", size="5"),
        rx.text(
            "This playlist is restricted. Enter the secret code provided by the administrator to unlock the download link.",
            color="gray.500",
        ),
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="Secret code",
                    type="password",
                    name="secret_code",
                    value=PlaylistState.code_input,
                    on_change=PlaylistState.set_code,
                    size="3",
                    width="100%",
                ),
                rx.button("Unlock playlist", type="submit", size="3", width="100%"),
                rx.cond(
                    PlaylistState.error,
                    rx.text(PlaylistState.error, color="red.500"),
                ),
                spacing="3",
                width="100%",
            ),
            on_submit=PlaylistState.verify_code,
        ),
        spacing="4",
        width="100%",
        align="start",
    )


def _download_panel() -> rx.Component:
    return rx.vstack(
        rx.heading("Playlist unlocked", size="5"),
        rx.text(
            "Copy the link or download the playlist file to load the StepDaddyLiveHD channels in your preferred IPTV player.",
            color="gray.500",
        ),
        rx.hstack(
            rx.button(
                as_child=True,
                children=rx.link(
                    rx.hstack(
                        rx.icon("download"),
                        rx.text("Download playlist"),
                        spacing="2",
                    ),
                    href=PlaylistState.playlist_url,
                    target="_blank",
                ),
                size="3",
            ),
            rx.button(
                rx.hstack(rx.icon("clipboard"), rx.text("Copy link"), spacing="2"),
                on_click=[
                    rx.set_clipboard(PlaylistState.playlist_url),
                    rx.toast("Playlist URL copied to clipboard!"),
                ],
                size="3",
                color_scheme="gray",
            ),
            spacing="4",
        ),
        rx.box(
            rx.code(PlaylistState.playlist_url),
            padding="0.75rem",
            width="100%",
            background=rx.color("gray", 3),
            border_radius="md",
            overflow="auto",
        ),
        rx.cond(
            config.proxy_content,
            rx.fragment(),
            rx.callout(
                "Proxy content is disabled on this instance. Some clients may not work.",
                icon="info",
                color_scheme="orange",
            ),
        ),
        spacing="4",
        width="100%",
        align="start",
    )


@rx.page("/playlist", on_load=PlaylistState.hydrate_access)
def playlist() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.center(
                rx.card(
                    rx.vstack(
                        rx.heading("Secure playlist access", size="7"),
                        rx.text(
                            "Protect the m3u8 feed with a secret code so only trusted viewers can download the playlist.",
                            color="gray.500",
                        ),
                        rx.cond(
                            PlaylistState.secret_required,
                            rx.badge("Secret required", color_scheme="red", variant="surface"),
                            rx.badge("Open access", color_scheme="green", variant="surface"),
                        ),
                        rx.cond(
                            PlaylistState.access_granted,
                            _download_panel(),
                            _secret_form(),
                        ),
                        spacing="5",
                        width="100%",
                        align="start",
                    ),
                    padding="2rem",
                    width="100%",
                    max_width="720px",
                    border_radius="xl",
                    box_shadow="lg",
                ),
                padding_y="3rem",
            ),
            padding_top="7rem",
        ),
    )
