# Ted

Ted is a Telegram-based personal assistant focused first on investment research.

The project is currently in specification/design stage. The Python package is a lightweight skeleton for future implementation.

## Source Of Truth

- `docs/personal-assistant-mvp-technical-spec.md` - architecture and implementation direction
- `docs/personal-assistant-mvp-requirements-v2.md` - product requirements and scope
- `docs/tasks/` - component-level task specs

## Current Principles

- Chat apps are thin gateways
- The application owns product state and policy
- Hermes owns agent reasoning through an adapter boundary
- Skills own domain-specific behavior
- Durable memory must be explicit only
- Portfolio context requires task-specific user confirmation
- Keep the first implementation simple and in-process unless real needs force more infrastructure

## Project Layout

- `docs/` - product, architecture, and task specs
- `assets/` - architecture diagrams
- `src/personal_assistant_mvp/` - Python package skeleton
- `tests/` - starter tests
- `pyproject.toml` - Python project metadata

