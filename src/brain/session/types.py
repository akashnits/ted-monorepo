"""Session state contracts."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from brain.types import AppModel


class ActiveSession(AppModel):
    session_id: UUID
    user_id: UUID
    started_at: datetime
    last_activity_at: datetime
    expires_at: datetime
    temporary_instructions: dict | None = None
    pending_state: dict | None = None
