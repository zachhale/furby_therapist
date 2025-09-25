"""
Entry point for running furby_therapist as a module.

This allows the package to be run with:
    python3 -m furby_therapist
"""

from .cli.main import main

if __name__ == "__main__":
    main()