#!/usr/bin/env python3
"""
Report generation module for Synapse
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import sys

MODULE_DIR = Path(__file__).resolve().parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from data_models import PatternInfo, SkillRecommendation  # type: ignore
from config_manager import ConfigManager  # type: ignore


class ReportGenerator:
    """Generates detailed reports from analysis"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def generate_report(
        self,
        patterns: Dict[str, Any],
        recommendations: List[Any],
        cortex_data: Dict
    ) -> Dict:
        """Generate comprehensive report"""

        normalized_patterns = {
            key: self._coerce_pattern(key, value)
            for key, value in (patterns or {}).items()
        }

        normalized_recommendations = [
            self._coerce_recommendation(item)
            for item in (recommendations or [])
        ]

        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "analyzer": "Synapse Pattern Detector",
                "version": "2.0.0"
            },
            "summary": self._generate_summary(normalized_patterns, normalized_recommendations, cortex_data),
            "patterns": self._format_patterns(normalized_patterns),
            "recommendations": self._format_recommendations(normalized_recommendations),
            "trend_analysis": self._generate_trend_analysis(cortex_data),
            "priority_matrix": self._generate_priority_matrix(normalized_recommendations),
            "actionable_insights": self._generate_insights(normalized_patterns, normalized_recommendations)
        }

        return report

    def _coerce_pattern(self, key: str, pattern: Any) -> PatternInfo:
        """Convert raw pattern data into a PatternInfo instance."""

        if isinstance(pattern, PatternInfo):
            return pattern

        if isinstance(pattern, dict):
            metadata = {
                k: v
                for k, v in pattern.items()
                if k not in {"pattern_type", "description", "frequency", "count", "impact_score", "trend_score", "urgency_score", "examples"}
            }

            frequency = pattern.get("frequency", pattern.get("count", 0))
            urgency_raw = pattern.get("urgency_score", pattern.get("priority", 0))
            try:
                urgency_score = float(urgency_raw)
            except (TypeError, ValueError):
                urgency_score = 0.0

            examples = pattern.get("examples", [])
            if not isinstance(examples, list):
                examples = [str(examples)] if examples else []

            return PatternInfo(
                pattern_type=pattern.get("pattern_type", key),
                description=pattern.get("description", key.replace('_', ' ').title()),
                frequency=int(frequency or 0),
                impact_score=float(pattern.get("impact_score", 0.0)),
                trend_score=float(pattern.get("trend_score", 0.0)),
                urgency_score=urgency_score,
                examples=[str(example) for example in examples],
                metadata=metadata,
            )

        raise TypeError(f"Unsupported pattern data type: {type(pattern)!r}")

    def _coerce_recommendation(self, recommendation: Any) -> SkillRecommendation:
        """Convert raw recommendation data into a SkillRecommendation instance."""

        if isinstance(recommendation, SkillRecommendation):
            return recommendation

        if isinstance(recommendation, dict):
            supporting_patterns = recommendation.get("supporting_patterns", [])
            if not isinstance(supporting_patterns, list):
                supporting_patterns = [str(supporting_patterns)]

            example_use_cases = recommendation.get("example_use_cases", [])
            if not isinstance(example_use_cases, list):
                example_use_cases = [str(example_use_cases)]

            return SkillRecommendation(
                skill_name=recommendation.get("skill_name", "unnamed-skill"),
                skill_type=recommendation.get("skill_type", "general"),
                description=recommendation.get("description", ""),
                reason=recommendation.get("reason", ""),
                priority_score=float(recommendation.get("priority_score", 0.0)),
                frequency_score=float(recommendation.get("frequency_score", recommendation.get("frequency", 0.0))),
                impact_score=float(recommendation.get("impact_score", 0.0)),
                trend_score=float(recommendation.get("trend_score", 0.0)),
                urgency_score=float(recommendation.get("urgency_score", recommendation.get("priority", 0.0))),
                roi_score=float(recommendation.get("roi_score", 0.0)),
                supporting_patterns=[str(item) for item in supporting_patterns],
                example_use_cases=[str(item) for item in example_use_cases],
            )

        raise TypeError(f"Unsupported recommendation data type: {type(recommendation)!r}")

    def _generate_summary(
        self,
        patterns: Dict[str, PatternInfo],
        recommendations: List[SkillRecommendation],
        cortex_data: Dict
    ) -> Dict:
        """Generate executive summary"""
        sessions = cortex_data.get("sessions", [])

        return {
            "total_sessions_analyzed": len(sessions),
            "patterns_detected": len(patterns),
            "skills_recommended": len(recommendations),
            "top_recommendation": recommendations[0].skill_name if recommendations else None,
            "highest_priority_score": recommendations[0].priority_score if recommendations else 0,
            "most_frequent_pattern": max(patterns.items(), key=lambda x: x[1].frequency)[0] if patterns else None
        }

    def _format_patterns(self, patterns: Dict[str, PatternInfo]) -> List[Dict]:
        """Format patterns for report"""
        formatted = []

        for pattern_key, pattern in sorted(patterns.items(), key=lambda x: x[1].frequency, reverse=True):
            formatted.append({
                "key": pattern_key,
                "type": pattern.pattern_type,
                "description": pattern.description,
                "frequency": pattern.frequency,
                "scores": {
                    "impact": pattern.impact_score,
                    "trend": pattern.trend_score,
                    "urgency": pattern.urgency_score
                },
                "examples": pattern.examples[:3],
                "metadata": pattern.metadata
            })

        return formatted

    def _format_recommendations(self, recommendations: List[SkillRecommendation]) -> List[Dict]:
        """Format recommendations for report"""
        formatted = []

        for rec in recommendations:
            formatted.append({
                "skill_name": rec.skill_name,
                "skill_type": rec.skill_type,
                "description": rec.description,
                "reason": rec.reason,
                "priority_score": round(rec.priority_score, 3),
                "detailed_scores": {
                    "frequency": round(rec.frequency_score, 3),
                    "impact": round(rec.impact_score, 3),
                    "trend": round(rec.trend_score, 3),
                    "urgency": round(rec.urgency_score, 3),
                    "roi": round(rec.roi_score, 3)
                },
                "supporting_patterns": rec.supporting_patterns,
                "example_use_cases": rec.example_use_cases[:5]
            })

        return formatted

    def _generate_trend_analysis(self, cortex_data: Dict) -> Dict:
        """Generate trend analysis"""
        sessions = cortex_data.get("sessions", [])

        if not sessions:
            return {}

        # Calculate averages
        total_files = sum(s.total_files for s in sessions)
        avg_files_per_session = total_files / len(sessions) if sessions else 0

        # Analyze session frequency
        timestamps = []
        for session in sessions:
            try:
                dt = datetime.strptime(session.timestamp, "%Y-%m-%d-%H:%M")
                timestamps.append(dt)
            except:
                continue

        session_frequency = 0
        if len(timestamps) >= 2:
            time_span = (timestamps[-1] - timestamps[0]).total_seconds() / 3600  # hours
            session_frequency = len(timestamps) / (time_span / 24) if time_span > 0 else 0  # sessions per day

        return {
            "session_frequency_per_day": round(session_frequency, 2),
            "avg_files_per_session": round(avg_files_per_session, 1),
            "total_sessions": len(sessions),
            "most_active_agent": max(sessions, key=lambda s: sessions.count(s)).agent if sessions else None
        }

    def _generate_priority_matrix(self, recommendations: List[SkillRecommendation]) -> Dict:
        """Generate priority matrix for recommendations"""

        high_priority = []
        medium_priority = []
        low_priority = []

        for rec in recommendations:
            if rec.priority_score >= 0.7:
                high_priority.append(rec.skill_name)
            elif rec.priority_score >= 0.5:
                medium_priority.append(rec.skill_name)
            else:
                low_priority.append(rec.skill_name)

        return {
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority
        }

    def _generate_insights(
        self,
        patterns: Dict[str, PatternInfo],
        recommendations: List[SkillRecommendation]
    ) -> List[str]:
        """Generate actionable insights"""
        insights = []

        # Insight 1: Most urgent patterns
        urgent_patterns = [p for p in patterns.values() if p.urgency_score > 0.7]
        if urgent_patterns:
            insights.append(
                f"Found {len(urgent_patterns)} high-urgency patterns that should be addressed immediately"
            )

        # Insight 2: Top recommendation
        if recommendations:
            top_rec = recommendations[0]
            insights.append(
                f"Top recommendation: {top_rec.skill_name} with priority score {top_rec.priority_score:.2f}"
            )

        # Insight 3: Problem recurrence
        problem_patterns = [p for p in patterns.values() if p.pattern_type == "problem_recurrence"]
        if problem_patterns:
            insights.append(
                f"Detected {len(problem_patterns)} recurring problems that could be prevented with automation"
            )

        # Insight 4: Skill gaps
        skill_gap_patterns = [p for p in patterns.values() if p.pattern_type == "skill_gap"]
        if skill_gap_patterns:
            domains = [p.metadata.get("domain") for p in skill_gap_patterns if "domain" in p.metadata]
            if domains:
                insights.append(
                    f"Identified skill gaps in: {', '.join(set(domains))}"
                )

        # Insight 5: High ROI opportunities
        high_roi_recs = [r for r in recommendations if r.roi_score > 0.7]
        if high_roi_recs:
            insights.append(
                f"Found {len(high_roi_recs)} high-ROI skill opportunities that would provide significant value"
            )

        return insights

    def save_report(self, report: Dict, output_path: str, format: str = "both"):
        """Save report to file"""

        try:
            output_path_obj = Path(output_path)

            if format in ["json", "both"]:
                json_path = output_path_obj.with_suffix(".json")
                with open(json_path, 'w') as f:
                    json.dump(report, f, indent=2)
                self.logger.info(f"Saved JSON report to {json_path}")

            if format in ["text", "both"]:
                text_path = output_path_obj.with_suffix(".txt")
                text_report = self._format_text_report(report)
                with open(text_path, 'w') as f:
                    f.write(text_report)
                self.logger.info(f"Saved text report to {text_path}")

        except Exception as e:
            self.logger.error(f"Error saving report: {e}")

    def _format_text_report(self, report: Dict) -> str:
        """Format report as human-readable text"""
        lines = []

        lines.append("=" * 80)
        lines.append("Synapse PATTERN DETECTION REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Metadata
        lines.append(f"Generated: {report['metadata']['generated_at']}")
        lines.append(f"Analyzer: {report['metadata']['analyzer']}")
        lines.append("")

        # Summary
        lines.append("SUMMARY")
        lines.append("-" * 80)
        summary = report['summary']
        for key, value in summary.items():
            lines.append(f"{key.replace('_', ' ').title()}: {value}")
        lines.append("")

        # Recommendations
        lines.append("SKILL RECOMMENDATIONS")
        lines.append("-" * 80)
        for i, rec in enumerate(report['recommendations'], 1):
            lines.append(f"\n{i}. {rec['skill_name']} (Priority: {rec['priority_score']:.2f})")
            lines.append(f"   Type: {rec['skill_type']}")
            lines.append(f"   Description: {rec['description']}")
            lines.append(f"   Reason: {rec['reason']}")
            lines.append(f"   Scores:")
            for score_name, score_value in rec['detailed_scores'].items():
                lines.append(f"     - {score_name.title()}: {score_value:.2f}")
        lines.append("")

        # Priority Matrix
        lines.append("PRIORITY MATRIX")
        lines.append("-" * 80)
        matrix = report['priority_matrix']
        lines.append(f"High Priority ({len(matrix['high_priority'])}): {', '.join(matrix['high_priority']) if matrix['high_priority'] else 'None'}")
        lines.append(f"Medium Priority ({len(matrix['medium_priority'])}): {', '.join(matrix['medium_priority']) if matrix['medium_priority'] else 'None'}")
        lines.append(f"Low Priority ({len(matrix['low_priority'])}): {', '.join(matrix['low_priority']) if matrix['low_priority'] else 'None'}")
        lines.append("")

        # Actionable Insights
        lines.append("ACTIONABLE INSIGHTS")
        lines.append("-" * 80)
        for i, insight in enumerate(report['actionable_insights'], 1):
            lines.append(f"{i}. {insight}")
        lines.append("")

        # Patterns Summary
        lines.append("DETECTED PATTERNS")
        lines.append("-" * 80)
        lines.append(f"Total patterns detected: {len(report['patterns'])}")
        lines.append("\nTop 10 patterns by frequency:")
        for i, pattern in enumerate(report['patterns'][:10], 1):
            lines.append(f"{i}. {pattern['description']} (Frequency: {pattern['frequency']})")
        lines.append("")

        lines.append("=" * 80)
        lines.append("End of Report")
        lines.append("=" * 80)

        return "\n".join(lines)