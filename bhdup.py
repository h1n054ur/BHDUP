#!/usr/bin/env python3
"""Legacy entry point — delegates to the bhdup package.

For the new CLI interface, run: bhdup --help
Or: python -m bhdup --help

This file is kept for backwards compatibility. All logic now
lives in the bhdup/ package modules.
"""

from bhdup.cli import main

if __name__ == "__main__":
    main()
