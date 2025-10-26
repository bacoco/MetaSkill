"""Documentation patch helpers for attached MCP tools."""
from __future__ import annotations

from pathlib import Path


def update_skill_documentation(*, skill_path: Path, tool_name: str, mode: str) -> None:
    """Update the SKILL.md file of the target skill.

    The scaffolding implementation does not modify the filesystem yet. The
    function exists so that higher-level orchestration code can depend on it
    while the detailed implementation is under active development.
    """

    if not skill_path:
        raise ValueError("skill_path must be provided")
    if not tool_name:
        raise ValueError("tool_name must be provided")
    if not mode:
        raise ValueError("mode must be provided")

    raise NotImplementedError("Skill documentation patching is not implemented yet.")
