"""
Tests complets pour Cortex API.
Couvre toutes les fonctions critiques avec différents scénarios.
"""

import json
import tempfile
from pathlib import Path
import importlib.util
from datetime import datetime, timedelta


def load_cortex_api_module():
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / ".claude/skills/cortex/scripts/cortex_api.py"
    spec = importlib.util.spec_from_file_location("cortex_api", str(module_path))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore
    return module


def test_event_limit_enforced():
    cortex_api = load_cortex_api_module()
    cortex_api.clear_cortex_instances()

    with tempfile.TemporaryDirectory() as tmpdir:
        inst = cortex_api.get_cortex_instance(tmpdir)
        max_events = getattr(cortex_api, "MAX_EVENTS", 1000)

        # Add more than limit
        for i in range(max_events + 25):
            inst.add_event("test", f"event-{i}")

        events = inst.get_events()
        assert len(events) == max_events
        # Last event should be the last one appended
        assert events[-1]["description"] == f"event-{max_events + 24}"


def test_status_file_is_valid_json_after_writes():
    cortex_api = load_cortex_api_module()
    cortex_api.clear_cortex_instances()

    with tempfile.TemporaryDirectory() as tmpdir:
        inst = cortex_api.get_cortex_instance(tmpdir)
        inst.add_event("test", "initial")
        inst.add_event("test", "second")

        status_path = Path(tmpdir) / ".cortex_status.json"
        assert status_path.exists()

        # Should be valid JSON
        with open(status_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict)
        assert "custom_events" in data


def test_get_events_with_filters():
    """Test event retrieval with different filters"""
    cortex_api = load_cortex_api_module()
    cortex_api.clear_cortex_instances()

    with tempfile.TemporaryDirectory() as tmpdir:
        inst = cortex_api.get_cortex_instance(tmpdir)

        # Add various events
        inst.add_event("api_call", "API call 1", {"endpoint": "/users"})
        inst.add_event("data_processing", "Process CSV", {"rows": 100})
        inst.add_event("api_call", "API call 2", {"endpoint": "/posts"})

        # Test filter by type
        api_events = inst.get_events(filter_type="api_call")
        assert len(api_events) == 2

        # Test limit
        limited = inst.get_events(limit=1)
        assert len(limited) == 1


def test_pattern_analysis():
    """Test pattern analysis functionality"""
    cortex_api = load_cortex_api_module()
    cortex_api.clear_cortex_instances()

    with tempfile.TemporaryDirectory() as tmpdir:
        inst = cortex_api.get_cortex_instance(tmpdir)

        # Add repeated patterns
        for i in range(6):
            inst.add_event("api_call", f"API call {i}")

        # Analyze patterns
        patterns = inst.get_pattern_analysis(days=7, threshold=5)

        assert "patterns" in patterns
        assert "api_call" in patterns["patterns"]
        assert patterns["patterns"]["api_call"]["count"] >= 5


def test_session_summary():
    """Test session summary generation"""
    cortex_api = load_cortex_api_module()
    cortex_api.clear_cortex_instances()

    with tempfile.TemporaryDirectory() as tmpdir:
        inst = cortex_api.get_cortex_instance(tmpdir)

        # Add events
        inst.add_event("test1", "Event 1")
        inst.add_event("test2", "Event 2")

        summary = inst.get_session_summary()

        assert "total_events" in summary
        assert summary["total_events"] == 2
        assert "event_counts" in summary
        assert "last_event" in summary


def test_atomic_write_safety():
    """Test atomic write prevents corruption"""
    cortex_api = load_cortex_api_module()
    cortex_api.clear_cortex_instances()

    with tempfile.TemporaryDirectory() as tmpdir:
        inst = cortex_api.get_cortex_instance(tmpdir)

        # Simulate multiple rapid writes
        for i in range(10):
            inst.add_event("rapid", f"Event {i}")

        # File should still be valid
        status_path = Path(tmpdir) / ".cortex_status.json"
        with open(status_path, "r") as f:
            data = json.load(f)

        assert len(data["custom_events"]) == 10
