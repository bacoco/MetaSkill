#!/usr/bin/env python3
"""
Data models for NEXUS pattern detection
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SessionData:
    """Represents a single SOUL session"""
    timestamp: str
    agent: str
    repository: str
    total_files: int
    modified_files: int
    added_files: int
    deleted_files: int
    untracked_files: int
    file_categories: Dict[str, List[str]]
    recent_commits: List[Dict[str, str]]
    problems_solved: List[str]
    git_status: str
    branch: str
    changed_files: List[str]


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