"""Parse imgbox CLI output into BBCode thumbnail links.

Replaces the fragile grep | awk | sed shell pipeline in bhdup.py
with a Python regex parser that extracts webpage and thumbnail URLs
from imgbox-cli output.
"""

from __future__ import annotations

import re


# imgbox-cli outputs lines like:
#   Webpage: https://imgbox.com/abc123
#   Thumbnail: https://thumbs2.imgbox.com/xx/yy/abc123_t.png
_WEBPAGE_RE = re.compile(r"Webpage:\s+(https?://\S+)")
_THUMBNAIL_RE = re.compile(r"Thumbnail:\s+(https?://\S+)")


def parse_bbcode(imgbox_output: str) -> str:
    """Parse imgbox CLI output and return BBCode for forum embedding.

    Each image produces a clickable thumbnail:
        [URL=<webpage>][img]<thumbnail>[/img][/URL]

    All thumbnails are concatenated into a single string matching
    the original shell pipeline output.
    """
    webpages = _WEBPAGE_RE.findall(imgbox_output)
    thumbnails = _THUMBNAIL_RE.findall(imgbox_output)

    if len(webpages) != len(thumbnails):
        raise ValueError(
            f"Mismatched imgbox output: {len(webpages)} webpages vs {len(thumbnails)} thumbnails"
        )

    if not webpages:
        raise ValueError("No imgbox URLs found in output")

    parts: list[str] = []
    for webpage, thumb in zip(webpages, thumbnails):
        parts.append(f"[URL={webpage}][img]{thumb}[/img][/URL]")

    return "".join(parts)
