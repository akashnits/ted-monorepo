# 02. Request Orchestrator

## Purpose

The Request Orchestrator coordinates product workflow after the Chat Gateway normalizes user input.

It handles commands, user/session state, confirmations, planner handoff, executor handoff, validation, artifact persistence, and chat-ready responses. It should remain deterministic product code and should not contain investment research logic.

```text
Chat Gateway
-> Request Orchestrator
-> Task Planner
-> Agent Executor
-> Hermes Runtime Adapter
-> Skill
-> Validator
-> Artifact Store
```

## Design Principle

Borrow the gateway/executor boundary from Doghouse, but keep this app simple.

The first implementation should run in one Python service. The executor can be a local Python class. Do not add distributed queues, global concurrency controls, multi-tenant routing, S3 execution indexes, or separate worker infrastructure until the app actually needs them.

## Responsibilities

- Receive `ChatMessage` and `ChatAction` from the Chat Gateway
- Resolve or create the internal user
- Route commands
- Load and update session state
- Detect and handle pending confirmations
- Call the Task Planner for natural language requests
- Enforce product policy before execution
- Ask for missing user decisions when needed
- Call the Agent Executor when a task is ready
- Pass executor output through validation
- Save completed research artifacts
- Return `ChatResponse` objects to the Chat Gateway

## Non-Responsibilities

- Telegram-specific rendering
- Investment research logic
- Skill selection logic
- Direct Hermes calls
- Research tool calls
- Inferred durable memory
- Queueing infrastructure
- Multi-user concurrency control
- Scheduled automation

## Core Interface

```python
class RequestOrchestrator:
    async def handle_message(self, message: ChatMessage) -> ChatResponse:
        ...

    async def handle_action(self, action: ChatAction) -> ChatResponse:
        ...
```

The Chat Gateway should only depend on this interface. Platform details should not leak past the chat data contracts.

## Dependencies

The orchestrator depends on interfaces rather than concrete implementations:

- `UserService`
- `ContextService`
- `SessionManager`
- `TaskPlanner`
- `AgentExecutor`
- `OutputValidator`
- `ArtifactStore`

These dependencies can start as local classes backed by the application database.

## Command Handling

The orchestrator owns command behavior.

`/start`

- Resolve or create the user
- Return a short introduction
- Do not call the planner or executor

`/profile`

- Load explicit profile fields
- Show saved fields and missing required fields
- Do not infer missing values from chat history

`/portfolio`

- Load saved portfolio summary
- Show whether portfolio context is configured
- Do not start research

`/start_session`

- Create a temporary session
- Clear or replace any previous active session

`/end_session`

- End the current session
- Clear temporary instructions and pending confirmation state

## Natural Language Flow

For a normal user message:

1. Resolve or create the internal user.
2. Load active session state.
3. If a confirmation is pending, decide whether the new message should be handled as a new request or rejected with a reminder.
4. Load explicit profile context.
5. Load saved portfolio metadata as candidate context only.
6. Send the request and available context summary to the Task Planner.
7. Interpret the planner result.
8. Ask for clarification, profile fields, or portfolio confirmation when required.
9. If the task is ready, build an executor request.
10. Call the Agent Executor.
11. Validate executor output.
12. Save completed research artifacts.
13. Return a chat-ready response.

## Planner Boundary

The planner decides what kind of task the user is asking for and which skill should handle it.

The orchestrator enforces product policy.

Examples:

- Planner says portfolio is recommended.
- Orchestrator requires user confirmation before including portfolio context.
- Planner says profile fields are missing.
- Orchestrator decides whether to ask or proceed with general research.
- Planner selects `investment_research`.
- Orchestrator calls the executor through the application boundary.

The planner must not produce final investment research. The orchestrator must reject planner output that tries to behave like a final answer.

## Pending Confirmation Flow

When portfolio context may be useful, the orchestrator stores pending state and returns a response with buttons:

```text
Use saved portfolio context?

[Use portfolio] [Continue without] [Cancel]
```

Pending state:

```python
@dataclass(frozen=True)
class PendingPortfolioConfirmation:
    task_id: str
    user_id: str
    original_text: str
    planned_skill_id: str
    planned_task_type: str
    expires_at: datetime
```

Action handling:

- `portfolio.confirm`: resume the task with portfolio context
- `portfolio.skip`: resume the task without portfolio context
- `task.cancel`: clear pending state and return a cancellation response

The orchestrator must never include portfolio context without an explicit confirmation for that task.

## Executor Request

When the task is ready, the orchestrator builds an executor request:

```python
@dataclass(frozen=True)
class AgentExecutionRequest:
    user_id: str
    skill_id: str
    user_request: str
    profile: UserProfile | None
    portfolio: Portfolio | None
    session_instructions: str | None
    constraints: AgentConstraints
```

The executor request should contain only context that passed product policy.

## Executor Result Handling

The executor returns structured output:

```python
@dataclass(frozen=True)
class AgentExecutionResult:
    status: Literal["completed", "needs_clarification", "out_of_scope", "failed"]
    brief: str | None
    artifact_payload: dict | None
    sources: list[SourceReference]
    diagnostics: dict | None = None
```

Handling rules:

- `completed`: validate, persist artifact, return brief
- `needs_clarification`: return clarification prompt
- `out_of_scope`: return out-of-scope response
- `failed`: return graceful failure response

Invalid executor output must not be saved as a completed artifact.

## Error Behavior

Errors should produce clear user-facing responses without exposing stack traces.

If the planner fails:

```text
I could not understand that request. Please try rephrasing it.
```

If execution fails:

```text
I could not complete that research request. Please try again.
```

Operational failures should be logged for debugging, but they should not create misleading completed artifacts.

## Implementation Tasks

1. Add orchestration package:
   - `src/personal_assistant_mvp/orchestration/`
2. Add orchestrator interface:
   - `handle_message`
   - `handle_action`
3. Add command routing:
   - `/start`
   - `/profile`
   - `/portfolio`
   - `/start_session`
   - `/end_session`
4. Add pending confirmation handling:
   - create pending state
   - resume with portfolio
   - resume without portfolio
   - cancel pending task
5. Add planner handoff:
   - pass natural language request to planner
   - interpret planner statuses
   - reject planner output that looks like final research
6. Add executor handoff:
   - build `AgentExecutionRequest`
   - call local `AgentExecutor`
   - handle structured result
7. Add validation and persistence:
   - validate completed outputs
   - save artifacts only after validation
8. Add tests:
   - command routing does not call planner or executor
   - natural language requests call planner
   - portfolio is never included without confirmation
   - confirm resumes the stored task with portfolio context
   - skip resumes the stored task without portfolio context
   - cancel clears pending state
   - completed executor output is validated and saved
   - failed executor output is not saved as completed artifact

## Acceptance Criteria

- Chat Gateway uses one orchestrator interface for messages
- Chat Gateway uses one orchestrator interface for actions
- Commands are handled deterministically without planner or executor calls
- Natural language requests go through the Task Planner
- Skill selection is delegated to the Task Planner
- Agent execution is delegated to the Agent Executor
- Profile context can be included automatically when available
- Portfolio context is never included without task-specific confirmation
- Pending confirmation state can be resumed or cancelled
- Completed results are validated before persistence
- Failed or invalid results are not saved as completed artifacts
- Orchestrator contains no investment research logic
- Orchestrator contains no Telegram-specific rendering logic
- First implementation does not require a distributed queue or separate worker service

