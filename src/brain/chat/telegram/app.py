"""Telegram bot application bootstrap."""

from __future__ import annotations

from telegram.ext import Application, ApplicationBuilder, CallbackQueryHandler, MessageHandler, filters

from brain.config import Settings, get_settings
from brain.errors import ConfigError
from brain.orchestration import RequestOrchestrator
from brain.chat.telegram.handlers import handle_callback, handle_message


def build_application(
    settings: Settings | None = None,
    orchestrator: RequestOrchestrator | None = None,
) -> Application:
    resolved = settings or get_settings()
    if not resolved.telegram_bot_token:
        raise ConfigError("TED_TELEGRAM_BOT_TOKEN is required to run the Telegram gateway.")

    application = ApplicationBuilder().token(resolved.telegram_bot_token).build()
    application.bot_data["orchestrator"] = orchestrator or RequestOrchestrator()
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    return application


def run_polling(settings: Settings | None = None) -> None:
    application = build_application(settings=settings)
    application.run_polling()

