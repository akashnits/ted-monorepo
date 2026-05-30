# 01. Chat Gateway

## Purpose

The Chat Gateway receives user messages from chat platforms, normalizes them into internal application requests, sends them to the request orchestrator, and renders orchestrator responses back to the same platform.

Telegram is the first supported adapter. The gateway should still be shaped so Slack, WhatsApp, Discord, Signal, or CLI can be added later without changing the core workflow.

```text
Telegram
-> Chat Gateway
-> Request Orchestrator
-> Context, Session, Confirmation
-> Agent Runtime Adapter
-> Hermes
```

## Current Scope

- Telegram adapter
- Command handling
- Natural language message handling
- Inline button callback handling
- Response rendering
- Error-safe message delivery

Additional chat platforms are out of scope for the initial release, but the gateway contract should not be Telegram-specific.

## Responsibilities

- Receive Telegram updates
- Normalize Telegram messages into a platform-neutral request object
- Normalize Telegram button callbacks into a platform-neutral action object
- Map Telegram user identity to platform identity fields
- Pass normalized input to `RequestOrchestrator`
- Render text responses
- Render button responses
- Split long responses when needed
- Handle Telegram send and edit failures gracefully

## Non-Responsibilities

- Investment research logic
- Direct LLM or Hermes calls
- Research tool calls
- Profile inference
- Portfolio analysis
- Session policy decisions
- Artifact persistence
- Skill routing decisions

## Data Contracts

Incoming chat message:

```python
@dataclass(frozen=True)
class ChatMessage:
    platform: Literal["telegram"]
    platform_user_id: str
    platform_chat_id: str
    message_id: str
    text: str
    username: str | None = None
    display_name: str | None = None
```

Incoming chat action:

```python
@dataclass(frozen=True)
class ChatAction:
    platform: Literal["telegram"]
    platform_user_id: str
    platform_chat_id: str
    message_id: str
    action_id: str
    action_value: str | None = None
```

Outgoing chat response:

```python
@dataclass(frozen=True)
class ChatResponse:
    text: str
    buttons: list[ChatButtonGroup] | None = None
    replace_message: bool = False
    parse_mode: Literal["plain", "markdown"] = "plain"
```

Button model:

```python
@dataclass(frozen=True)
class ChatButton:
    label: str
    action_id: str
    action_value: str | None = None


@dataclass(frozen=True)
class ChatButtonGroup:
    buttons: list[ChatButton]
```

## Telegram Commands

`/start`

Creates or fetches the user through the orchestrator and returns a short introduction.

`/profile`

Shows explicit saved profile fields and missing fields.

`/portfolio`

Shows a saved portfolio summary or says none is configured.

`/start_session`

Starts a temporary session and clears or replaces any previous active session.

`/end_session`

Ends the current session and clears temporary task state.

Natural language messages are passed to the orchestrator as possible investment research requests.

## Portfolio Confirmation UX

Use inline buttons for portfolio confirmation:

```text
Use saved portfolio context?

[Use portfolio] [Continue without] [Cancel]
```

Button action IDs:

```text
portfolio.confirm
portfolio.skip
task.cancel
```

The Chat Gateway must not interpret these actions beyond normalization. The orchestrator and session flow decide what happens.

## Error Behavior

If the orchestrator fails unexpectedly, the gateway should send a plain fallback response:

```text
I could not complete that request. Please try again.
```

If Hermes or research tools fail, the gateway should render the orchestrator response. It should not inspect agent failures directly.

If a Telegram message is too long:

- Split it into multiple messages
- Keep buttons only on the final message when controls are needed

## Implementation Tasks

1. Add chat domain models:
   - `ChatMessage`
   - `ChatAction`
   - `ChatResponse`
   - `ChatButton`
   - `ChatButtonGroup`
2. Add Telegram adapter:
   - bot bootstrap
   - command handlers
   - text message handler
   - callback query handler
3. Add response renderer:
   - plain text rendering
   - markdown rendering when needed
   - inline keyboard rendering
   - long-message splitting
4. Add orchestrator interface placeholder:
   - `handle_message(message: ChatMessage) -> ChatResponse`
   - `handle_action(action: ChatAction) -> ChatResponse`
5. Add tests:
   - Telegram update normalization
   - callback normalization
   - response-to-inline-keyboard conversion
   - long-message splitting
   - command dispatch

## Acceptance Criteria

- Telegram `/start` reaches the orchestrator as a normalized message
- Telegram text messages reach the orchestrator as `ChatMessage`
- Telegram inline button clicks reach the orchestrator as `ChatAction`
- Gateway can render plain text responses
- Gateway can render inline buttons
- Gateway can split oversized Telegram messages
- Gateway contains no investment-specific reasoning
- Gateway does not call Hermes directly
- Adding another chat platform later does not require changing orchestrator input contracts

