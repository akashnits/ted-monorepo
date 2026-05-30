"""Temporary session management."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Protocol
from uuid import UUID

from brain.session.types import ActiveSession


class SessionService(Protocol):
    async def get_active_session(self, user_id: UUID) -> ActiveSession | None:
        """Return the active temporary session, if any."""

    async def start_session(self, user_id: UUID) -> ActiveSession:
        """Start or refresh a temporary session."""

    async def end_session(self, user_id: UUID) -> bool:
        """End the active temporary session. Returns true when one existed."""


class InMemorySessionService:
    """Local session manager used by CLI and tests."""

    def __init__(self, session_ttl: timedelta = timedelta(hours=8)) -> None:
        self._session_ttl = session_ttl
        self._sessions: dict[UUID, ActiveSession] = {}

    async def get_active_session(self, user_id: UUID) -> ActiveSession | None:
        session = self._sessions.get(user_id)
        if not session:
            return None
        now = datetime.now(UTC)
        if session.expires_at <= now:
            self._sessions.pop(user_id, None)
            return None
        refreshed = session.model_copy(update={"last_activity_at": now})
        self._sessions[user_id] = refreshed
        return refreshed

    async def start_session(self, user_id: UUID) -> ActiveSession:
        now = datetime.now(UTC)
        session = ActiveSession(
            session_id=uuid.uuid4(),
            user_id=user_id,
            started_at=now,
            last_activity_at=now,
            expires_at=now + self._session_ttl,
        )
        self._sessions[user_id] = session
        return session

    async def end_session(self, user_id: UUID) -> bool:
        return self._sessions.pop(user_id, None) is not None
