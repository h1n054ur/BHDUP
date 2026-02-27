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


def check_binaries(verbose: bool = False) -> None:
    """Verify all required external tools are installed.

    Prints a clear message for each missing binary and exits
    if any are not found. When verbose is True, also prints
    the resolved path for each found binary.
    """
    missing: list[str] = []
    found: list[str] = []

    for binary, purpose in REQUIRED_BINARIES.items():
        path = shutil.which(binary)
        if path is None:
            missing.append(f"  - {binary}: {purpose}")
        else:
            found.append(f"  - {binary}: {path}")

    if found and verbose:
        print("Found required binaries:")
        for line in found:
            print(line)

    if missing:
        print("Error: missing required system binaries:", file=sys.stderr)
        for line in missing:
            print(line, file=sys.stderr)
        print(
            "\nInstall the missing tools and ensure they are on your PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
