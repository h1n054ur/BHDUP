# Contributing to BHDUP

Thanks for your interest. Here's how to set up a development environment and submit changes.

## Dev Setup

```bash
git clone https://github.com/h1n054ur/BHDUP.git
cd BHDUP
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest tests/ -v
```

## Linting

```bash
ruff check bhdup/ tests/
ruff format bhdup/ tests/
```

## Branch Naming

- `feat/short-description` for new features
- `fix/short-description` for bug fixes
- `docs/short-description` for documentation
- `refactor/short-description` for refactoring
- `test/short-description` for test additions
- `ci/short-description` for CI changes

## Commit Messages

Follow conventional commits:

```
feat: add argparse CLI with interactive fallback
fix: handle missing TMDB results gracefully
test: add pytest suite for config module
docs: update README with new CLI flags
ci: add GitHub Actions workflow
refactor: split monolithic script into modules
chore: expand ruff config
```

## Pull Requests

1. Create a feature branch from `main`
2. Make your changes
3. Run `ruff check` and `pytest` locally
4. Open a PR against `main`
5. Describe what changed and why in the PR body

## Code Style

- Python 3.11+
- Ruff for linting and formatting (config in `pyproject.toml`)
- Type hints where practical
- Docstrings on all public functions

## Package Layout

```
bhdup/
  __init__.py      Package metadata
  cli.py           Argument parsing and entry point
  config.py        .env loading and validation
  imgbox.py        imgbox BBCode parsing
  log.py           Structured logging
  metadata.py      TMDB/IMDb lookups
  paths.py         Pathlib utilities
  preflight.py     System binary checks
  runner.py        Batch processing loop
  shell.py         Subprocess wrappers
  types.py         Type definitions
tests/
  test_cli.py
  test_config.py
  test_imgbox.py
  test_paths.py
  test_preflight.py
```
