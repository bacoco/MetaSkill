"""Candidate validation utilities."""
from __future__ import annotations

from typing import Iterable

from skills.mcp_provider.provider_api import Candidate


class ValidationError(RuntimeError):
    """Raised when a candidate does not satisfy minimal requirements."""


REQUIRED_FIELDS: Iterable[str] = ("id", "name", "capabilities", "transport")


def validate_candidate(candidate: Candidate) -> None:
    """Validate a candidate entry.

    The scaffolding implementation ensures obvious attributes are populated.
    Additional validation logic (allowlists, signatures, etc.) must be added in
    future iterations.
    """

    for field_name in REQUIRED_FIELDS:
        value = getattr(candidate, field_name, None)
        if value in (None, "", ()):  # empty tuple/list allowed? treat as invalid.
            raise ValidationError(f"Candidate missing required field: {field_name}")
