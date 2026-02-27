"""Release processing loop with per-release error isolation.

Wraps each release in a try/except so a single failure doesn't
abort the entire batch. Collects results and prints a summary.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from bhdup.log import Step, log, error


@dataclass
class ReleaseResult:
    """Outcome of processing a single release."""

    name: str
    success: bool = False
    error_message: str = ""


@dataclass
class BatchResult:
    """Aggregate outcome of a full batch run."""

    results: list[ReleaseResult] = field(default_factory=list)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.success)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if not r.success)

    def summary(self) -> str:
        lines = [f"\nBatch complete: {self.passed} passed, {self.failed} failed"]
        for r in self.results:
            status = "PASS" if r.success else "FAIL"
            detail = f" — {r.error_message}" if r.error_message else ""
            lines.append(f"  [{status}] {r.name}{detail}")
        return "\n".join(lines)


def cleanup_release_temp(release_dir: Path) -> None:
    """Remove temp files left by a failed release.

    Cleans up .torrent, .png, mediainfo.txt, tmp files, and
    the .files staging directory for the given release.
    """
    working = release_dir.parent
    staging = working / f"{release_dir.name}.files"

    # Remove known temp file patterns
    for pattern in ["*.png", "tmp*", "mediainfo.txt"]:
        for f in working.glob(pattern):
            try:
                f.unlink()
            except OSError:
                pass

    # Remove release-specific torrent
    torrent = working / f"{release_dir.name}.torrent"
    try:
        torrent.unlink()
    except OSError:
        pass

    # Remove staging directory
    if staging.is_dir():
        import shutil

        shutil.rmtree(staging, ignore_errors=True)


def process_release(release_dir: Path, **kwargs: object) -> None:
    """Process a single release directory.

    This is a placeholder that will be filled in when the main
    script is fully modularised. For now it demonstrates the
    isolation pattern.

    Args:
        release_dir: Path to the release folder.
        **kwargs: Upload parameters (category, pack, live, anon, etc.)
    """
    log(Step.START, "processing", release=release_dir.name)

    # Each step would be called here:
    # 1. hash_torrent(...)
    # 2. dump_mediainfo(...)
    # 3. take_screenshots(...)
    # 4. upload_imgbox(...)
    # 5. lookup_metadata(...)
    # 6. post_to_bhd(...)

    log(Step.DONE, "finished", release=release_dir.name)


def run_batch(
    releases: list[Path],
    dry_run: bool = False,
    **kwargs: object,
) -> BatchResult:
    """Process all releases with per-release error isolation.

    Each release is wrapped in try/except. On failure, temp files
    are cleaned up and the loop continues with the next release.
    """
    batch = BatchResult()

    for release_dir in releases:
        result = ReleaseResult(name=release_dir.name)
        try:
            if dry_run:
                log(Step.START, "dry run — skipping", release=release_dir.name)
            else:
                process_release(release_dir, **kwargs)
            result.success = True
        except Exception as exc:
            result.error_message = str(exc)
            error(f"{exc}", release=release_dir.name)
            cleanup_release_temp(release_dir)
        batch.results.append(result)

    log(Step.DONE, batch.summary())
    return batch
