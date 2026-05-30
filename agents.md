# Agent Instructions

This repository is documentation for a Telegram-based personal assistant. Treat the specification files as the source of truth.

## Read First

- `docs/personal-assistant-mvp-requirements-v2.md`
- `docs/personal-assistant-mvp-technical-spec.md`

## Operating Rules

- Do not invent product behavior that conflicts with the requirements
- Keep the scope narrow and avoid broadening it without explicit instruction
- Preserve the explicit-memory model; do not infer durable preferences from conversation
- Treat profile data as durable explicit context
- Treat portfolio data as sensitive context that requires user confirmation before use
- Keep the application layer thin and avoid hardcoding investment logic outside the skill layer
- Prefer repository language and terminology from the specs when writing new docs or implementation notes
- Treat `docs/personal-assistant-mvp-technical-spec.md` as the implementation source of truth

## Repo Conventions

- Use ASCII unless a file already requires something else
- Keep edits focused and avoid unrelated refactors
- Update documentation when implementation choices materially change the design
- If new code is added later, keep the product boundary, agent boundary, and skill boundary clear

## Helpful References

- Architecture overview: `assets/architecture-overview.svg`
- Research flow: `assets/research-flow.svg`
