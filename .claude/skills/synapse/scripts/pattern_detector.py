#!/usr/bin/env python3
"""
Synapse Pattern Detector - Main Orchestrator
Analyzes Cortex files to detect patterns and recommend skills.

This is a streamlined orchestrator that uses modular components:
- ConfigManager: Manages configuration
- CortexDataReader: Reads and parses Cortex files
- PatternDetector: Detects patterns
- SkillRecommender: Recommends skills
- ReportGenerator: Generates reports
"""

import argparse
import logging
from pathlib import Path
from typing import Dict, Optional

# Import modules
from modules import (
    ConfigManager,
    CortexDataReader,
    PatternDetector,
    SkillRecommender,
    ReportGenerator
)


class PatternDetectorMain:
    """Main pattern detector orchestrator"""

    def __init__(self, config_path: Optional[str] = None, repo_root: str = "."):
        self.config = ConfigManager(config_path)
        self.repo_root = repo_root

        # Setup logging
        log_level = logging.DEBUG if self.config.get("output", "verbose", default=True) else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='[%(levelname)s] %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Validate config
        if not self.config.validate():
            self.logger.warning("Configuration validation failed, using defaults")

        # Initialize components
        self.cortex_reader = CortexDataReader(repo_root, self.config)
        self.pattern_detector = PatternDetector(self.config)
        self.skill_recommender = SkillRecommender(self.config)
        self.report_generator = ReportGenerator(self.config)

    def run_analysis(self, output_path: Optional[str] = None) -> Dict:
        """Run complete pattern analysis"""

        self.logger.info("Starting Synapse pattern detection analysis")

        # Step 1: Read Cortex data
        self.logger.info("Reading Cortex data...")
        cortex_data = self.cortex_reader.read_all_cortex_data()

        if not cortex_data.get("sessions"):
            self.logger.error("No session data found. Cannot perform analysis.")
            return {}

        # Step 2: Detect patterns
        self.logger.info("Detecting patterns...")
        patterns = self.pattern_detector.analyze_all_patterns(cortex_data)

        if not patterns:
            self.logger.warning("No patterns detected")

        # Step 3: Generate recommendations
        self.logger.info("Generating skill recommendations...")
        recommendations = self.skill_recommender.recommend_skills(patterns)

        # Step 4: Generate report
        self.logger.info("Generating report...")
        report = self.report_generator.generate_report(patterns, recommendations, cortex_data)

        # Step 5: Save report if output path specified
        if output_path:
            report_format = self.config.get("output", "report_format", default="both")
            self.report_generator.save_report(report, output_path, format=report_format)

        self.logger.info("Analysis complete!")

        return report

    def print_summary(self, report: Dict):
        """Print report summary to console"""

        print("\n" + "=" * 80)
        print("Synapse PATTERN DETECTION - SUMMARY")
        print("=" * 80)

        summary = report.get("summary", {})
        print(f"\nSessions Analyzed: {summary.get('total_sessions_analyzed', 0)}")
        print(f"Patterns Detected: {summary.get('patterns_detected', 0)}")
        print(f"Skills Recommended: {summary.get('skills_recommended', 0)}")

        if summary.get('top_recommendation'):
            print(f"\nTop Recommendation: {summary['top_recommendation']}")
            print(f"Priority Score: {summary.get('highest_priority_score', 0):.2f}")

        # Print top 3 recommendations
        recommendations = report.get("recommendations", [])
        if recommendations:
            print("\n" + "-" * 80)
            print("TOP SKILL RECOMMENDATIONS:")
            print("-" * 80)
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"\n{i}. {rec['skill_name']} (Priority: {rec['priority_score']:.2f})")
                print(f"   {rec['description']}")
                print(f"   Reason: {rec['reason'][:100]}...")

        # Print actionable insights
        insights = report.get("actionable_insights", [])
        if insights:
            print("\n" + "-" * 80)
            print("ACTIONABLE INSIGHTS:")
            print("-" * 80)
            for i, insight in enumerate(insights, 1):
                print(f"{i}. {insight}")

        print("\n" + "=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Synapse Pattern Detector - Analyze Cortex files and recommend skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze current repository
  python pattern_detector.py

  # Analyze with custom config
  python pattern_detector.py --config synapse_config.json

  # Specify repository root
  python pattern_detector.py --repo /path/to/repo

  # Save report to file
  python pattern_detector.py --output pattern_report

  # Generate JSON report only
  python pattern_detector.py --output report --format json
        """
    )

    parser.add_argument(
        "--config",
        help="Path to Synapse configuration file (JSON)",
        type=str
    )

    parser.add_argument(
        "--repo",
        help="Repository root path (default: current directory)",
        type=str,
        default="."
    )

    parser.add_argument(
        "--output",
        help="Output path for report (without extension)",
        type=str
    )

    parser.add_argument(
        "--format",
        help="Report format: json, text, or both (default: both)",
        choices=["json", "text", "both"],
        default="both"
    )

    parser.add_argument(
        "--quiet",
        help="Suppress console output",
        action="store_true"
    )

    parser.add_argument(
        "--version",
        help="Show version and exit",
        action="version",
        version="Synapse Pattern Detector v2.0.0"
    )

    args = parser.parse_args()

    # Initialize detector
    detector = PatternDetectorMain(
        config_path=args.config,
        repo_root=args.repo
    )

    # Run analysis
    report = detector.run_analysis(output_path=args.output)

    # Print summary unless quiet mode
    if not args.quiet and report:
        detector.print_summary(report)

    return 0 if report else 1


if __name__ == "__main__":
    exit(main())