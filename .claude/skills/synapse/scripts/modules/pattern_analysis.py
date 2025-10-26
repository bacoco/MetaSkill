#!/usr/bin/env python3
"""
Pattern analysis module for Synapse
"""

import re
import logging
from datetime import datetime
from collections import Counter, defaultdict
from typing import Dict, List
from pathlib import Path
import sys

MODULE_DIR = Path(__file__).resolve().parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from data_models import SessionData, PatternInfo  # type: ignore
from config_manager import ConfigManager  # type: ignore


class PatternDetector:
    """Detects sophisticated patterns in Cortex data"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def analyze_all_patterns(self, cortex_data: Dict) -> Dict[str, PatternInfo]:
        """Analyze all patterns in Cortex data"""
        patterns = {}

        sessions = cortex_data.get("sessions", [])
        commits = cortex_data.get("git_commits", [])

        if not sessions:
            self.logger.warning("No sessions to analyze")
            return patterns

        # Temporal patterns
        patterns.update(self.analyze_temporal_patterns(sessions))

        # File correlation patterns
        patterns.update(self.analyze_file_correlations(sessions))

        # Problem recurrence patterns
        patterns.update(self.analyze_problem_recurrence(sessions))

        # Commit patterns
        patterns.update(self.analyze_commit_patterns(commits))

        # Agent collaboration patterns
        patterns.update(self.analyze_agent_collaboration(sessions))

        # Skill gap patterns
        patterns.update(self.analyze_skill_gaps(sessions, commits))

        self.logger.info(f"Detected {len(patterns)} patterns")

        return patterns

    def analyze_temporal_patterns(self, sessions: List[SessionData]) -> Dict[str, PatternInfo]:
        """Analyze temporal patterns in sessions"""
        patterns = {}

        if not sessions:
            return patterns

        # Extract timestamps
        timestamps = []
        for session in sessions:
            # Validate input type defensively
            if not isinstance(session, SessionData):
                continue
            try:
                # Parse timestamp format: 2025-10-25-12:26
                dt = datetime.strptime(session.timestamp, "%Y-%m-%d-%H:%M")
                timestamps.append(dt)
            except Exception:
                continue

        if len(timestamps) < 2:
            return patterns

        # Analyze session frequency
        time_diffs = []
        for i in range(1, len(timestamps)):
            diff = (timestamps[i] - timestamps[i-1]).total_seconds() / 3600  # hours
            time_diffs.append(diff)

        avg_session_interval = sum(time_diffs) / len(time_diffs) if time_diffs else 0

        # Detect high-frequency periods
        if avg_session_interval < 1:  # Less than 1 hour between sessions
            patterns["high_frequency_sessions"] = PatternInfo(
                pattern_type="temporal",
                description="High frequency of sessions detected",
                frequency=len(sessions),
                impact_score=0.7,
                trend_score=0.6,
                urgency_score=0.5,
                examples=[f"Average {avg_session_interval:.1f} hours between sessions"],
                metadata={"avg_interval_hours": avg_session_interval}
            )

        # Analyze day of week patterns
        day_counts = Counter([ts.strftime("%A") for ts in timestamps])
        most_common_day, day_count = day_counts.most_common(1)[0]

        if day_count >= 3:
            patterns["day_of_week_pattern"] = PatternInfo(
                pattern_type="temporal",
                description=f"Most sessions on {most_common_day}",
                frequency=day_count,
                impact_score=0.4,
                trend_score=0.3,
                urgency_score=0.2,
                examples=[f"{day_count} sessions on {most_common_day}"],
                metadata={"day": most_common_day, "count": day_count}
            )

        # Analyze hour of day patterns
        hour_counts = Counter([ts.hour for ts in timestamps])
        if hour_counts:
            most_common_hour, hour_count = hour_counts.most_common(1)[0]

            patterns["time_of_day_pattern"] = PatternInfo(
                pattern_type="temporal",
                description=f"Most sessions around {most_common_hour}:00",
                frequency=hour_count,
                impact_score=0.3,
                trend_score=0.2,
                urgency_score=0.1,
                examples=[f"{hour_count} sessions around {most_common_hour}:00"],
                metadata={"hour": most_common_hour, "count": hour_count}
            )

        return patterns

    def analyze_file_correlations(self, sessions: List[SessionData]) -> Dict[str, PatternInfo]:
        """Analyze which files are modified together"""
        patterns = {}

        # Track file co-occurrences
        file_pairs = Counter()
        all_files = []

        for session in sessions:
            files = session.changed_files
            all_files.extend(files)

            # Count pairs
            for i, file1 in enumerate(files):
                for file2 in files[i+1:]:
                    pair = tuple(sorted([file1, file2]))
                    file_pairs[pair] += 1

        # Find frequently co-occurring files
        threshold = self.config.get("analysis", "file_correlation_threshold", default=2)

        for (file1, file2), count in file_pairs.most_common(10):
            if count >= threshold:
                pattern_key = f"file_correlation_{len(patterns)}"
                patterns[pattern_key] = PatternInfo(
                    pattern_type="file_correlation",
                    description=f"Files often modified together: {file1} and {file2}",
                    frequency=count,
                    impact_score=0.6,
                    trend_score=0.5,
                    urgency_score=0.4,
                    examples=[f"Modified together {count} times"],
                    metadata={"file1": file1, "file2": file2}
                )

        # Analyze file type patterns
        file_extensions = Counter()
        for file in all_files:
            if '.' in file:
                ext = file.split('.')[-1]
                file_extensions[ext] += 1

        for ext, count in file_extensions.most_common(5):
            if count >= 5:
                pattern_key = f"file_type_{ext}"
                patterns[pattern_key] = PatternInfo(
                    pattern_type="file_type",
                    description=f"Frequent work with .{ext} files",
                    frequency=count,
                    impact_score=0.7,
                    trend_score=0.6,
                    urgency_score=0.5,
                    examples=[f"{count} .{ext} files modified"],
                    metadata={"extension": ext}
                )

        return patterns

    def analyze_problem_recurrence(self, sessions: List[SessionData]) -> Dict[str, PatternInfo]:
        """Analyze recurring problems"""
        patterns = {}

        # Collect all problems
        all_problems = []
        for session in sessions:
            all_problems.extend(session.problems_solved)

        if not all_problems:
            return patterns

        # Extract keywords from problems
        problem_keywords = Counter()
        for problem in all_problems:
            # Simple keyword extraction (lowercase words)
            words = re.findall(r'\b\w+\b', problem.lower())
            # Filter out common words
            meaningful_words = [w for w in words if len(w) > 3 and w not in {'with', 'from', 'that', 'this', 'have', 'been'}]
            problem_keywords.update(meaningful_words)

        # Detect recurring problem themes
        threshold = self.config.get("analysis", "problem_recurrence_threshold", default=2)

        for keyword, count in problem_keywords.most_common(10):
            if count >= threshold:
                pattern_key = f"recurring_problem_{keyword}"
                patterns[pattern_key] = PatternInfo(
                    pattern_type="problem_recurrence",
                    description=f"Recurring issue related to: {keyword}",
                    frequency=count,
                    impact_score=0.8,
                    trend_score=0.7,
                    urgency_score=0.8,
                    examples=[p for p in all_problems if keyword in p.lower()][:3],
                    metadata={"keyword": keyword}
                )

        return patterns

    def analyze_commit_patterns(self, commits: List[Dict]) -> Dict[str, PatternInfo]:
        """Analyze commit message patterns"""
        patterns = {}

        if not commits:
            return patterns

        # Analyze commit message prefixes/types
        commit_types = Counter()
        for commit in commits:
            message = commit.get("message", "")
            # Extract emoji or prefix
            emoji_match = re.match(r'^([\U0001F300-\U0001F9FF]|:\w+:)', message)
            if emoji_match:
                commit_types[emoji_match.group(1)] += 1
            else:
                # Try to extract type like "feat:", "fix:", etc.
                type_match = re.match(r'^(\w+):', message)
                if type_match:
                    commit_types[type_match.group(1)] += 1

        # Detect dominant commit types
        for commit_type, count in commit_types.most_common(5):
            if count >= 3:
                pattern_key = f"commit_type_{commit_type}"
                patterns[pattern_key] = PatternInfo(
                    pattern_type="commit_pattern",
                    description=f"Frequent commit type: {commit_type}",
                    frequency=count,
                    impact_score=0.5,
                    trend_score=0.4,
                    urgency_score=0.3,
                    examples=[c["message"] for c in commits if commit_type in c["message"]][:3],
                    metadata={"commit_type": commit_type}
                )

        # Analyze commit keywords
        all_messages = " ".join([c.get("message", "") for c in commits])
        keywords = re.findall(r'\b\w{4,}\b', all_messages.lower())
        keyword_counts = Counter(keywords)

        for keyword, count in keyword_counts.most_common(10):
            if count >= 5 and keyword not in {'with', 'from', 'that', 'this', 'have'}:
                pattern_key = f"commit_keyword_{keyword}"
                patterns[pattern_key] = PatternInfo(
                    pattern_type="commit_keyword",
                    description=f"Frequent commit keyword: {keyword}",
                    frequency=count,
                    impact_score=0.6,
                    trend_score=0.5,
                    urgency_score=0.4,
                    examples=[c["message"] for c in commits if keyword in c["message"].lower()][:3],
                    metadata={"keyword": keyword}
                )

        return patterns

    def analyze_agent_collaboration(self, sessions: List[SessionData]) -> Dict[str, PatternInfo]:
        """Analyze how agents collaborate"""
        patterns = {}

        if len(sessions) < 2:
            return patterns

        # Analyze agent transitions
        agent_transitions = []
        for i in range(1, len(sessions)):
            prev_agent = sessions[i-1].agent
            curr_agent = sessions[i].agent
            if prev_agent != curr_agent:
                agent_transitions.append((prev_agent, curr_agent))

        if agent_transitions:
            transition_counts = Counter(agent_transitions)
            most_common_transition, count = transition_counts.most_common(1)[0]

            patterns["agent_handoff_pattern"] = PatternInfo(
                pattern_type="agent_collaboration",
                description=f"Frequent handoff: {most_common_transition[0]} → {most_common_transition[1]}",
                frequency=count,
                impact_score=0.5,
                trend_score=0.4,
                urgency_score=0.3,
                examples=[f"Handoff occurred {count} times"],
                metadata={"from": most_common_transition[0], "to": most_common_transition[1]}
            )

        # Analyze agent specializations
        agent_file_types = defaultdict(Counter)
        for session in sessions:
            agent = session.agent
            for file in session.changed_files:
                if '.' in file:
                    ext = file.split('.')[-1]
                    agent_file_types[agent][ext] += 1

        for agent, extensions in agent_file_types.items():
            if extensions:
                top_ext, count = extensions.most_common(1)[0]
                patterns[f"agent_specialization_{agent}"] = PatternInfo(
                    pattern_type="agent_specialization",
                    description=f"{agent} frequently works with .{top_ext} files",
                    frequency=count,
                    impact_score=0.4,
                    trend_score=0.3,
                    urgency_score=0.2,
                    examples=[f"{count} .{top_ext} files"],
                    metadata={"agent": agent, "extension": top_ext}
                )

        return patterns

    def analyze_skill_gaps(self, sessions: List[SessionData], commits: List[Dict]) -> Dict[str, PatternInfo]:
        """Detect potential skill gaps"""
        patterns = {}

        # Analyze recurring problems that might need skills
        all_problems = []
        for session in sessions:
            all_problems.extend(session.problems_solved)

        # Detect domains that might need skills
        domain_keywords = {
            "testing": ["test", "testing", "unittest", "pytest", "jest"],
            "deployment": ["deploy", "docker", "kubernetes", "ci/cd", "pipeline"],
            "documentation": ["readme", "docs", "documentation", "markdown"],
            "api": ["api", "endpoint", "request", "response", "rest"],
            "database": ["database", "sql", "query", "migration"],
            "frontend": ["react", "vue", "angular", "css", "html"],
            "backend": ["server", "backend", "node", "python", "java"],
            "performance": ["performance", "optimization", "cache", "speed"],
            "security": ["security", "auth", "authentication", "permission"]
        }

        # Check which domains appear in problems and commits
        domain_scores = defaultdict(int)

        all_text = " ".join(all_problems + [c.get("message", "") for c in commits]).lower()

        for domain, keywords in domain_keywords.items():
            for keyword in keywords:
                if keyword in all_text:
                    domain_scores[domain] += all_text.count(keyword)

        # Detect skill gaps for high-frequency domains
        for domain, score in domain_scores.items():
            if score >= 5:
                patterns[f"skill_gap_{domain}"] = PatternInfo(
                    pattern_type="skill_gap",
                    description=f"Potential skill gap in {domain}",
                    frequency=score,
                    impact_score=0.8,
                    trend_score=0.7,
                    urgency_score=0.7,
                    examples=[f"{domain} mentioned {score} times"],
                    metadata={"domain": domain}
                )

        return patterns