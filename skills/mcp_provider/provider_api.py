"""Public API for the MCP Provider skill.

This module exposes typed helper functions that orchestrate discovery,
validation, attachment, and runtime operations for Model Context Protocol
(MCP) tools. The implementation is intentionally lightweight for the MVP:
only interface scaffolding and structured return types are provided. The
business logic will be implemented in subsequent iterations following the
product requirements document.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Mapping, Optional, Sequence


@dataclass(slots=True)
class Candidate:
    """Minimal representation of a discovered MCP entry."""

    id: str
    name: str
    capabilities: Sequence[str]
    transport: str
    docker_image: Optional[str] = None
    docs_url: Optional[str] = None
    source: Optional[str] = None
    metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class CandidateScore:
    """Associates a :class:`Candidate` with a floating score."""

    candidate: Candidate
    score: float
    reasons: Sequence[str] = field(default_factory=tuple)


@dataclass(slots=True)
class ToolConfig:
    """Description of the artifacts generated for a skill."""

    tool_name: str
    skill_path: Path
    manifest_path: Path
    env_file_path: Optional[Path] = None
    extra_files: Sequence[Path] = field(default_factory=tuple)


@dataclass(slots=True)
class RunDescriptor:
    """Runtime configuration for launching an MCP in a sandbox."""

    command: Sequence[str]
    environment_files: Sequence[Path] = field(default_factory=tuple)
    timeout_seconds: Optional[int] = None
    policy: str = "strict"


@dataclass(slots=True)
class HealthReport:
    """Outcome of a health check invocation."""

    mcp_id: str
    ok: bool
    latency_ms: Optional[int] = None
    warnings: Sequence[str] = field(default_factory=tuple)
    log_excerpt: Optional[str] = None


class NotConfiguredError(RuntimeError):
    """Raised when the MCP Provider is invoked without proper configuration."""


def discover_mcp(
    *, intents: Optional[Iterable[str]] = None, sources: Optional[Iterable[str]] = None
) -> List[Candidate]:
    """Discover MCP candidates.

    Parameters
    ----------
    intents:
        Optional iterable of intent strings describing the desired capabilities.
    sources:
        Optional iterable of MCP catalogue URLs. When omitted, an allowlisted set
        defined in :mod:`skills.mcp_provider.discovery.sources` will be used.

    Returns
    -------
    list of :class:`Candidate`
        The discovered candidates. The list is empty when discovery is not yet
        implemented or when no sources are available.
    """

    raise NotImplementedError("MCP discovery is not implemented yet.")


def select_and_attach_mcp(
    *,
    skill_path: Path,
    candidates: Sequence[Candidate],
    mode: str = "default",
    intents: Optional[Iterable[str]] = None,
) -> ToolConfig:
    """Select the best MCP candidate and attach it to a skill.

    This scaffolding function validates the input parameters and raises a
    :class:`NotImplementedError`. Future implementations will orchestrate the
    scoring, validation, artifact generation, and SKILL.md patching steps.
    """

    if not skill_path:
        raise ValueError("skill_path must be provided")

    if not candidates:
        raise ValueError("candidates must not be empty")

    raise NotImplementedError("MCP attachment is not implemented yet.")


def ensure_runtime(*, mcp_id: str, policy: str = "strict") -> RunDescriptor:
    """Prepare a sandboxed runtime definition for the given MCP."""

    if not mcp_id:
        raise ValueError("mcp_id must be provided")

    raise NotImplementedError("Runtime preparation is not implemented yet.")


def test_mcp(tool_config: ToolConfig) -> HealthReport:
    """Perform a basic health check using the provided tool configuration."""

    if not tool_config.tool_name:
        raise ValueError("tool_config.tool_name must be provided")

    raise NotImplementedError("MCP health check is not implemented yet.")


# Ensure pytest does not mistake the public API function for a test case.
test_mcp.__test__ = False  # type: ignore[attr-defined]
