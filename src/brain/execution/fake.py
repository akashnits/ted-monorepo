"""Fake executor used until Hermes integration exists."""

from __future__ import annotations

from brain.execution.types import AgentExecutionRequest, AgentExecutionResult, ExecutionStatus


class FakeAgentExecutor:
    async def execute(self, request: AgentExecutionRequest) -> AgentExecutionResult:
        return AgentExecutionResult(
            status=ExecutionStatus.COMPLETED,
            brief=(
                f"Stub research brief for: {request.user_request}\n\n"
                "The execution path is wired. Real Hermes research will replace this response."
            ),
            artifact_payload={
                "skill_id": request.skill_id,
                "task_type": request.task_type,
                "stub": True,
            },
        )

