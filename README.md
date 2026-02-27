<h1 align="center">
	<img width="400" src="bhdup-logo.png" alt="BHDUP">
</h1>

<p align="center">
  <strong>Media upload automation tool</strong>
</p>

<p align="center">
  <a href="https://github.com/h1n054ur/BHDUP"><img src="https://img.shields.io/github/stars/h1n054ur/BHDUP?style=social" alt="Stars"></a>
  <a href="https://github.com/h1n054ur/BHDUP"><img src="https://img.shields.io/github/forks/h1n054ur/BHDUP?style=social" alt="Forks"></a>
  <a href="https://github.com/h1n054ur/BHDUP/blob/main/LICENSE"><img src="https://img.shields.io/github/license/h1n054ur/BHDUP" alt="License"></a>
</p>

---

> **Note:** I wrote this a while back when I was actively using it. Not sure if it still works with current API versions, but leaving it up in case anyone still finds it useful. The codebase was recently cleaned up and modularised — feel free to fork and adapt.

BHDUP automates the workflow of generating screenshots, extracting mediainfo, looking up metadata from TMDB/IMDb, and uploading via API. It handles batch processing of multiple releases with per-release error isolation.

## Quick Start

```bash
git clone https://github.com/h1n054ur/BHDUP.git
cd BHDUP
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Configuration

Copy `.env.example` to `.env` and fill in your API keys:

| Variable | Required | Description |
|----------|----------|-------------|
| `TORRENTPASSKEY` | Yes | Your passkey |
| `BHDAPI` | Yes | Upload API key |
| `TMDBAPI` | Yes | TMDB v3 API key ([free](https://www.themoviedb.org/settings/api)) |
| `SCREEN_SHOT1` - `SCREEN_SHOT6` | No | Screenshot timestamps (`HH:MM:SS`, defaults provided) |

## Usage

```bash
# Interactive mode
bhdup

# Non-interactive (all flags)
bhdup --category 1 --live 0 --anon 0

# Dry run
bhdup --category 2 --pack 1 --live 0 --anon 0 --dry-run
```

Run from a directory containing release folders. Each folder should have a video file inside.

## Requirements

- Python >= 3.11
- ffmpeg, mktorrent, mediainfo, imgbox-cli on PATH

## Package Layout

```
bhdup/
  cli.py           Argument parsing and entry point
  config.py        .env loading and validation
  imgbox.py        Screenshot hosting output parsing
  log.py           Structured logging
  metadata.py      TMDB/IMDb lookups
  paths.py         Path utilities
  preflight.py     System binary checks
  runner.py        Batch processing with error isolation
  shell.py         Subprocess wrappers
  types.py         Type definitions
```

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -v
ruff check bhdup/ tests/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

## License

[GPL-3.0](LICENSE)
