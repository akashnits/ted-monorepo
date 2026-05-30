"""Read-only personal context access."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from brain.context.types import PortfolioContext, ProfileContext


class ContextService(Protocol):
    async def get_profile(self, user_id: UUID) -> ProfileContext:
        """Return explicit profile context for a user."""

    async def get_portfolio(self, user_id: UUID) -> PortfolioContext:
        """Return portfolio availability without exposing holdings by default."""


class InMemoryContextService:
    """Local context store used before the database-backed service is wired."""

    def __init__(self) -> None:
        self._profiles: dict[UUID, ProfileContext] = {}
        self._portfolios: dict[UUID, PortfolioContext] = {}

    async def get_profile(self, user_id: UUID) -> ProfileContext:
        return self._profiles.get(user_id, ProfileContext(user_id=user_id, is_configured=False))

    async def get_portfolio(self, user_id: UUID) -> PortfolioContext:
        return self._portfolios.get(user_id, PortfolioContext(user_id=user_id, is_configured=False))

    def set_profile(self, profile: ProfileContext) -> None:
        self._profiles[profile.user_id] = profile

    def set_portfolio(self, portfolio: PortfolioContext) -> None:
        self._portfolios[portfolio.user_id] = portfolio
