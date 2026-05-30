# Agent Instructions

Treat the docs as the source of truth for this repository.

## Read First

- `docs/personal-assistant-mvp-technical-spec.md`
- `docs/personal-assistant-mvp-requirements-v2.md`
- `docs/tasks/`

## Rules

- Keep scope narrow and avoid adding infrastructure before it is needed
- Preserve explicit memory only; do not infer durable preferences from chat
- Profile context is explicit durable context
- Portfolio context requires task-specific user confirmation
- Keep chat, orchestration, planning, execution, skills, tools, validation, and persistence as separate boundaries
- Do not hardcode investment logic outside the Investment Research Skill
- Keep task specs short; detailed implementation plans can come later

