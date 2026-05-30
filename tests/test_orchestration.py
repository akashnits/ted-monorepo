import pytest

from brain.chat.types import ChatAction, ChatMessage
from brain.context import InMemoryContextService, PortfolioContext, ProfileContext
from brain.orchestration import RequestOrchestrator
from brain.users import InMemoryUserService


def _message(text: str, platform_user_id: str = "user-1") -> ChatMessage:
    return ChatMessage(
        platform="test",
        platform_user_id=platform_user_id,
        platform_chat_id="chat-1",
        message_id="message-1",
        text=text,
    )


@pytest.mark.asyncio
async def test_orchestrator_handles_start_command() -> None:
    response = await RequestOrchestrator().handle_message(_message("/start"))

    assert response.text == "Ted is ready. Send an investment research request."


@pytest.mark.asyncio
async def test_orchestrator_runs_fake_research_flow() -> None:
    response = await RequestOrchestrator().handle_message(_message("Analyze TCS"))

    assert "Stub research brief for: Analyze TCS" in response.text


@pytest.mark.asyncio
async def test_orchestrator_handles_unwired_action() -> None:
    response = await RequestOrchestrator().handle_action(
        ChatAction(
            platform="test",
            platform_user_id="user-1",
            platform_chat_id="chat-1",
            message_id="message-1",
            action_id="portfolio.confirm",
        )
    )

    assert response.text == "Action `portfolio.confirm` is not wired yet."


@pytest.mark.asyncio
async def test_orchestrator_shows_empty_profile_and_portfolio() -> None:
    orchestrator = RequestOrchestrator()

    profile = await orchestrator.handle_message(_message("/profile"))
    portfolio = await orchestrator.handle_message(_message("/portfolio"))

    assert profile.text == "No profile saved yet."
    assert portfolio.text == "No portfolio saved yet."


@pytest.mark.asyncio
async def test_orchestrator_shows_saved_context() -> None:
    user_service = InMemoryUserService()
    context_service = InMemoryContextService()
    user = await user_service.resolve_user(_message("/start"))
    context_service.set_profile(
        ProfileContext(
            user_id=user.user_id,
            is_configured=True,
            base_currency="INR",
            primary_markets=("India", "US"),
            default_investment_horizon="long term",
            risk_style="balanced",
        )
    )
    context_service.set_portfolio(
        PortfolioContext(
            user_id=user.user_id,
            is_configured=True,
            holding_count=3,
        )
    )
    orchestrator = RequestOrchestrator(
        user_service=user_service,
        context_service=context_service,
    )

    profile = await orchestrator.handle_message(_message("/profile"))
    portfolio = await orchestrator.handle_message(_message("/portfolio"))

    assert "Currency: INR" in profile.text
    assert "Markets: India, US" in profile.text
    assert portfolio.text == "Portfolio saved with 3 holdings. It will require confirmation before use."


@pytest.mark.asyncio
async def test_orchestrator_starts_and_ends_session() -> None:
    orchestrator = RequestOrchestrator()

    started = await orchestrator.handle_message(_message("/start_session"))
    ended = await orchestrator.handle_message(_message("/end_session"))
    ended_again = await orchestrator.handle_message(_message("/end_session"))

    assert started.text.startswith("Session started. It expires at ")
    assert ended.text == "Session ended."
    assert ended_again.text == "No active session to end."
