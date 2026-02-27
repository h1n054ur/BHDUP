<h1 align="center">
	<img width="400" src="bhdup-logo.png" alt="BHDUP">
</h1>

<p align="center">
  <strong>Automated media uploading tool for BHD</strong>
</p>

<p align="center">
  <a href="https://github.com/h1n054ur/BHDUP"><img src="https://img.shields.io/github/stars/h1n054ur/BHDUP?style=social" alt="Stars"></a>
  <a href="https://github.com/h1n054ur/BHDUP"><img src="https://img.shields.io/github/forks/h1n054ur/BHDUP?style=social" alt="Forks"></a>
  <a href="https://github.com/h1n054ur/BHDUP/blob/main/LICENSE"><img src="https://img.shields.io/github/license/h1n054ur/BHDUP" alt="License"></a>
</p>

---

BHDUP automates the process of creating torrents, generating screenshots, extracting mediainfo, and uploading releases to BHD via their API. It handles TMDB/IMDb lookups, imgbox thumbnail hosting, and supports both movie and TV categories.

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| Python | >= 3.11 | [python.org](https://www.python.org/downloads/) |
| ffmpeg | Screenshot generation | `apt install ffmpeg` / `brew install ffmpeg` |
| mktorrent | Torrent file creation | [github.com/Rudde/mktorrent](https://github.com/Rudde/mktorrent) |
| mediainfo | Media metadata extraction | `apt install mediainfo` / `brew install mediainfo` |
| imgbox-cli | Screenshot hosting | `pipx install imgbox-cli` |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/h1n054ur/BHDUP.git
cd BHDUP

# Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Configure
cp .env.example .env
# Edit .env with your API keys (see Configuration below)
```

## Configuration

Edit `.env` with your credentials:

| Variable | Required | Description |
|----------|----------|-------------|
| `TORRENTPASSKEY` | Yes | Your BHD torrent passkey |
| `BHDAPI` | Yes | Your BHD API key |
| `TMDBAPI` | Yes | TMDB v3 API key ([free registration](https://www.themoviedb.org/settings/api)) |
| `SCREEN_SHOT1` - `SCREEN_SHOT6` | No | Screenshot timestamps in `HH:MM:SS` format (defaults provided) |

## Usage

```bash
# Run from a directory containing properly named release folders
python3 bhdup.py
```

The script will prompt for:
- **Category**: Movie (1) or TV (2)
- **Pack**: Season pack or single (TV only)
- **Live**: Upload live or save as draft
- **Anonymous**: Upload anonymously or not

### Directory Structure

```
working-directory/
├── Release.Name.2024.1080p.BluRay.Remux/
│   └── movie.mkv
├── Another.Release.2024.2160p.UHD.Remux/
│   └── movie.mkv
├── bhdup.py
└── .env
```

## Supported Formats

- UHD Remux (2160p Blu-ray)
- BD Remux (1080p Blu-ray)
- DVD Remux
- 2160p, 1080p, 720p
- WEB sources

## Cleanup

If a run fails and leaves temp files:

```bash
rm -r *.files tmp *.png mediainfo.txt *.torrent
```

## License

[GPL-3.0](LICENSE)
