# MCP Provider Skill

The MCP Provider skill discovers, validates, and attaches Model Context Protocol (MCP) tools to generated skills. It is intended to be invoked by Forge or human creators during the skill construction pipeline.

## Capabilities
- Discover MCP catalog entries from approved sources.
- Score and validate candidates against requested intents and security policies.
- Generate tool artifacts inside `.claude/skills/<skill-name>/` directories.
- Optionally prepare sandboxed Docker runtimes for MCP execution and run health checks.

## Security Considerations
- Only allowlisted sources are processed.
- Docker executions default to a strict sandbox profile (read-only filesystem, dropped capabilities, network isolation).
- Secrets are never logged and must be provided via environment files or secrets management.

## Usage
```python
from skills.mcp_provider.provider_api import (
    discover_mcp,
    select_and_attach_mcp,
    ensure_runtime,
    test_mcp,
)
```

Refer to the repository README for detailed workflow integration guidance.
