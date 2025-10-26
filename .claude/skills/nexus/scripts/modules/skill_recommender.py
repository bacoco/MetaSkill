#!/usr/bin/env python3
"""
Skill recommendation module for NEXUS
"""

import logging
from collections import defaultdict
from typing import Dict, List, Optional

from .data_models import PatternInfo, SkillRecommendation
from .config_manager import ConfigManager


class SkillRecommender:
    """Recommends skills based on detected patterns"""

    # Skill templates for different domains
    SKILL_TEMPLATES = {
        "testing": {
            "name": "TEST-GUARDIAN",
            "type": "testing",
            "description": "Automated testing assistance and test generation",
            "capabilities": ["test generation", "test automation", "coverage analysis"]
        },
        "deployment": {
            "name": "DEPLOY-SAGE",
            "type": "deployment",
            "description": "Deployment automation and CI/CD optimization",
            "capabilities": ["deployment automation", "CI/CD", "container management"]
        },
        "documentation": {
            "name": "DOC-GENIUS",
            "type": "documentation",
            "description": "Automatic documentation generation and maintenance",
            "capabilities": ["doc generation", "readme creation", "API documentation"]
        },
        "api": {
            "name": "API-MASTER",
            "type": "api",
            "description": "API design, implementation, and testing assistance",
            "capabilities": ["API design", "endpoint creation", "API testing"]
        },
        "performance": {
            "name": "PERF-OPTIMIZER",
            "type": "performance",
            "description": "Performance analysis and optimization",
            "capabilities": ["profiling", "optimization", "caching strategies"]
        },
        "security": {
            "name": "SECURITY-SHIELD",
            "type": "security",
            "description": "Security analysis and vulnerability detection",
            "capabilities": ["security scanning", "vulnerability detection", "auth implementation"]
        },
        "refactoring": {
            "name": "CODE-REFINER",
            "type": "refactoring",
            "description": "Code refactoring and quality improvement",
            "capabilities": ["code refactoring", "quality analysis", "pattern application"]
        },
        "data_processing": {
            "name": "DATA-WIZARD",
            "type": "data",
            "description": "Data processing and analysis automation",
            "capabilities": ["data transformation", "ETL", "analysis"]
        }
    }

    def __init__(self, config: ConfigManager):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def recommend_skills(self, patterns: Dict[str, PatternInfo]) -> List[SkillRecommendation]:
        """Generate skill recommendations based on patterns"""
        recommendations = []

        # Group patterns by domain
        domain_patterns = self._group_patterns_by_domain(patterns)

        # Generate recommendations for each domain
        for domain, domain_pattern_list in domain_patterns.items():
            if len(domain_pattern_list) >= 2 or any(p.frequency >= 5 for p in domain_pattern_list):
                recommendation = self._create_skill_recommendation(domain, domain_pattern_list)
                if recommendation:
                    recommendations.append(recommendation)

        # Sort by priority score
        recommendations.sort(key=lambda r: r.priority_score, reverse=True)

        # Filter by minimum score threshold
        min_score = self.config.get("thresholds", "recommendation_min_score", default=0.5)
        recommendations = [r for r in recommendations if r.priority_score >= min_score]

        self.logger.info(f"Generated {len(recommendations)} skill recommendations")

        return recommendations

    def _group_patterns_by_domain(self, patterns: Dict[str, PatternInfo]) -> Dict[str, List[PatternInfo]]:
        """Group patterns by domain/category"""
        domain_patterns = defaultdict(list)

        # Domain keywords mapping
        domain_keywords = {
            "testing": ["test", "testing", "unittest", "pytest"],
            "deployment": ["deploy", "docker", "ci/cd", "pipeline"],
            "documentation": ["readme", "docs", "documentation", "md"],
            "api": ["api", "endpoint", "request", "response"],
            "performance": ["performance", "optimization", "cache"],
            "security": ["security", "auth", "authentication"],
            "refactoring": ["refactor", "cleanup", "quality"],
            "data_processing": ["data", "csv", "json", "process"]
        }

        for pattern_key, pattern in patterns.items():
            # Check pattern type and description for domain keywords
            pattern_text = f"{pattern.pattern_type} {pattern.description}".lower()

            matched_domain = None
            for domain, keywords in domain_keywords.items():
                if any(keyword in pattern_text for keyword in keywords):
                    matched_domain = domain
                    break

            # Also check metadata for specific domains
            if not matched_domain:
                if "skill_gap" in pattern_key:
                    domain = pattern.metadata.get("domain")
                    if domain:
                        matched_domain = domain

            if matched_domain:
                domain_patterns[matched_domain].append(pattern)
            else:
                # General category
                domain_patterns["general"].append(pattern)

        return domain_patterns

    def _create_skill_recommendation(self, domain: str, patterns: List[PatternInfo]) -> Optional[SkillRecommendation]:
        """Create a skill recommendation for a domain"""

        # Get skill template
        template = self.SKILL_TEMPLATES.get(domain)
        if not template:
            return None

        # Calculate scores
        frequency_score = self._calculate_frequency_score(patterns)
        impact_score = self._calculate_impact_score(patterns)
        trend_score = self._calculate_trend_score(patterns)
        urgency_score = self._calculate_urgency_score(patterns)
        roi_score = self._calculate_roi_score(patterns)

        # Calculate weighted priority score
        weights = self.config.config["scoring"]
        priority_score = (
            frequency_score * weights["frequency_weight"] +
            impact_score * weights["impact_weight"] +
            trend_score * weights["trend_weight"] +
            urgency_score * weights["urgency_weight"] +
            roi_score * weights["roi_weight"]
        )

        # Generate reason
        reason = self._generate_recommendation_reason(domain, patterns)

        # Extract example use cases
        example_use_cases = []
        for pattern in patterns[:3]:
            example_use_cases.extend(pattern.examples[:2])

        return SkillRecommendation(
            skill_name=template["name"],
            skill_type=template["type"],
            description=template["description"],
            reason=reason,
            priority_score=priority_score,
            frequency_score=frequency_score,
            impact_score=impact_score,
            trend_score=trend_score,
            urgency_score=urgency_score,
            roi_score=roi_score,
            supporting_patterns=[p.description for p in patterns],
            example_use_cases=example_use_cases
        )

    def _calculate_frequency_score(self, patterns: List[PatternInfo]) -> float:
        """Calculate frequency score (0-1)"""
        total_frequency = sum(p.frequency for p in patterns)
        max_frequency = self.config.get("thresholds", "pattern_frequency_high", default=6) * len(patterns)
        return min(total_frequency / max_frequency, 1.0)

    def _calculate_impact_score(self, patterns: List[PatternInfo]) -> float:
        """Calculate impact score (0-1)"""
        if not patterns:
            return 0.0
        avg_impact = sum(p.impact_score for p in patterns) / len(patterns)
        return avg_impact

    def _calculate_trend_score(self, patterns: List[PatternInfo]) -> float:
        """Calculate trend score (0-1)"""
        if not patterns:
            return 0.0
        avg_trend = sum(p.trend_score for p in patterns) / len(patterns)
        return avg_trend

    def _calculate_urgency_score(self, patterns: List[PatternInfo]) -> float:
        """Calculate urgency score (0-1)"""
        if not patterns:
            return 0.0
        avg_urgency = sum(p.urgency_score for p in patterns) / len(patterns)
        return avg_urgency

    def _calculate_roi_score(self, patterns: List[PatternInfo]) -> float:
        """Calculate ROI score (0-1)"""
        # ROI based on frequency and impact
        if not patterns:
            return 0.0
        total_frequency = sum(p.frequency for p in patterns)
        avg_impact = sum(p.impact_score for p in patterns) / len(patterns)

        # Higher frequency + higher impact = higher ROI
        roi = (total_frequency / 10) * avg_impact
        return min(roi, 1.0)

    def _generate_recommendation_reason(self, domain: str, patterns: List[PatternInfo]) -> str:
        """Generate human-readable reason for recommendation"""
        pattern_count = len(patterns)
        total_frequency = sum(p.frequency for p in patterns)
        avg_impact = sum(p.impact_score for p in patterns) / len(patterns)

        reason = f"Detected {pattern_count} patterns in {domain} domain with {total_frequency} total occurrences. "

        if avg_impact > 0.7:
            reason += f"High impact ({avg_impact:.1f}) suggests significant productivity gains. "

        # Add specific pattern insights
        problem_patterns = [p for p in patterns if p.pattern_type == "problem_recurrence"]
        if problem_patterns:
            reason += f"Found {len(problem_patterns)} recurring problems that could be automated. "

        skill_gap_patterns = [p for p in patterns if p.pattern_type == "skill_gap"]
        if skill_gap_patterns:
            reason += f"Skill gap detected: frequent {domain} work without specialized tooling. "

        return reason.strip()