import json
import tempfile
from pathlib import Path
import importlib.util


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
