"""BHDUP — Automated media uploading tool.

Package layout:

    bhdup/
    ├── __init__.py      This file — package metadata
    ├── cli.py           Argument parsing and entry point
    ├── config.py        .env loading and validation
    ├── imgbox.py        imgbox BBCode parsing
    ├── log.py           Structured logging
    ├── metadata.py      TMDB/IMDb lookups
    ├── paths.py         Pathlib utilities
    ├── preflight.py     System binary checks
    ├── runner.py        Batch processing loop
    ├── shell.py         Subprocess wrappers
    └── types.py         Type definitions
"""

__version__ = "2.0.0"
