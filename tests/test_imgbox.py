"""Tests for bhdup.imgbox module."""

from __future__ import annotations

import pytest

from bhdup.imgbox import parse_bbcode


SAMPLE_OUTPUT = """\
[17:43:12] Uploading 1.png ...
   Webpage: https://imgbox.com/abc111
   Thumbnail: https://thumbs2.imgbox.com/xx/yy/abc111_t.png
[17:43:13] Uploading 2.png ...
   Webpage: https://imgbox.com/abc222
   Thumbnail: https://thumbs2.imgbox.com/xx/yy/abc222_t.png
"""


def test_parse_valid_output() -> None:
    result = parse_bbcode(SAMPLE_OUTPUT)
    assert "[URL=https://imgbox.com/abc111]" in result
    assert "[img]https://thumbs2.imgbox.com/xx/yy/abc111_t.png[/img]" in result
    assert "[URL=https://imgbox.com/abc222]" in result
    assert result.count("[URL=") == 2


def test_empty_output_raises() -> None:
    with pytest.raises(ValueError, match="No imgbox URLs"):
        parse_bbcode("")


def test_mismatched_counts_raises() -> None:
    bad = "Webpage: https://imgbox.com/a\n"
    with pytest.raises(ValueError, match="Mismatched"):
        parse_bbcode(bad)
