"""Docker runtime policies."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Sequence


@dataclass(frozen=True, slots=True)
class RuntimePolicy:
    """Describes a Docker runtime policy."""

    name: str
    args: Sequence[str]


_DEFAULT_POLICIES: Dict[str, RuntimePolicy] = {
    "strict": RuntimePolicy(
        name="strict",
        args=(
            "--read-only",
            "--cap-drop=ALL",
            "--security-opt",
            "no-new-privileges",
            "--pids-limit",
            "128",
            "--memory",
            "512m",
            "--cpus",
            "1",
            "--tmpfs",
            "/tmp:rw,noexec",
            "--network",
            "none",
        ),
    ),
    "default": RuntimePolicy(name="default", args=tuple()),
    "netneeded": RuntimePolicy(
        name="netneeded",
        args=("--network", "mcp-provider-net"),
    ),
}


def get_policy(name: str = "strict") -> RuntimePolicy:
    """Return a runtime policy by name."""

    try:
        return _DEFAULT_POLICIES[name]
    except KeyError as exc:  # pragma: no cover - defensive branch.
        raise KeyError(f"Unknown runtime policy: {name}") from exc
