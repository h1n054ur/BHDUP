"""Safe subprocess wrappers replacing os.system calls.

Every external command the script needs (ffmpeg, mktorrent, mediainfo,
imgbox) is wrapped here with proper error handling, argument lists, and
no shell=True invocations.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run(args: list[str], *, quiet: bool = False) -> subprocess.CompletedProcess[str]:
    """Run a command and return the CompletedProcess result.

    Raises SystemExit with a clear message if the command fails.
    When *quiet* is True, stdout and stderr are captured instead of
    printed to the terminal.
    """
    capture = subprocess.PIPE if quiet else None
    try:
        result = subprocess.run(
            args,
            check=True,
            text=True,
            stdout=capture,
            stderr=capture,
        )
    except FileNotFoundError:
        print(f"Error: command not found: {args[0]}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        cmd_str = " ".join(args)
        print(f"Error: command failed (exit {exc.returncode}): {cmd_str}", file=sys.stderr)
        if exc.stderr:
            print(exc.stderr, file=sys.stderr)
        sys.exit(1)
    return result


def hash_torrent(folder: Path, announce_url: str, output: Path, piece_length: int = 24) -> None:
    """Create a .torrent file with mktorrent."""
    run(
        [
            "mktorrent",
            "-p",
            "-l",
            str(piece_length),
            "-a",
            announce_url,
            "-o",
            str(output),
            str(folder),
        ],
        quiet=True,
    )


def dump_mediainfo(video_path: Path, output: Path) -> str:
    """Write mediainfo output to a file and return the text."""
    result = run(["mediainfo", str(video_path)], quiet=True)
    output.write_text(result.stdout)
    return result.stdout


def take_screenshot(video_path: Path, timestamp: str, output_path: Path) -> None:
    """Extract a single frame from a video at the given timestamp."""
    run(
        [
            "ffmpeg",
            "-nostats",
            "-loglevel",
            "0",
            "-ss",
            timestamp,
            "-i",
            str(video_path),
            "-vframes",
            "1",
            "-q:v",
            "2",
            str(output_path),
        ],
        quiet=True,
    )


def take_screenshots(video_path: Path, timestamps: list[str], output_dir: Path) -> list[Path]:
    """Generate numbered screenshots and return their paths."""
    paths: list[Path] = []
    for i, ts in enumerate(timestamps, start=1):
        out = output_dir / f"{i}.png"
        take_screenshot(video_path, ts, out)
        paths.append(out)
    return paths


def upload_imgbox(image_paths: list[Path], thumb_width: int = 350) -> str:
    """Upload images to imgbox and return the raw output text.

    The caller is responsible for parsing bbcode from the output.
    """
    args = ["imgbox"] + [str(p) for p in image_paths] + ["-w", str(thumb_width)]
    result = run(args, quiet=True)
    return result.stdout


def cleanup_files(*paths: Path) -> None:
    """Remove files, ignoring errors for missing ones."""
    for p in paths:
        try:
            p.unlink()
        except FileNotFoundError:
            pass
