import os
import secrets

import reflex as rx

from Stepzz import secret_manager
from Stepzz.components import navbar
from rxconfig import config


class AdminState(rx.State):
    password: str = ""
    is_authenticated: bool = False
    error_message: str = ""
    success_message: str = ""
    playlist_secret: str = secret_manager.load_secret()

    def set_password(self, value: str):
        self.password = value

    def _clear_messages(self):
        self.error_message = ""
        self.success_message = ""

    def login(self):
        self._clear_messages()
        expected_password = os.environ.get("ADMIN_PASSWORD", "")
        if not expected_password:
            self.error_message = "ADMIN_PASSWORD environment variable is not configured."
            return

        if secrets.compare_digest(self.password.strip(), expected_password):
            self.is_authenticated = True
            self.password = ""
            self.playlist_secret = secret_manager.load_secret()
            config.playlist_secret = self.playlist_secret
            self.success_message = "Admin access granted."
        else:
            self.error_message = "Invalid admin password."
            self.is_authenticated = False

    def logout(self):
        self._clear_messages()
        self.is_authenticated = False
        self.password = ""

    def generate_secret(self):
        self._clear_messages()
        if not self.is_authenticated:
            self.error_message = "Please log in to rotate the playlist secret."
            return

        new_secret = secret_manager.generate_secret()
        self.playlist_secret = new_secret
        config.playlist_secret = new_secret
        self.success_message = "Generated a new playlist secret."

    @rx.var
    def playlist_url(self) -> str:
        secret = self.playlist_secret.strip()
        if secret:
            return f"{config.api_url}/{secret}/playlist.m3u8"
        return f"{config.api_url}/playlist.m3u8"


def _login_form() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Admin Login", size="6"),
            rx.text(
                "Enter the administrator password to manage the playlist secret.",
                text_align="center",
            ),
            rx.input(
                placeholder="Admin password",
                type="password",
                value=AdminState.password,
                on_change=AdminState.set_password,
                size="3",
            ),
            rx.button(
                "Log In",
                on_click=AdminState.login,
                width="100%",
                size="3",
            ),
            rx.cond(
                AdminState.error_message != "",
                rx.text(AdminState.error_message, color="tomato", font_weight="medium"),
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        padding="2rem",
        width="100%",
        max_width="450px",
        border_radius="xl",
        box_shadow="lg",
    )


def _admin_panel() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Playlist Administration", size="6"),
            rx.text(
                "Share the URL below with trusted viewers. Generate a new secret whenever you need to revoke access.",
                text_align="center",
            ),
            rx.box(
                rx.text(
                    AdminState.playlist_url,
                    font_family="mono",
                    font_size="sm",
                    word_break="break-all",
                ),
                padding="0.75rem",
                background="gray.100",
                border_radius="md",
                width="100%",
                text_align="center",
            ),
            rx.hstack(
                rx.button(
                    "Copy URL",
                    rx.icon("clipboard", margin_right="0.5rem"),
                    on_click=[
                        rx.set_clipboard(AdminState.playlist_url),
                        rx.toast("Admin playlist URL copied!"),
                    ],
                    size="3",
                ),
                rx.button(
                    "Generate New Secret",
                    rx.icon("refresh-ccw", margin_right="0.5rem"),
                    on_click=AdminState.generate_secret,
                    size="3",
                    color_scheme="red",
                ),
                rx.button(
                    "Log Out",
                    rx.icon("log-out", margin_right="0.5rem"),
                    on_click=AdminState.logout,
                    size="3",
                    color_scheme="gray",
                ),
                spacing="3",
                justify="center",
                wrap="wrap",
            ),
            rx.cond(
                AdminState.success_message != "",
                rx.text(AdminState.success_message, color="green", font_weight="medium"),
            ),
            rx.cond(
                AdminState.error_message != "",
                rx.text(AdminState.error_message, color="tomato", font_weight="medium"),
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


@rx.page("/admin")
def admin() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.center(
                rx.cond(
                    AdminState.is_authenticated,
                    _admin_panel(),
                    _login_form(),
                ),
            ),
            padding_top="7rem",
        ),
    )
