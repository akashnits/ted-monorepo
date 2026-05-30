"""Personal context contracts."""

from __future__ import annotations

from uuid import UUID

from brain.types import AppModel


class ProfileContext(AppModel):
    user_id: UUID
    is_configured: bool
    base_currency: str | None = None
    primary_markets: tuple[str, ...] = ()
    default_investment_horizon: str | None = None
    risk_style: str | None = None

    def to_display_text(self) -> str:
        if not self.is_configured:
            return "No profile saved yet."

        parts = []
        if self.base_currency:
            parts.append(f"Currency: {self.base_currency}")
        if self.primary_markets:
            parts.append(f"Markets: {', '.join(self.primary_markets)}")
        if self.default_investment_horizon:
            parts.append(f"Horizon: {self.default_investment_horizon}")
        if self.risk_style:
            parts.append(f"Risk style: {self.risk_style}")
        return "\n".join(parts) if parts else "Profile is saved, but has no displayable fields yet."


class PortfolioContext(AppModel):
    user_id: UUID
    is_configured: bool
    holding_count: int = 0
    requires_confirmation: bool = True

    def to_display_text(self) -> str:
        if not self.is_configured:
            return "No portfolio saved yet."
        suffix = " It will require confirmation before use." if self.requires_confirmation else ""
        return f"Portfolio saved with {self.holding_count} holdings.{suffix}"
