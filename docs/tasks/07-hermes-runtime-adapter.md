# 07. Hermes Runtime Adapter

## Purpose

The Hermes Runtime Adapter hides Hermes-specific API details behind a stable application interface.

It lets the Agent Executor run Hermes tasks without knowing Hermes transport, request format, authentication, model configuration, or response quirks.

```text
Agent Executor
-> Hermes Runtime Adapter
-> Hermes
```

## Diagram

```mermaid
flowchart TD
    Executor[Agent Executor] --> Adapter[Hermes Runtime Adapter]
    Adapter --> Request[Build Hermes Request]
    Request --> Hermes[Hermes]
    Hermes --> Raw[Raw Hermes Response]
    Raw --> Normalize[Normalize Result]
    Normalize --> Executor
```

## Responsibilities

- Convert app execution requests into Hermes-compatible requests
- Attach selected skill configuration
- Attach authorized context
- Apply model and runtime configuration
- Call Hermes
- Normalize Hermes responses into app-level execution results
- Normalize Hermes errors into app-level failure statuses
- Preserve diagnostics useful for debugging

## Non-Responsibilities

- Task planning
- Skill selection
- User confirmation
- Context authorization
- Output validation
- Artifact persistence
- Chat rendering
- Durable memory writes

## Interfaces

Input from the Agent Executor:

- app-level execution request
- selected skill
- authorized context
- task constraints
- runtime configuration

Output to the Agent Executor:

- normalized execution status
- normalized answer payload
- normalized artifact payload when available
- normalized source metadata when available
- diagnostics or structured failure details

## Key Policies

- Hermes-specific request and response formats must not leak outside this adapter
- Model and runtime switching should be configuration-driven where possible
- Malformed Hermes responses should fail closed as structured runtime failures
- Diagnostics should be preserved for logs and debugging
- User-facing error messages should be produced upstream, not by this adapter
- The first version can support one Hermes backend and one model path

## Acceptance Criteria

- Agent Executor can call one stable runtime adapter interface
- Adapter can send a valid task to Hermes
- Adapter returns normalized execution results
- Adapter converts Hermes errors into structured failures
- Adapter hides Hermes transport and payload details from the rest of the app
- No orchestrator, planner, context service, or chat gateway calls Hermes directly

