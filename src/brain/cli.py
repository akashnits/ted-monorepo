"""Command-line entry point for the project."""

from __future__ import annotations

import argparse
import asyncio

from . import __version__
from brain.chat.types import ChatMessage, ChatResponse
from brain.orchestration import RequestOrchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ted",
        description="Ted personal assistant.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
    )
    subparsers = parser.add_subparsers(dest="command")
    ask_parser = subparsers.add_parser("ask", help="Run a request through the local skeleton.")
    ask_parser.add_argument("text", help="Request text.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "ask":
        response = asyncio.run(_ask(args.text))
        print(response.text)
    return 0


async def _ask(text: str) -> ChatResponse:
    orchestrator = RequestOrchestrator()
    return await orchestrator.handle_message(
        ChatMessage(
            platform="cli",
            platform_user_id="local",
            platform_chat_id="local",
            message_id="local",
            text=text,
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
