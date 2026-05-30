"""Shared application model base types."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class AppModel(BaseModel):
    """Base Pydantic model for application contracts."""

    model_config = ConfigDict(extra="forbid", frozen=True)

