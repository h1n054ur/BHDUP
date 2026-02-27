"""Path utilities for BHDUP release processing.

Replaces manual string concatenation with pathlib operations for
constructing file paths, temp directories, and output locations.
"""

from __future__ import annotations

from pathlib import Path


def release_dirs(working_dir: Path) -> list[Path]:
    """List release directories in the working directory.

    Filters out non-directories, hidden entries, and known
    project files so only release folders remain.
    """
    skip = {
        "bhdup.py",
        ".env",
        ".env.example",
        ".git",
        ".gitignore",
        ".ruff_cache",
        "__pycache__",
        "bhdup",
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "bhdup-logo.png",
    }
    dirs = sorted(
        p
        for p in working_dir.iterdir()
        if p.is_dir() and p.name not in skip and not p.name.startswith(".")
    )
    return dirs


def video_file(release_dir: Path) -> Path:
    """Return the first video file found in a release directory.

    Raises FileNotFoundError if the directory is empty.
    """
    VIDEO_EXTENSIONS = {
        ".mkv",
        ".mp4",
        ".avi",
        ".m4v",
        ".ts",
        ".wmv",
        ".mov",
    }
    for f in sorted(release_dir.iterdir()):
        if f.suffix.lower() in VIDEO_EXTENSIONS:
            return f
    # Fall back to first file if no known video extension found
    children = sorted(release_dir.iterdir())
    if not children:
        raise FileNotFoundError(f"No files found in {release_dir}")
    return children[0]


def temp_dir(release_dir: Path) -> Path:
    """Return the path to a temporary .files directory for a release."""
    return release_dir.parent / f"{release_dir.name}.files"


def torrent_path(release_dir: Path) -> Path:
    """Return the .torrent output path for a release."""
    return release_dir.parent / f"{release_dir.name}.torrent"


def mediainfo_path(working_dir: Path) -> Path:
    """Return the mediainfo output path."""
    return working_dir / "mediainfo.txt"


def bbcode_path(release_dir: Path) -> Path:
    """Return the bbcode output path inside the .files directory."""
    return temp_dir(release_dir) / "bbcode.txt"
