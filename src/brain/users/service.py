"""User identity resolution."""

from __future__ import annotations

import uuid
from typing import Protocol

from brain.chat.types import ChatMessage
from brain.users.types import UserIdentity


class UserService(Protocol):
    async def resolve_user(self, message: ChatMessage) -> UserIdentity:
        """Return the durable user identity for a chat message."""


class InMemoryUserService:
    """Local user resolver used before the database-backed service is wired."""

    def __init__(self) -> None:
        self._users: dict[tuple[str, str], UserIdentity] = {}

    async def resolve_user(self, message: ChatMessage) -> UserIdentity:
        key = (message.platform, message.platform_user_id)
        existing = self._users.get(key)
        if existing:
            updated = existing.model_copy(
                update={
                    "username": message.username or existing.username,
                    "display_name": message.display_name or existing.display_name,
                }
            )
            self._users[key] = updated
            return updated

        user = UserIdentity(
            user_id=uuid.uuid5(uuid.NAMESPACE_URL, f"ted:{message.platform}:{message.platform_user_id}"),
            platform=message.platform,
            platform_user_id=message.platform_user_id,
            username=message.username,
            display_name=message.display_name,
        )
        self._users[key] = user
        return user
