#!/usr/bin/env python3
"""
Data models for Synapse pattern detection
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SessionData:
    """Represents a single Cortex session"""

    timestamp: str = ""
    agent: str = ""
    repository: str = ""
    total_files: int = 0
    modified_files: int = 0
    added_files: int = 0
    deleted_files: int = 0
    untracked_files: int = 0
    file_categories: Dict[str, List[str]] = field(default_factory=dict)
    recent_commits: List[Dict[str, str]] = field(default_factory=list)
    problems_solved: List[str] = field(default_factory=list)
    git_status: str = ""
    branch: str = "main"
    changed_files: List[str] = field(default_factory=list)


@dataclass
class PatternInfo:
    """Information about a detected pattern"""

    pattern_type: str
    description: str
    frequency: int
    impact_score: float
    trend_score: float
    urgency_score: float
    examples: List[str]
    metadata: Dict = field(default_factory=dict)

    def combined_priority_score(self) -> float:
        """Calculate a simple combined score used for ranking patterns."""

        base_scores = [
            max(self.frequency, 0),
            max(self.impact_score, 0.0),
            max(self.trend_score, 0.0),
            max(self.urgency_score, 0.0),
        ]

        # Normalize frequency to avoid over-emphasizing huge counts.
        normalized_frequency = min(base_scores[0] / 10.0, 1.0)
        weighted_scores = [
            normalized_frequency,
            base_scores[1],
            base_scores[2],
            base_scores[3],
        ]

        return sum(weighted_scores) / len(weighted_scores)


@dataclass
class SkillRecommendation:
    """Recommendation for a new skill"""

    skill_name: str
    skill_type: str
    description: str
    reason: str
    priority_score: float
    frequency_score: float
    impact_score: float
    trend_score: float
    urgency_score: float
    roi_score: float
    supporting_patterns: List[str]
    example_use_cases: List[str]


@dataclass
class TrendAnalysis:
    """Trend analysis over time"""
    increasing_patterns: List[str]
    decreasing_patterns: List[str]
    stable_patterns: List[str]
    emerging_patterns: List[str]
    session_frequency: float
    avg_files_per_session: float
    most_active_periods: List[str]