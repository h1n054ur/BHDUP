"""Configuration loading and validation for BHDUP."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from dotenv import load_dotenv
import os


REQUIRED_KEYS = ["TORRENTPASSKEY", "BHDAPI", "TMDBAPI"]
SCREENSHOT_KEYS = [f"SCREEN_SHOT{i}" for i in range(1, 7)]
TIME_PATTERN = re.compile(r"^\d{2}:\d{2}:\d{2}$")
DEFAULT_SCREENSHOT_TIMES = [
    "00:02:45",
    "00:05:45",
    "00:08:45",
    "00:11:45",
    "00:14:45",
    "00:17:45",
]


def load_config(env_path: Path | None = None) -> dict[str, str]:
    """Load and validate .env configuration.

    Returns a dict of all config values. Exits with a clear
    error message if required keys are missing or malformed.
    """
    if env_path is None:
        env_path = Path.cwd() / ".env"

    if not env_path.exists():
        print(f"Error: .env file not found at {env_path}", file=sys.stderr)
        sys.exit(1)

    load_dotenv(env_path)

    config: dict[str, str] = {}
    missing: list[str] = []

    for key in REQUIRED_KEYS:
        value = os.getenv(key, "").strip()
        if not value:
            missing.append(key)
        else:
            config[key] = value

    if missing:
        print(f"Error: missing required .env keys: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    bad_times: list[str] = []
    for i, key in enumerate(SCREENSHOT_KEYS):
        value = os.getenv(key, "").strip()
        if value:
            if not TIME_PATTERN.match(value):
                bad_times.append(f"{key}={value}")
            config[key] = value
        else:
            config[key] = DEFAULT_SCREENSHOT_TIMES[i]

    if bad_times:
        print(
            f"Error: invalid screenshot time format (expected HH:MM:SS): {', '.join(bad_times)}",
            file=sys.stderr,
        )
        sys.exit(1)

    return config
