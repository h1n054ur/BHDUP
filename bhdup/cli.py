"""Command-line interface for BHDUP.

Provides argparse-based argument parsing with fallback to interactive
prompts when flags are not provided.
"""

from __future__ import annotations

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="bhdup",
        description="Automated media uploading tool",
    )
    parser.add_argument(
        "--category",
        type=int,
        choices=[1, 2],
        help="1 for Movie, 2 for TV",
    )
    parser.add_argument(
        "--pack",
        type=int,
        choices=[0, 1],
        help="1 if season pack, 0 if not (TV only)",
    )
    parser.add_argument(
        "--live",
        type=int,
        choices=[0, 1],
        help="1 for live upload, 0 for draft",
    )
    parser.add_argument(
        "--anon",
        type=int,
        choices=[0, 1],
        help="1 for anonymous, 0 for named",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="process releases without uploading",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="show detailed output during processing",
    )
    return parser


def _prompt_int(prompt: str, valid: set[int]) -> int:
    """Prompt the user until they enter a valid integer."""
    while True:
        try:
            value = int(input(prompt))
            if value in valid:
                return value
        except (ValueError, EOFError):
            pass
        print(f"Please enter one of: {sorted(valid)}", file=sys.stderr)


def resolve_args(args: argparse.Namespace) -> argparse.Namespace:
    """Fill in any missing arguments with interactive prompts.

    If all required flags are provided, no prompts are shown —
    allowing fully non-interactive batch operation.
    """
    if args.category is None:
        args.category = _prompt_int("Enter 1 for Movie or 2 for TV: ", {1, 2})

    if args.category == 2 and args.pack is None:
        args.pack = _prompt_int("Enter 1 if Pack or 0 if not a Pack: ", {0, 1})
    elif args.category == 1:
        args.pack = 0

    if args.live is None:
        args.live = _prompt_int("Enter 1 for Live or 0 for Draft: ", {0, 1})

    if args.anon is None:
        args.anon = _prompt_int("Enter 1 for Anonymous or 0 for Named: ", {0, 1})

    return args


def main() -> None:
    """Entry point for the bhdup command."""
    parser = build_parser()
    args = parser.parse_args()
    args = resolve_args(args)

    # Import here to avoid circular imports and allow the CLI
    # module to be tested independently
    from bhdup.log import Step, log

    log(
        Step.START,
        f"category={args.category} pack={args.pack} "
        f"live={args.live} anon={args.anon} dry_run={args.dry_run}",
    )

    if args.dry_run:
        log(Step.DONE, "Dry run complete — no uploads performed")
        return

    log(Step.DONE, "Processing complete")
