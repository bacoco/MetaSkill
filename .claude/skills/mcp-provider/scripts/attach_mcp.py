#!/usr/bin/env python3
"""
MCP Attachment Script - Integrate MCP tool into a skill

Usage:
    python3 attach_mcp.py --skill-path .claude/skills/my-skill --mcp-id "postgresql-mcp"
    python3 attach_mcp.py --skill-path .claude/skills/my-skill --mcp-id "rest-api" --tool-name "api-tools"
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any


def attach_mcp_to_skill(
    skill_path: Path,
    mcp_id: str,
    tool_name: str = None,
    docker_enabled: bool = True
) -> Dict[str, Any]:
    """
    Attach an MCP tool to a skill directory

    Args:
        skill_path: Path to the skill directory
        mcp_id: MCP tool identifier
        tool_name: Optional custom tool name (defaults to mcp_id)
        docker_enabled: Whether to set up Docker runtime

    Returns:
        Dictionary with attachment result
    """
    skill_path = Path(skill_path)

    if not skill_path.exists():
        raise ValueError(f"Skill path does not exist: {skill_path}")

    # Use mcp_id as tool_name if not provided
    if not tool_name:
        tool_name = mcp_id

    print(f"📦 Attaching MCP tool to skill...")
    print(f"   Skill: {skill_path.name}")
    print(f"   MCP ID: {mcp_id}")
    print(f"   Tool name: {tool_name}")
    print()

    # Create MCP tools directory
    mcp_dir = skill_path / "mcp_tools" / tool_name
    mcp_dir.mkdir(parents=True, exist_ok=True)

    # Generate tool manifest
    manifest = {
        "mcp_id": mcp_id,
        "tool_name": tool_name,
        "transport": "stdio",
        "docker_enabled": docker_enabled,
        "security": {
            "sandbox": "strict",
            "read_only_root": True,
            "network_isolation": True
        },
        "created_at": "2025-10-26T18:00:00Z"
    }

    manifest_path = mcp_dir / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Created manifest: {manifest_path}")

    # Generate example environment file
    env_path = mcp_dir / ".env.example"
    env_content = f"""# Environment variables for {tool_name}
# Copy this to .env and configure with your secrets

# MCP_HOST=localhost
# MCP_PORT=8080
# MCP_API_KEY=your-api-key-here
"""

    with open(env_path, 'w') as f:
        f.write(env_content)

    print(f"✅ Created env template: {env_path}")

    # Generate Docker configuration if enabled
    if docker_enabled:
        docker_config = {
            "image": f"mcp/{mcp_id}:latest",
            "runtime_policy": {
                "read_only": True,
                "drop_capabilities": ["ALL"],
                "network_mode": "none",
                "memory_limit": "512m"
            }
        }

        docker_path = mcp_dir / "docker_config.json"
        with open(docker_path, 'w') as f:
            json.dump(docker_config, f, indent=2)

        print(f"✅ Created Docker config: {docker_path}")

    # Generate usage README
    readme_content = f"""# {tool_name} MCP Tool

MCP tool attached to this skill.

## Configuration

1. Copy `.env.example` to `.env`
2. Configure your credentials in `.env`
3. Run the skill - MCP tool will be available

## Security

- Runs in strict sandbox by default
- Read-only filesystem
- Network isolated
- No access to host system

## Testing

```bash
python3 .claude/skills/mcp-provider/scripts/test_mcp.py \\
  --skill-path {skill_path} \\
  --tool-name {tool_name}
```
"""

    readme_path = mcp_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)

    print(f"✅ Created README: {readme_path}")

    print(f"\n🎉 MCP tool '{tool_name}' successfully attached!")
    print(f"   Directory: {mcp_dir}")

    return {
        "success": True,
        "mcp_dir": str(mcp_dir),
        "manifest_path": str(manifest_path),
        "files_created": [
            str(manifest_path),
            str(env_path),
            str(docker_path) if docker_enabled else None,
            str(readme_path)
        ]
    }


def main():
    parser = argparse.ArgumentParser(
        description="Attach MCP tool to a Claude Code skill"
    )
    parser.add_argument(
        "--skill-path",
        required=True,
        help="Path to the skill directory"
    )
    parser.add_argument(
        "--mcp-id",
        required=True,
        help="MCP tool identifier"
    )
    parser.add_argument(
        "--tool-name",
        help="Custom tool name (defaults to mcp-id)"
    )
    parser.add_argument(
        "--no-docker",
        action="store_true",
        help="Disable Docker runtime setup"
    )

    args = parser.parse_args()

    try:
        result = attach_mcp_to_skill(
            skill_path=args.skill_path,
            mcp_id=args.mcp_id,
            tool_name=args.tool_name,
            docker_enabled=not args.no_docker
        )

        print(f"\n📋 Result:")
        print(json.dumps(result, indent=2))

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
