"""Artifact generation utilities."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from skills.mcp_provider.provider_api import Candidate, ToolConfig


@dataclass(slots=True)
class ArtifactPlan:
    """Represents a set of filesystem changes required to attach an MCP."""

    manifest_path: Path
    env_file_path: Path | None
    additional_files: Sequence[Path]


def generate_tool_artifacts(
    *,
    skill_path: Path,
    candidate: Candidate,
    mode: str,
    intents: Iterable[str] | None = None,
) -> ToolConfig:
    """Generate tool artifacts for a skill.

    The scaffolding implementation does not perform filesystem operations yet;
    it simply prepares deterministic paths relative to the provided
    ``skill_path``. This keeps downstream orchestration code stable while the
    full implementation is under development.
    """

    tools_dir = skill_path / "tools"
    tool_filename = f"mcp_{candidate.id}.json"
    manifest_path = tools_dir / tool_filename
    env_file_path = skill_path / ".env.mcp"

    return ToolConfig(
        tool_name=candidate.id,
        skill_path=skill_path,
        manifest_path=manifest_path,
        env_file_path=env_file_path,
        extra_files=(tools_dir,),
    )
