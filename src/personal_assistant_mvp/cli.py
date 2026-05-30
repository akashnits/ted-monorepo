"""Command-line entry point for the project."""

from __future__ import annotations

import argparse

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="personal-assistant-mvp",
        description="Starter CLI for the Personal Assistant MVP project.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
    )
    return parser


def main() -> int:
    build_parser().parse_args()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

