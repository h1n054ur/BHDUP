"""Preflight checks for required system binaries."""

from __future__ import annotations

import shutil
import sys


REQUIRED_BINARIES = {
    "ffmpeg": "screenshot generation",
    "mktorrent": "torrent file creation",
    "mediainfo": "media metadata extraction",
    "imgbox": "screenshot hosting (install via: pipx install imgbox-cli)",
}


def check_binaries() -> None:
    """Verify all required external tools are installed.

    Prints a clear message for each missing binary and exits
    if any are not found.
    """
    missing: list[str] = []

    for binary, purpose in REQUIRED_BINARIES.items():
        if shutil.which(binary) is None:
            missing.append(f"  - {binary}: {purpose}")

    if missing:
        print("Error: missing required system binaries:", file=sys.stderr)
        for line in missing:
            print(line, file=sys.stderr)
        print(
            "\nInstall the missing tools and ensure they are on your PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
