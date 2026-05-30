"""Render platform-neutral chat responses to Telegram."""

from __future__ import annotations

from collections.abc import Iterable

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import MessageLimit
from telegram.ext import ContextTypes

from brain.chat.types import ChatButtonGroup, ChatResponse


def keyboard_markup(button_groups: Iterable[ChatButtonGroup]) -> InlineKeyboardMarkup | None:
    rows = [
        [
            InlineKeyboardButton(
                button.label,
                callback_data=button.action_value or button.action_id,
            )
            for button in group.buttons
        ]
        for group in button_groups
    ]
    if not rows:
        return None
    return InlineKeyboardMarkup(rows)


def split_text(text: str, limit: int = MessageLimit.MAX_TEXT_LENGTH) -> list[str]:
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    remaining = text
    while len(remaining) > limit:
        split_at = remaining.rfind("\n", 0, limit)
        if split_at <= 0:
            split_at = limit
        chunks.append(remaining[:split_at].rstrip())
        remaining = remaining[split_at:].lstrip()
    if remaining:
        chunks.append(remaining)
    return chunks


async def render_response(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    response: ChatResponse,
) -> None:
    chat = update.effective_chat
    if chat is None:
        return

    chunks = split_text(response.text)
    markup = keyboard_markup(response.buttons)
    parse_mode = None if response.parse_mode == "plain" else response.parse_mode

    for index, chunk in enumerate(chunks):
        reply_markup = markup if index == len(chunks) - 1 else None
        await context.bot.send_message(
            chat_id=chat.id,
            text=chunk,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )

