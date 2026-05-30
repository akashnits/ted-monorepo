# 01. Chat Gateway

## Purpose

The Chat Gateway receives messages from chat platforms, normalizes them into application requests, and renders application responses back to the same platform.

Telegram is the first supported adapter, but the boundary should stay platform-neutral so additional chat surfaces can be added later without changing the core workflow.

```text
Telegram
-> Chat Gateway
-> Request Orchestrator
```

## Responsibilities

- Receive Telegram updates
- Normalize user messages into platform-neutral chat messages
- Normalize button callbacks into platform-neutral chat actions
- Preserve platform identity fields needed by the application
- Pass normalized input to the Request Orchestrator
- Render text responses from the application
- Render button responses from the application
- Split oversized Telegram messages when needed
- Handle Telegram delivery failures without leaking platform errors into core workflow

## Non-Responsibilities

- Product workflow decisions
- Investment research logic
- Skill selection
- Direct Hermes calls
- Research tool calls
- Profile or portfolio decisions
- Session policy
- Artifact persistence

## Interfaces

Incoming platform events should be converted into one of two internal request types:

- `ChatMessage`: normalized user text, platform identity, chat identity, and message identity
- `ChatAction`: normalized button/action input, platform identity, chat identity, message identity, and action identifier

The gateway receives one internal response type from the application:

- `ChatResponse`: response text, optional buttons, optional message replacement intent, and formatting mode

The Request Orchestrator is the only application component the gateway should call.

## Key Policies

- Telegram-specific objects must not leak into orchestration, planning, execution, or storage layers
- Command text such as `/start` or `/profile` should be forwarded as normalized input; command behavior belongs to the orchestrator
- Inline buttons should be preferred for confirmation actions
- The gateway may know how to render buttons, but it must not decide what button actions mean
- Long messages should be split at the gateway boundary because message size limits are platform-specific
- Any non-Telegram adapter added later should reuse the same internal chat contracts

## Acceptance Criteria

- Telegram text messages reach the orchestrator as normalized chat messages
- Telegram button callbacks reach the orchestrator as normalized chat actions
- The gateway can render plain text responses
- The gateway can render button responses
- Oversized Telegram messages are split before delivery
- Gateway code contains no investment-specific reasoning
- Gateway code does not call Hermes directly
- Adding another chat platform does not require changing orchestrator input contracts

