"""User identity contracts."""

from __future__ import annotations

from uuid import UUID

from brain.types import AppModel


class UserIdentity(AppModel):
    user_id: UUID
    platform: str
    platform_user_id: str
    username: str | None = None
    display_name: str | None = None
