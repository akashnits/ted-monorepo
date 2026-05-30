# Implementation Approach

Build Ted in thin vertical slices. Do not implement every component in isolation before seeing the full request flow work.

The first target is a simple end-to-end path:

```text
Telegram message
-> Chat Gateway
-> Request Orchestrator
-> Task Planner
-> Agent Executor
-> ChatResponse
-> Telegram reply
```

Use fake planner/executor implementations first, then replace them with real components one by one.

## Build Order

### 1. Foundation

Implement:

- `13-database-schema.md`
- `14-configuration-and-secrets.md`
- `15-observability-and-errors.md`

How:

- Add typed config with Pydantic Settings.
- Add Postgres connection and Alembic migrations.
- Add basic logging and typed application errors.
- Define shared Pydantic models used across components.

### 2. Chat And Orchestration Skeleton

Implement:

- `01-chat-gateway.md`
- `02-request-orchestrator.md`

How:

- Use `python-telegram-bot`.
- Put Telegram code in `src/chat/telegram/`.
- Put shared chat contracts in `src/chat/types.py`.
- Put orchestrator code in `src/orchestration/`.
- Wire Telegram messages into the orchestrator.
- Return simple `ChatResponse` objects.
- Use fake planner and fake executor at this stage.

### 3. User, Context, And Sessions

Implement:

- `04-context-service.md`
- `05-session-manager.md`

How:

- Store users, profiles, portfolios, and sessions in Postgres.
- Keep profile and portfolio reads behind the Context Service.
- Keep sessions temporary and separate from durable memory.
- Add pending confirmation support for portfolio usage.
- Keep portfolio data manually managed at first.

### 4. Planning

Implement:

- `03-task-planner.md`
- `08-skill-registry.md`

How:

- Start with a static Skill Registry.
- Register only `investment_research`.
- Give the planner planner-safe skill cards.
- Use an LLM with structured JSON output validated by Pydantic.
- Let the planner call only Context Service summary APIs.
- Planner recommends useful context; orchestrator authorizes context use.

### 5. Skill And Research Tools

Implement:

- `09-investment-research-skill.md`
- `10-research-tool-gateway.md`

How:

- Create `skills/investment_research/SKILL.md`.
- Write the skill as a research playbook.
- Start with a small tool set: security resolution, quote, profile, financials, filings, news, and peer snapshot.
- Keep provider adapters behind the Research Tool Gateway.
- Return normalized evidence with source metadata.

### 6. Agent Execution

Implement:

- `06-agent-executor.md`
- `07-hermes-runtime-adapter.md`

How:

- Keep the executor in-process as a Python class.
- Executor receives only ready tasks from the orchestrator.
- Executor resolves skill config and calls the Hermes Runtime Adapter.
- Hermes Runtime Adapter exposes only allowed research tools.
- Use direct tool-calling research flow.
- Normalize Hermes output into app-level execution results.

### 7. Validation And Persistence

Implement:

- `11-output-validator.md`
- `12-artifact-store.md`

How:

- Validate Hermes output with Pydantic schemas.
- Enforce recommendation labels, confidence labels, source metadata, and artifact payload.
- Save only validated completed outputs.
- Store artifacts and sources in Postgres.

## First Real Flow

Target this scenario first:

```text
User: Analyze TCS
```

Expected path:

```text
Telegram
-> Chat Gateway
-> Orchestrator
-> Planner selects investment_research
-> Context Service loads profile summary
-> Executor calls Hermes
-> Hermes uses research tools
-> Output Validator accepts result
-> Artifact Store saves result
-> Telegram receives compact research brief
```

After this works, add portfolio confirmation:

```text
User: Should I buy TCS?
-> planner recommends portfolio context
-> orchestrator asks for confirmation
-> user confirms
-> executor receives portfolio context
```

## Guiding Rules

- Keep the first implementation in one Python service.
- Prefer in-process classes before adding workers or queues.
- Keep database access behind services.
- Keep Hermes behind the runtime adapter.
- Keep investment logic inside the skill.
- Use fake implementations to prove flow before adding external dependencies.
- Tighten quality through skill instructions, tool descriptions, validator rules, and reviewed outputs.

