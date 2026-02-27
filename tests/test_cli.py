"""Tests for bhdup.cli module."""

from __future__ import annotations

import argparse

from bhdup.cli import build_parser, resolve_args


def test_build_parser_defaults() -> None:
    parser = build_parser()
    args = parser.parse_args([])
    assert args.category is None
    assert args.pack is None
    assert args.live is None
    assert args.anon is None
    assert args.dry_run is False


def test_build_parser_all_flags() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "--category",
            "1",
            "--pack",
            "0",
            "--live",
            "1",
            "--anon",
            "0",
            "--dry-run",
        ]
    )
    assert args.category == 1
    assert args.pack == 0
    assert args.live == 1
    assert args.anon == 0
    assert args.dry_run is True


def test_resolve_args_movie_sets_pack_zero() -> None:
    args = argparse.Namespace(category=1, pack=None, live=1, anon=0, dry_run=False, verbose=False)
    resolved = resolve_args(args)
    assert resolved.pack == 0
