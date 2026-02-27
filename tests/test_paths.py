"""Tests for bhdup.paths module."""

from __future__ import annotations

from pathlib import Path

import pytest

from bhdup.paths import release_dirs, video_file, temp_dir, torrent_path


def test_release_dirs_filters_project_files(tmp_path: Path) -> None:
    # Create some release dirs and project files
    (tmp_path / "Release.2024.1080p").mkdir()
    (tmp_path / "Another.Release.2024").mkdir()
    (tmp_path / ".git").mkdir()
    (tmp_path / "bhdup").mkdir()
    (tmp_path / "README.md").touch()

    dirs = release_dirs(tmp_path)
    names = [d.name for d in dirs]
    assert "Release.2024.1080p" in names
    assert "Another.Release.2024" in names
    assert ".git" not in names
    assert "bhdup" not in names


def test_release_dirs_empty(tmp_path: Path) -> None:
    assert release_dirs(tmp_path) == []


def test_video_file_finds_mkv(tmp_path: Path) -> None:
    release = tmp_path / "Release"
    release.mkdir()
    (release / "movie.mkv").touch()
    (release / "subs.srt").touch()
    assert video_file(release).name == "movie.mkv"


def test_video_file_fallback(tmp_path: Path) -> None:
    release = tmp_path / "Release"
    release.mkdir()
    (release / "something.bin").touch()
    # Falls back to first file when no video extension found
    assert video_file(release).name == "something.bin"


def test_video_file_empty_raises(tmp_path: Path) -> None:
    release = tmp_path / "Empty"
    release.mkdir()
    with pytest.raises(FileNotFoundError):
        video_file(release)


def test_temp_dir() -> None:
    p = Path("/work/Release.2024.1080p")
    assert temp_dir(p) == Path("/work/Release.2024.1080p.files")


def test_torrent_path() -> None:
    p = Path("/work/Release.2024.1080p")
    assert torrent_path(p) == Path("/work/Release.2024.1080p.torrent")
