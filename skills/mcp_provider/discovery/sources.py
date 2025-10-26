"""Source resolution helpers for MCP catalogue discovery."""
from __future__ import annotations

from typing import Iterable, List

DEFAULT_SOURCES: List[str] = []


class SourceNotAllowedError(RuntimeError):
    """Raised when a requested source is not present on the allowlist."""


def resolve_sources(requested: Iterable[str] | None = None) -> List[str]:
    """Validate and resolve catalogue sources.

    This scaffolding implementation keeps track of the requested sources and
    ensures they adhere to a basic allowlist requirement. The concrete
    allowlist is intentionally empty and must be populated during the
    production implementation.
    """

    if requested is None:
        return list(DEFAULT_SOURCES)

    resolved: List[str] = []
    for url in requested:
        if url not in DEFAULT_SOURCES:
            raise SourceNotAllowedError(f"Source '{url}' is not allowlisted.")
        resolved.append(url)
    return resolved
