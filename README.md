# Personal Assistant - Ted

This repository captures the product and architecture documentation for a Telegram-based personal assistant.

- Telegram is the only user interface
- The assistant supports one explicit profile per user
- The assistant supports one saved portfolio per user
- Portfolio context must be confirmed before use
- The first skill is investment research
- Completed research is saved as artifacts for future retrieval work

## What Is In This Repo

- `docs/personal-assistant-mvp-requirements-v2.md` - product requirements and scope
- `docs/personal-assistant-mvp-technical-spec.md` - architecture and implementation direction
- `assets/architecture-overview.svg` - architecture diagram
- `assets/research-flow.svg` - research flow diagram
- `src/personal_assistant_mvp/` - Python package skeleton
- `tests/` - starter test suite
- `pyproject.toml` - Python project metadata and build config

## Core Design Principles

- The application owns user identity, Telegram integration, profile storage, portfolio storage, session state, and artifact persistence
- The agent owns planning, reasoning, research synthesis, and response generation
- Skills own task-specific instructions, quality standards, and safety boundaries
- Durable memory must be explicit only; inferred preferences are out of scope
- Profile context can be used automatically when present
- Portfolio context must be shown to the user and confirmed each time before use

## Current Status

This repo currently contains specifications and design assets rather than executable application code.

The technical source of truth for implementation is `docs/personal-assistant-mvp-technical-spec.md`.

## Project Layout

The Python package follows a standard `src/` layout:

- `src/personal_assistant_mvp/` for importable application code
- `tests/` for automated checks
- `pyproject.toml` for packaging, CLI entry points, and test configuration
- `docs/` for product and architecture documentation
