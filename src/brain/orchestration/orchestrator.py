"""Request orchestrator skeleton."""

from __future__ import annotations

from brain.chat.types import ChatAction, ChatMessage, ChatResponse
from brain.execution.types import AgentExecutionRequest, ExecutionStatus
from brain.execution.fake import FakeAgentExecutor
from brain.planning.fake import FakeTaskPlanner
from brain.planning.types import PlanStatus


class RequestOrchestrator:
    def __init__(
        self,
        planner: FakeTaskPlanner | None = None,
        executor: FakeAgentExecutor | None = None,
    ) -> None:
        self._planner = planner or FakeTaskPlanner()
        self._executor = executor or FakeAgentExecutor()

    async def handle_message(self, message: ChatMessage) -> ChatResponse:
        text = message.text.strip()
        if not text:
            return ChatResponse(text="Send me a request to research.")

        if text.startswith("/"):
            return self._handle_command(text)

        plan = await self._planner.plan(text)
        if plan.status == PlanStatus.UNSUPPORTED:
            return ChatResponse(text=plan.unsupported_reason or "I cannot handle that request yet.")
        if plan.status == PlanStatus.NEEDS_CLARIFICATION:
            return ChatResponse(text=plan.clarification_question or "Can you clarify that request?")
        if plan.status == PlanStatus.NEEDS_CONTEXT_CONFIRMATION:
            return ChatResponse(text="I need confirmation before using additional context.")
        if not plan.selected_skill_id:
            return ChatResponse(text="I could not decide how to handle that request.")

        result = await self._executor.execute(
            AgentExecutionRequest(
                user_request=text,
                skill_id=plan.selected_skill_id,
                task_type=plan.task_type,
            )
        )
        if result.status == ExecutionStatus.COMPLETED and result.brief:
            return ChatResponse(text=result.brief)
        if result.status == ExecutionStatus.NEEDS_CLARIFICATION and result.brief:
            return ChatResponse(text=result.brief)
        if result.status == ExecutionStatus.OUT_OF_SCOPE:
            return ChatResponse(text=result.brief or "That request is out of scope.")
        return ChatResponse(text="I could not complete that request.")

    async def handle_action(self, action: ChatAction) -> ChatResponse:
        return ChatResponse(text=f"Action `{action.action_id}` is not wired yet.")

    def _handle_command(self, command_text: str) -> ChatResponse:
        command = command_text.split(maxsplit=1)[0]
        if command == "/start":
            return ChatResponse(text="Ted is ready. Send an investment research request.")
        if command == "/profile":
            return ChatResponse(text="Profile support is not wired yet.")
        if command == "/portfolio":
            return ChatResponse(text="Portfolio support is not wired yet.")
        if command == "/start_session":
            return ChatResponse(text="Session support is not wired yet.")
        if command == "/end_session":
            return ChatResponse(text="Session support is not wired yet.")
        return ChatResponse(text=f"Unknown command: {command}")
