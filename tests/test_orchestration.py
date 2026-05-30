import pytest

from brain.chat.types import ChatAction, ChatMessage
from brain.orchestration import RequestOrchestrator


@pytest.mark.asyncio
async def test_orchestrator_handles_start_command() -> None:
    response = await RequestOrchestrator().handle_message(
        ChatMessage(
            platform="test",
            platform_user_id="user-1",
            platform_chat_id="chat-1",
            message_id="message-1",
            text="/start",
        )
    )

    assert response.text == "Ted is ready. Send an investment research request."


@pytest.mark.asyncio
async def test_orchestrator_runs_fake_research_flow() -> None:
    response = await RequestOrchestrator().handle_message(
        ChatMessage(
            platform="test",
            platform_user_id="user-1",
            platform_chat_id="chat-1",
            message_id="message-1",
            text="Analyze TCS",
        )
    )

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
