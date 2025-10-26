"""Tests for the MCP Provider scaffolding."""
from pathlib import Path

import pytest

from skills.mcp_provider import (
    Candidate,
    discover_mcp,
    ensure_runtime,
    select_and_attach_mcp,
    test_mcp,
)
from skills.mcp_provider.attach.artifacts import generate_tool_artifacts
from skills.mcp_provider.discovery import sources
from skills.mcp_provider.logging import AuditLogger
from skills.mcp_provider.runtime import docker_runner
from skills.mcp_provider.selection.validator import ValidationError, validate_candidate
from skills.mcp_provider.selection.scorer import score_candidates


def test_default_sources_allowlist_is_empty():
    assert sources.DEFAULT_SOURCES == []


def test_resolve_sources_rejects_unknown_url():
    with pytest.raises(sources.SourceNotAllowedError):
        sources.resolve_sources(["https://example.com/llms.txt"])


def test_validate_candidate_detects_missing_fields():
    candidate = Candidate(
        id="demo",
        name="Demo",
        capabilities=(),
        transport="stdio",
    )
    with pytest.raises(ValidationError):
        validate_candidate(candidate)


def test_generate_tool_artifacts_provides_paths(tmp_path: Path):
    candidate = Candidate(
        id="demo",
        name="Demo",
        capabilities=("sql.query",),
        transport="stdio",
    )
    tool_config = generate_tool_artifacts(
        skill_path=tmp_path,
        candidate=candidate,
        mode="default",
    )
    assert tool_config.manifest_path == tmp_path / "tools" / "mcp_demo.json"
    assert tool_config.env_file_path == tmp_path / ".env.mcp"


def test_discover_mcp_not_implemented():
    with pytest.raises(NotImplementedError):
        discover_mcp()


def test_select_and_attach_mcp_requires_candidates(tmp_path: Path):
    with pytest.raises(ValueError):
        select_and_attach_mcp(skill_path=tmp_path, candidates=[])

    candidate = Candidate(
        id="demo",
        name="Demo",
        capabilities=("sql.query",),
        transport="stdio",
    )
    with pytest.raises(NotImplementedError):
        select_and_attach_mcp(skill_path=tmp_path, candidates=[candidate])


def test_ensure_runtime_requires_id():
    with pytest.raises(ValueError):
        ensure_runtime(mcp_id="")


def test_test_mcp_requires_tool_name(tmp_path: Path):
    candidate = Candidate(
        id="demo",
        name="Demo",
        capabilities=("sql.query",),
        transport="stdio",
    )
    tool_config = generate_tool_artifacts(
        skill_path=tmp_path,
        candidate=candidate,
        mode="default",
    )
    tool_config = type(tool_config)(  # create mutated copy with empty name
        tool_name="",
        skill_path=tool_config.skill_path,
        manifest_path=tool_config.manifest_path,
        env_file_path=tool_config.env_file_path,
        extra_files=tool_config.extra_files,
    )
    with pytest.raises(ValueError):
        test_mcp(tool_config)


def test_docker_runner_builds_command():
    command = docker_runner.build_docker_command(image="demo:1.0")
    assert command[0:3] == ("docker", "run", "--rm")
    assert command[-1] == "demo:1.0"


def test_score_candidates_returns_placeholder_scores():
    candidate = Candidate(
        id="demo",
        name="Demo",
        capabilities=("sql.query",),
        transport="stdio",
    )
    scored = score_candidates([candidate], intents=["sql.query"])
    assert scored[0].score == 0.0
    assert "scoring not implemented" in scored[0].reasons[0]


def test_audit_logger_writes_json(tmp_path: Path):
    logfile = tmp_path / "audit.log"
    logger = AuditLogger(logfile=logfile)
    logger.log("demo", {"key": "value"})
    contents = logfile.read_text(encoding="utf-8")
    assert "\"event\": " in contents
