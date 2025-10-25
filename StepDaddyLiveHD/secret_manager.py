"""Utilities for loading and rotating the playlist secret code."""

from __future__ import annotations

import os
import secrets
from pathlib import Path


SECRET_FILE = Path(__file__).resolve().parent.parent / ".playlist_secret"


def _read_secret_file() -> str:
    if SECRET_FILE.exists():
        return SECRET_FILE.read_text(encoding="utf-8").strip()
    return ""


def _write_secret_file(secret: str) -> str:
    SECRET_FILE.write_text(secret, encoding="utf-8")
    return secret


def load_secret() -> str:
    """Return the active playlist secret."""

    env_secret = os.environ.get("PLAYLIST_SECRET_CODE", "").strip()
    if env_secret:
        return env_secret
    return _read_secret_file()


def save_secret(secret: str) -> str:
    """Persist ``secret`` for future reads and return it."""

    secret = secret.strip()
    if not secret:
        SECRET_FILE.unlink(missing_ok=True)
        return ""
    return _write_secret_file(secret)


def generate_secret(length: int = 24) -> str:
    """Create, persist, and return a new random playlist secret."""

    secret = secrets.token_urlsafe(length)
    return save_secret(secret)
