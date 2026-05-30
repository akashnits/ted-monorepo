"""Convert Telegram updates into platform-neutral chat contracts."""

from __future__ import annotations

from telegram import Update

from brain.chat.types import ChatAction, ChatMessage


def message_from_update(update: Update) -> ChatMessage | None:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    if message is None or user is None or chat is None or message.text is None:
        return None

    return ChatMessage(
        platform="telegram",
        platform_user_id=str(user.id),
        platform_chat_id=str(chat.id),
        message_id=str(message.message_id),
        text=message.text,
        username=user.username,
        display_name=user.full_name,
    )


def action_from_update(update: Update) -> ChatAction | None:
    query = update.callback_query
    user = update.effective_user
    chat = update.effective_chat
    if query is None or user is None or chat is None or query.message is None:
        return None

    return ChatAction(
        platform="telegram",
        platform_user_id=str(user.id),
        platform_chat_id=str(chat.id),
        message_id=str(query.message.message_id),
        action_id=query.data or "",
    )

