"""Type definitions for BHDUP.

Provides TypedDict and type aliases for data structures used across
the package, especially for guessit output and BHD API payloads.
"""

from __future__ import annotations

from typing import TypedDict


class GuessitResult(TypedDict, total=False):
    """Subset of guessit output fields used by BHDUP."""

    title: str
    screen_size: str
    source: str
    other: str | list[str]


class BHDPayload(TypedDict):
    """POST payload for the Beyond-HD upload API."""

    name: str
    description: str
    category_id: int
    type: str
    source: str
    imdb_id: str
    tmdb_id: str
    pack: int
    live: int
    anon: int


class UploadResult(TypedDict):
    """Minimal expected structure from BHD API response."""

    status_code: int
    status_message: str
    success: bool
