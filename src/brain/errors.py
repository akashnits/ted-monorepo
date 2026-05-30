"""Typed application errors."""

from __future__ import annotations


class TedError(Exception):
    """Base class for expected application errors."""


class ConfigError(TedError):
    """Raised when required runtime configuration is missing or invalid."""


class DatabaseError(TedError):
    """Raised when database setup or access fails."""


class PlannerError(TedError):
    """Raised when task planning fails."""


class RuntimeExecutionError(TedError):
    """Raised when agent runtime execution fails."""


class ValidationError(TedError):
    """Raised when an agent result fails application validation."""


class PersistenceError(TedError):
    """Raised when durable persistence fails."""

