import pytest

from brain.chat.cli import CliChat


@pytest.mark.asyncio
async def test_cli_chat_runs_until_exit() -> None:
    inputs = iter(["/start", "Analyze TCS", "/exit"])
    outputs: list[str] = []

    chat = CliChat(
        input_fn=lambda _: next(inputs),
        output_fn=outputs.append,
    )

    await chat.run()

    assert outputs[0] == "Ted CLI chat. Type /exit to quit."
    assert "Ted is ready" in outputs[1]
    assert "Stub research brief for: Analyze TCS" in outputs[2]


@pytest.mark.asyncio
async def test_cli_chat_handles_eof() -> None:
    outputs: list[str] = []

    def raise_eof(_: str) -> str:
        raise EOFError

    chat = CliChat(input_fn=raise_eof, output_fn=outputs.append)

    await chat.run()

    assert outputs == ["Ted CLI chat. Type /exit to quit.", ""]
