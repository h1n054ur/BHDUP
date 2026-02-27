"""Tests for bhdup.preflight module."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from bhdup.preflight import check_binaries


def test_check_binaries_all_found() -> None:
    """Should not raise when all binaries are found."""
    with patch("shutil.which", return_value="/usr/bin/fake"):
        check_binaries(verbose=False)


def test_check_binaries_missing() -> None:
    """Should exit when a binary is missing."""
    with patch("shutil.which", return_value=None), pytest.raises(SystemExit):
        check_binaries()
