from brain.chat.telegram.renderer import keyboard_markup, split_text
from brain.chat.types import ChatButton, ChatButtonGroup


def test_split_text_keeps_short_text_intact() -> None:
    assert split_text("hello", limit=10) == ["hello"]


def test_split_text_splits_long_text() -> None:
    assert split_text("hello world", limit=5) == ["hello", "world"]


def test_keyboard_markup_uses_action_value_when_present() -> None:
    markup = keyboard_markup(
        (
            ChatButtonGroup(
                buttons=(
                    ChatButton(
                        label="Use portfolio",
                        action_id="portfolio.confirm",
                        action_value="confirm-123",
                    ),
                )
            ),
        )
    )

    assert markup is not None
    assert markup.inline_keyboard[0][0].text == "Use portfolio"
    assert markup.inline_keyboard[0][0].callback_data == "confirm-123"


def test_keyboard_markup_falls_back_to_action_id() -> None:
    markup = keyboard_markup(
        (
            ChatButtonGroup(
                buttons=(ChatButton(label="Cancel", action_id="task.cancel"),),
            ),
        )
    )

    assert markup is not None
    assert markup.inline_keyboard[0][0].callback_data == "task.cancel"
