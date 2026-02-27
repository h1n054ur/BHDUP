"""Tests for bhdup.config module."""

from __future__ import annotations

from pathlib import Path

import pytest

from bhdup.config import load_config, TIME_PATTERN, DEFAULT_SCREENSHOT_TIMES


@pytest.fixture()
def valid_env(tmp_path: Path) -> Path:
    """Create a valid .env file."""
    env = tmp_path / ".env"
    env.write_text(
        "TORRENTPASSKEY=abc123\n"
        "BHDAPI=def456\n"
        "TMDBAPI=ghi789\n"
        "SCREEN_SHOT1=00:05:00\n"
        "SCREEN_SHOT2=00:10:00\n"
    )
    return env


@pytest.fixture()
def missing_keys_env(tmp_path: Path) -> Path:
    """Create an .env file with missing required keys."""
    env = tmp_path / ".env"
    env.write_text("TORRENTPASSKEY=abc123\n")
    return env


@pytest.fixture()
def bad_time_env(tmp_path: Path) -> Path:
    """Create an .env file with malformed screenshot time."""
    env = tmp_path / ".env"
    env.write_text("TORRENTPASSKEY=abc123\nBHDAPI=def456\nTMDBAPI=ghi789\nSCREEN_SHOT1=badtime\n")
    return env


def test_load_valid_config(valid_env: Path) -> None:
    config = load_config(valid_env)
    assert config["TORRENTPASSKEY"] == "abc123"
    assert config["BHDAPI"] == "def456"
    assert config["TMDBAPI"] == "ghi789"
    assert config["SCREEN_SHOT1"] == "00:05:00"
    assert config["SCREEN_SHOT2"] == "00:10:00"
    # Remaining screenshot times should use defaults
    assert config["SCREEN_SHOT3"] == DEFAULT_SCREENSHOT_TIMES[2]


def test_missing_required_keys(missing_keys_env: Path) -> None:
    with pytest.raises(SystemExit):
        load_config(missing_keys_env)


def test_bad_screenshot_time(bad_time_env: Path) -> None:
    with pytest.raises(SystemExit):
        load_config(bad_time_env)


def test_missing_env_file(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        load_config(tmp_path / "nonexistent.env")


def test_time_pattern_valid() -> None:
    assert TIME_PATTERN.match("00:05:30")
    assert TIME_PATTERN.match("01:23:45")
    assert TIME_PATTERN.match("99:59:59")


def test_time_pattern_invalid() -> None:
    assert not TIME_PATTERN.match("5:30")
    assert not TIME_PATTERN.match("badtime")
    assert not TIME_PATTERN.match("00:05")
    assert not TIME_PATTERN.match("")
