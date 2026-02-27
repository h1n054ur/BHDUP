"""Structured logging for BHDUP pipeline steps.

Replaces scattered colorama print() calls with a consistent logger
that tags each message with a step label and optional release name.
"""

from __future__ import annotations

import sys
from enum import Enum

try:
    from colorama import Fore, Style, init as colorama_init

    colorama_init(autoreset=True)
    _HAS_COLOR = True
except ImportError:
    _HAS_COLOR = False


class Step(Enum):
    """Pipeline step identifiers for log messages."""

    START = "start"
    CONFIG = "config"
    PREFLIGHT = "preflight"
    HASH = "hash"
    MEDIAINFO = "mediainfo"
    SCREENSHOT = "screenshot"
    UPLOAD = "upload"
    METADATA = "metadata"
    POST = "post"
    CLEANUP = "cleanup"
    DONE = "done"
    ERROR = "error"


_STEP_COLORS: dict[Step, str] = {}
if _HAS_COLOR:
    _STEP_COLORS = {
        Step.START: Fore.RED,
        Step.CONFIG: Fore.WHITE,
        Step.PREFLIGHT: Fore.WHITE,
        Step.HASH: Fore.GREEN,
        Step.MEDIAINFO: Fore.YELLOW,
        Step.SCREENSHOT: Fore.MAGENTA,
        Step.UPLOAD: Fore.CYAN,
        Step.METADATA: Fore.BLUE,
        Step.POST: Fore.YELLOW,
        Step.CLEANUP: Fore.WHITE,
        Step.DONE: Fore.GREEN,
        Step.ERROR: Fore.RED,
    }


def log(step: Step, message: str, release: str | None = None) -> None:
    """Print a structured log line.

    Format: [STEP] message
    Or:     [STEP] (release) message
    """
    tag = f"[{step.value.upper()}]"
    context = f"({release}) " if release else ""
    color = _STEP_COLORS.get(step, "")
    reset = Style.RESET_ALL if _HAS_COLOR else ""

    line = f"{color}{tag} {context}{message}{reset}"
    dest = sys.stderr if step == Step.ERROR else sys.stdout
    print(line, file=dest)


def info(message: str, release: str | None = None) -> None:
    """Shorthand for a config/info-level message."""
    log(Step.CONFIG, message, release)


def error(message: str, release: str | None = None) -> None:
    """Shorthand for an error message."""
    log(Step.ERROR, message, release)


def step_done(step: Step, release: str | None = None) -> None:
    """Log completion of a pipeline step."""
    log(step, "done", release)
