"""Fake planner used to prove the application flow."""

from __future__ import annotations

from brain.planning.types import PlanStatus, TaskPlan


class FakeTaskPlanner:
    async def plan(self, user_request: str) -> TaskPlan:
        return TaskPlan(
            status=PlanStatus.READY,
            intent="investment_research",
            selected_skill_id="investment_research",
            task_type="single_equity_research",
            context_recommendations=(),
        )

