"""Smoke test for playlist secret gating."""
from __future__ import annotations

import importlib
import os
import pathlib
import sys

# Ensure the repository root is importable when running directly from the scripts directory.
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient

from Stepzz import secret_manager
from Stepzz.backend import fastapi_app, step_daddy
from Stepzz.pages.playlist import validate_access_code
from Stepzz.step_daddy import Channel


def main() -> None:
    temp_secret = "temporary-secret"

    # Ensure the temporary secret is set before importing the app config.
    os.environ["PLAYLIST_SECRET_CODE"] = temp_secret

    # Reload the Reflex config so it picks up the temporary secret.
    import rxconfig

    importlib.reload(rxconfig)
    from rxconfig import config

    # Import after the config reload so the helper uses the updated config.

    is_authorized, error_message = validate_access_code("wrong-secret", config.playlist_secret)
    assert not is_authorized, "Access should be denied with an invalid code."
    assert error_message == "Invalid access code.", "User should see an error on failure."

    is_authorized, error_message = validate_access_code(temp_secret, config.playlist_secret)
    assert is_authorized, "Access should be granted with the correct code."
    assert error_message == "", "Error message should be cleared after success."

    # When no secret is configured the playlist should be open by default.
    is_authorized, error_message = validate_access_code("anything", "")
    assert is_authorized, "Playlist should be open when no secret is configured."
    assert error_message == "", "There should be no error when playlist is open."

    # Ensure rotating the secret without the environment override persists a new value.
    os.environ.pop("PLAYLIST_SECRET_CODE", None)
    generated_secret = secret_manager.generate_secret()
    assert generated_secret == secret_manager.load_secret(), "Generated secret should be persisted."
    assert generated_secret, "Generated secret should not be empty."

    # Clean up the persisted secret so subsequent runs start fresh.
    secret_manager.save_secret("")

    # Verify the playlist endpoint returns valid content and respects secret gating.
    sample_channels = [
        Channel(id="1", name="Channel One", tags=[], logo=""),
        Channel(id="2", name="Channel Two", tags=["sports"], logo="https://example.com/logo.png"),
    ]

    step_daddy.channels = sample_channels

    try:
        with TestClient(fastapi_app) as client:
            open_response = client.get("/playlist.m3u8")
            assert open_response.status_code == 200, "Open playlist should return successfully."

            playlist_body = open_response.text
            assert playlist_body.startswith("#EXTM3U"), "Playlist should start with the EXTINF header."

            for channel in sample_channels:
                assert channel.name in playlist_body, "Channel names should be listed in the playlist."
                assert f"/stream/{channel.id}.m3u8" in playlist_body, "Channel stream URLs should be included."

            rotated_secret = secret_manager.save_secret("rotating-secret")

            locked_response = client.get("/playlist.m3u8")
            assert locked_response.status_code == 404, "Locked playlist without secret should not be accessible."

            unlocked_response = client.get(f"/{rotated_secret}/playlist.m3u8")
            assert unlocked_response.status_code == 200, "Playlist should unlock when the secret is supplied."
            assert unlocked_response.text == playlist_body, "Playlist contents should be consistent after locking."
    finally:
        secret_manager.save_secret("")
        step_daddy.channels = []

    print("Playlist secret gating and generation smoke test passed with temporary secret:", temp_secret)


if __name__ == "__main__":
    main()
