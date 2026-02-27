"""TMDB and IMDb metadata lookup with error handling.

Wraps tmdbv3api and cinemagoer (IMDbPY) searches with proper
exception handling so a missing or ambiguous title doesn't crash
the entire upload batch.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

from tmdbv3api import TMDb, TV, Movie
from imdb import IMDb as CinemagoerIMDb


@dataclass
class MediaIDs:
    """Container for external media database IDs."""

    tmdb_id: str | None = None
    imdb_id: str | None = None
    title: str = ""


def configure_tmdb(api_key: str) -> None:
    """Set the TMDB API key for all subsequent lookups."""
    tmdb = TMDb()
    tmdb.api_key = api_key


def search_tmdb_tv(title: str) -> str | None:
    """Search TMDB for a TV show and return its ID, or None."""
    try:
        tv = TV()
        results = tv.search(title)
        if results:
            return str(results[0].id)
    except Exception as exc:
        print(f"Warning: TMDB TV search failed for '{title}': {exc}", file=sys.stderr)
    return None


def search_tmdb_movie(title: str) -> str | None:
    """Search TMDB for a movie and return its ID, or None."""
    try:
        movie = Movie()
        results = movie.search(title)
        if results:
            return str(results[0].id)
    except Exception as exc:
        print(f"Warning: TMDB movie search failed for '{title}': {exc}", file=sys.stderr)
    return None


def search_imdb(title: str) -> str | None:
    """Search IMDb for a title and return its ID, or None."""
    try:
        ia = CinemagoerIMDb()
        results = ia.search_movie(title)
        if results:
            return str(results[0].movieID)
    except Exception as exc:
        print(f"Warning: IMDb search failed for '{title}': {exc}", file=sys.stderr)
    return None


def lookup(title: str, category: int, tmdb_api_key: str) -> MediaIDs:
    """Look up TMDB and IMDb IDs for a title.

    Args:
        title: The guessed title to search for.
        category: 1 for movie, 2 for TV show.
        tmdb_api_key: TMDB API key string.

    Returns:
        MediaIDs with whatever IDs were found. Missing IDs are None.
    """
    configure_tmdb(tmdb_api_key)

    ids = MediaIDs(title=title)

    if category == 1:
        ids.tmdb_id = search_tmdb_movie(title)
    elif category == 2:
        ids.tmdb_id = search_tmdb_tv(title)

    ids.imdb_id = search_imdb(title)

    if ids.tmdb_id is None and ids.imdb_id is None:
        print(
            f"Warning: no TMDB or IMDb results for '{title}'. "
            "Upload will proceed without external IDs.",
            file=sys.stderr,
        )

    return ids
