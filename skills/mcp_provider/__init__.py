"""Meta-skill MCP Provider package."""

from .provider_api import (
    Candidate,
    CandidateScore,
    HealthReport,
    NotConfiguredError,
    RunDescriptor,
    ToolConfig,
    discover_mcp,
    ensure_runtime,
    select_and_attach_mcp,
    test_mcp,
)

__all__ = [
    "Candidate",
    "CandidateScore",
    "HealthReport",
    "NotConfiguredError",
    "RunDescriptor",
    "ToolConfig",
    "discover_mcp",
    "ensure_runtime",
    "select_and_attach_mcp",
    "test_mcp",
]
