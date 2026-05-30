"""Agent execution contracts."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import Field

from brain.types import AppModel


class ExecutionStatus(StrEnum):
    COMPLETED = "completed"
    NEEDS_CLARIFICATION = "needs_clarification"
    OUT_OF_SCOPE = "out_of_scope"
    FAILED = "failed"


class AgentExecutionRequest(AppModel):
    user_request: str
    skill_id: str
    task_type: str | None = None
    authorized_context: dict[str, Any] = Field(default_factory=dict)
    constraints: dict[str, Any] = Field(default_factory=dict)


class AgentExecutionResult(AppModel):
    status: ExecutionStatus
    brief: str | None = None
    artifact_payload: dict[str, Any] | None = None
    sources: tuple[dict[str, Any], ...] = ()
    diagnostics: dict[str, Any] | None = None
