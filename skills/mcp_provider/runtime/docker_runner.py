"""Helpers for building Docker commands for MCP runtimes."""
from __future__ import annotations

from typing import Iterable, List, Sequence

from .policies import RuntimePolicy, get_policy


def build_docker_command(
    *, image: str, policy: str = "strict", extra_args: Iterable[str] | None = None
) -> Sequence[str]:
    """Construct a docker CLI command according to the runtime policy."""

    if not image:
        raise ValueError("image must be provided")

    runtime_policy: RuntimePolicy = get_policy(policy)
    command: List[str] = ["docker", "run", "--rm"]
    command.extend(runtime_policy.args)

    if extra_args:
        command.extend(extra_args)

    command.append(image)
    return tuple(command)
