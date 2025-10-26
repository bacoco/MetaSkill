"""Candidate scoring utilities."""
from __future__ import annotations

from typing import Iterable, List

from skills.mcp_provider.provider_api import Candidate, CandidateScore


DEFAULT_THRESHOLD = 0.6


def score_candidates(
    candidates: Iterable[Candidate], intents: Iterable[str] | None = None
) -> List[CandidateScore]:
    """Score candidates based on the requested intents.

    The MVP scaffolding returns deterministic zero scores while preserving the
    ordering of the input candidates. This keeps the API functional for
    downstream integration without enforcing a specific scoring policy yet.
    """

    scored: List[CandidateScore] = []
    for candidate in candidates:
        scored.append(
            CandidateScore(
                candidate=candidate,
                score=0.0,
                reasons=("scoring not implemented",),
            )
        )
    return scored
