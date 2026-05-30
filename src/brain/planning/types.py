"""Task planning contracts."""

from __future__ import annotations

from enum import StrEnum

from brain.types import AppModel


class PlanStatus(StrEnum):
    READY = "ready"
    NEEDS_CLARIFICATION = "needs_clarification"
    UNSUPPORTED = "unsupported"
    NEEDS_CONTEXT_CONFIRMATION = "needs_context_confirmation"


class TaskPlan(AppModel):
    status: PlanStatus
    intent: str | None = None
    selected_skill_id: str | None = None
    task_type: str | None = None
    context_recommendations: tuple[str, ...] = ()
    clarification_question: str | None = None
    unsupported_reason: str | None = None

