"""Platform-neutral chat contracts."""

from __future__ import annotations

from typing import Literal

from brain.types import AppModel


class ChatButton(AppModel):
    label: str
    action_id: str
    action_value: str | None = None


class ChatButtonGroup(AppModel):
    buttons: tuple[ChatButton, ...]


class ChatMessage(AppModel):
    platform: str
    platform_user_id: str
    platform_chat_id: str
    message_id: str
    text: str
    username: str | None = None
    display_name: str | None = None


class ChatAction(AppModel):
    platform: str
    platform_user_id: str
    platform_chat_id: str
    message_id: str
    action_id: str
    action_value: str | None = None


class ChatResponse(AppModel):
    text: str
    buttons: tuple[ChatButtonGroup, ...] = ()
    replace_message: bool = False
    parse_mode: Literal["plain", "markdown"] = "plain"

