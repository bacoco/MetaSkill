"""
Test suite for Synapse modules
"""

import json
import tempfile
from pathlib import Path
import importlib.util


def load_module(module_name, relative_path):
    """Helper to load a module from file path"""
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / relative_path
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore
    return module


def test_pattern_detection():
    """Test basic pattern detection functionality"""
    try:
        # Load pattern analysis module
        pattern_module = load_module(
            "pattern_analysis",
            ".claude/skills/synapse/scripts/modules/pattern_analysis.py"
        )

        # Load config module
        config_module = load_module(
            "config_manager",
            ".claude/skills/synapse/scripts/modules/config_manager.py"
        )

        # Create test config
        config = config_module.ConfigManager()

        # Create detector
        detector = pattern_module.PatternDetector(config)

        # Test with empty data
        patterns = detector.analyze_all_patterns({"sessions": []})
        assert isinstance(patterns, dict)
        assert len(patterns) == 0

    except Exception as e:
        raise AssertionError(f"Pattern detection test failed: {e}")


def test_config_validation():
    """Test configuration validation"""
    try:
        config_module = load_module(
            "config_manager",
            ".claude/skills/synapse/scripts/modules/config_manager.py"
        )

        # Test default config
        config = config_module.ConfigManager()
        assert config.validate() == True

        # Test getting values
        threshold = config.get("analysis", "pattern_threshold", default=5)
        assert threshold == 5

        # Test with custom config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "analysis": {
                    "pattern_threshold": 10,
                    "lookback_days": 14
                }
            }, f)
            config_file = f.name

        custom_config = config_module.ConfigManager(config_file)
        custom_threshold = custom_config.get("analysis", "pattern_threshold", default=5)
        assert custom_threshold == 10

        # Cleanup
        Path(config_file).unlink(missing_ok=True)

    except Exception as e:
        raise AssertionError(f"Config validation test failed: {e}")


def test_data_models():
    """Test data model validation"""
    try:
        data_models = load_module(
            "data_models",
            ".claude/skills/synapse/scripts/modules/data_models.py"
        )

        # Test SessionData
        session = data_models.SessionData(
            timestamp="2025-10-26-14:30",
            agent="test-agent",
            changed_files=["file1.py", "file2.py"],
            problems_solved=[]
        )

        assert session.timestamp == "2025-10-26-14:30"
        assert len(session.changed_files) == 2
        assert session.agent == "test-agent"

        # Test PatternInfo
        pattern = data_models.PatternInfo(
            pattern_type="test_pattern",
            description="Test pattern description",
            frequency=5,
            impact_score=0.8,
            trend_score=0.6,
            urgency_score=0.7,
            examples=["example1"],
            metadata={"test": "value"}
        )

        assert pattern.pattern_type == "test_pattern"
        assert pattern.impact_score == 0.8
        assert pattern.combined_priority_score() > 0

    except Exception as e:
        raise AssertionError(f"Data models test failed: {e}")


# Export all test functions
__all__ = [
    "test_pattern_detection",
    "test_config_validation",
    "test_data_models"
]