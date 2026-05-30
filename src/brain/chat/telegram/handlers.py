"""Telegram update handlers."""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from brain.chat.telegram.normalization import action_from_update, message_from_update
from brain.chat.telegram.renderer import render_response
from brain.orchestration import RequestOrchestrator


def _get_orchestrator(context: ContextTypes.DEFAULT_TYPE) -> RequestOrchestrator:
    orchestrator = context.application.bot_data.get("orchestrator")
    if not isinstance(orchestrator, RequestOrchestrator):
        orchestrator = RequestOrchestrator()
        context.application.bot_data["orchestrator"] = orchestrator
    return orchestrator


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_message = message_from_update(update)
    if chat_message is None:
        return

    response = await _get_orchestrator(context).handle_message(chat_message)
    await render_response(update, context, response)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_action = action_from_update(update)
    if chat_action is None:
        return

    response = await _get_orchestrator(context).handle_action(chat_action)
    await render_response(update, context, response)

