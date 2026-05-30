# 02. Request Orchestrator

## Purpose

The Request Orchestrator coordinates product workflow after the Chat Gateway normalizes user input.

It owns command handling, user/session state flow, confirmation flow, planner handoff, executor handoff, validation handoff, artifact persistence, and chat-ready responses. It should remain deterministic product code and should not contain investment research logic.

```text
Chat Gateway
-> Request Orchestrator
-> Task Planner
-> Agent Executor
-> Hermes Runtime Adapter
```

## Design Principle

Borrow the gateway/executor boundary from Doghouse, but keep this app simple.

The first implementation should run in one Python service. The executor can be a local Python class. Do not add distributed queues, global concurrency controls, multi-tenant routing, S3 execution indexes, or separate worker infrastructure until the app actually needs them.

## Responsibilities

- Receive normalized chat messages and chat actions
- Resolve or create the internal user
- Route general commands
- Load and update session state
- Detect and handle pending confirmations
- Call the Task Planner for natural language requests
- Enforce product policy before execution
- Ask for missing user decisions when needed
- Call the Agent Executor when a task is ready
- Send completed executor output through validation
- Save completed research artifacts after validation
- Return chat-ready responses to the Chat Gateway

## Non-Responsibilities

- Telegram-specific rendering
- Task interpretation
- Skill selection
- Investment research logic
- Direct Hermes calls
- Research tool calls
- Inferred durable memory
- Queueing infrastructure
- Multi-user concurrency control
- Scheduled automation

## Interfaces

The Chat Gateway calls:

- `handle_message(chat_message) -> chat_response`
- `handle_action(chat_action) -> chat_response`

The orchestrator depends on these component boundaries:

- `UserService` for user identity
- `ContextService` for explicit profile and portfolio context
- `SessionManager` for temporary session and pending-state data
- `TaskPlanner` for task interpretation and skill selection
- `AgentExecutor` for running ready tasks
- `OutputValidator` for result validation
- `ArtifactStore` for completed research persistence

The orchestrator returns only chat-ready responses. It should not return raw planner, executor, or validator objects to the Chat Gateway.

## Key Policies

- Commands are handled by the orchestrator without planner or executor calls
- Natural language requests go through the Task Planner
- The planner recommends task type, skill, missing context, and portfolio usefulness
- The orchestrator enforces product policy before execution
- Profile context may be included automatically when it exists because it is explicit durable context
- Portfolio context must never be included without task-specific user confirmation
- Planner output must not be treated as final research
- Executor output must be validated before it is saved as a completed artifact
- Failed or invalid executor output must not create a completed artifact
- The first implementation should not require a distributed queue or separate worker service

## Pending Confirmation Policy

When portfolio context may be useful, the orchestrator should store pending task state and return a confirmation response with actions equivalent to:

- use portfolio
- continue without portfolio
- cancel

On confirmation, the orchestrator resumes the stored task with portfolio context. On skip, it resumes without portfolio context. On cancel, it clears pending state and does not execute the task.

## Acceptance Criteria

- Chat Gateway uses one orchestrator interface for messages
- Chat Gateway uses one orchestrator interface for actions
- Commands are handled deterministically without planner or executor calls
- Natural language requests are delegated to the Task Planner
- Skill selection is not implemented inside the orchestrator
- Agent execution is delegated to the Agent Executor
- Profile context can be included automatically when available
- Portfolio context is never included without task-specific confirmation
- Pending confirmation state can be resumed or cancelled
- Completed results are validated before persistence
- Failed or invalid results are not saved as completed artifacts
- Orchestrator code contains no investment research logic
- Orchestrator code contains no Telegram-specific rendering logic

