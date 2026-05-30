"""Interactive CLI chat adapter."""

from __future__ import annotations

from collections.abc import Callable

from brain.chat.types import ChatMessage, ChatResponse
from brain.orchestration import RequestOrchestrator

InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


class CliChat:
    def __init__(
        self,
        orchestrator: RequestOrchestrator | None = None,
        input_fn: InputFn = input,
        output_fn: OutputFn = print,
    ) -> None:
        self._orchestrator = orchestrator or RequestOrchestrator()
        self._input = input_fn
        self._output = output_fn

    async def run(self) -> None:
        self._output("Ted CLI chat. Type /exit to quit.")
        counter = 0
        while True:
            try:
                text = self._input("Ted> ").strip()
            except EOFError:
                self._output("")
                return

            if not text:
                continue
            if text in {"/exit", "/quit"}:
                return

            counter += 1
            response = await self._orchestrator.handle_message(
                ChatMessage(
                    platform="cli",
                    platform_user_id="cli-local",
                    platform_chat_id="cli-local",
                    message_id=str(counter),
                    text=text,
                    display_name="Local CLI",
                )
            )
            self._render(response)

    def _render(self, response: ChatResponse) -> None:
        self._output(response.text)
        for group in response.buttons:
            labels = " ".join(f"[{button.label}]" for button in group.buttons)
            if labels:
                self._output(labels)

