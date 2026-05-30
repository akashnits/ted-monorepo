"""Request orchestrator skeleton."""

from __future__ import annotations

from uuid import UUID

from brain.chat.types import ChatAction, ChatMessage, ChatResponse
from brain.context import ContextService, InMemoryContextService
from brain.execution.fake import FakeAgentExecutor
from brain.execution.types import AgentExecutionRequest, ExecutionStatus
from brain.planning.fake import FakeTaskPlanner
from brain.planning.types import PlanStatus
from brain.session import InMemorySessionService, SessionService
from brain.users import InMemoryUserService, UserService


class RequestOrchestrator:
    def __init__(
        self,
        planner: FakeTaskPlanner | None = None,
        executor: FakeAgentExecutor | None = None,
        user_service: UserService | None = None,
        context_service: ContextService | None = None,
        session_service: SessionService | None = None,
    ) -> None:
        self._planner = planner or FakeTaskPlanner()
        self._executor = executor or FakeAgentExecutor()
        self._users = user_service or InMemoryUserService()
        self._context = context_service or InMemoryContextService()
        self._sessions = session_service or InMemorySessionService()

    async def handle_message(self, message: ChatMessage) -> ChatResponse:
        text = message.text.strip()
        if not text:
            return ChatResponse(text="Send me a request to research.")

        user = await self._users.resolve_user(message)
        if text.startswith("/"):
            return await self._handle_command(text, user.user_id)

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

    async def _handle_command(self, command_text: str, user_id: UUID) -> ChatResponse:
        command = command_text.split(maxsplit=1)[0]
        if command == "/start":
            return ChatResponse(text="Ted is ready. Send an investment research request.")
        if command == "/profile":
            profile = await self._context.get_profile(user_id)
            return ChatResponse(text=profile.to_display_text())
        if command == "/portfolio":
            portfolio = await self._context.get_portfolio(user_id)
            return ChatResponse(text=portfolio.to_display_text())
        if command == "/start_session":
            session = await self._sessions.start_session(user_id)
            expires_at = session.expires_at.strftime("%Y-%m-%d %H:%M UTC")
            return ChatResponse(text=f"Session started. It expires at {expires_at}.")
        if command == "/end_session":
            ended = await self._sessions.end_session(user_id)
            if ended:
                return ChatResponse(text="Session ended.")
            return ChatResponse(text="No active session to end.")
        return ChatResponse(text=f"Unknown command: {command}")
