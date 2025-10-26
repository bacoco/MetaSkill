<!-- Load this when user needs detailed MCP integration guide -->

# MCP Integration Reference

Complete guide for integrating Model Context Protocol (MCP) tools into Claude Code skills.

## Table of Contents

1. [Overview](#overview)
2. [MCP Catalog Structure](#mcp-catalog-structure)
3. [Security Model](#security-model)
4. [API Reference](#api-reference)
5. [Docker Runtime](#docker-runtime)
6. [Troubleshooting](#troubleshooting)

---

## Overview

### What is MCP?

Model Context Protocol (MCP) is a standard protocol for connecting AI models to external tools and data sources. The MCP Provider skill helps you integrate these tools into your Claude Code skills.

### Integration Flow

```
1. Discover MCP tools from catalogs
   ↓
2. Score and validate candidates
   ↓
3. Generate tool configuration
   ↓
4. (Optional) Set up Docker runtime
   ↓
5. Test integration
   ↓
6. Use in skill workflows
```

---

## MCP Catalog Structure

### Approved Catalogs

By default, MCP Provider only fetches from approved sources:

- **Official MCP Servers**: `https://github.com/modelcontextprotocol/servers`
- Add more in `config.json`

### Catalog Entry Format

```json
{
  "id": "postgresql-mcp",
  "name": "PostgreSQL MCP Server",
  "version": "1.0.0",
  "capabilities": ["sql_query", "schema_inspection"],
  "transport": "stdio",
  "docker_image": "mcp/postgresql:latest",
  "docs_url": "https://github.com/...",
  "security_notes": "Requires database credentials"
}
```

### Adding Custom Catalogs

Edit `.claude/skills/mcp-provider/config.json`:

```json
{
  "approved_sources": [
    "https://github.com/modelcontextprotocol/servers",
    "https://your-organization.com/mcp-catalog.json"
  ]
}
```

**Security Note**: Only add catalogs from trusted sources.

---

## Security Model

### Sandbox Levels

**Strict** (Default):
- Read-only root filesystem
- All capabilities dropped
- Network isolated
- Memory limited to 512MB

**Medium**:
- Limited write access to /tmp
- Network allowed for specific ports
- Some capabilities retained

**Permissive** (Use with caution):
- Normal filesystem access
- Full network access
- Standard capabilities

### Runtime Policies

Configure in `runtime_policy.json`:

```json
{
  "read_only_root": true,
  "drop_capabilities": ["ALL"],
  "add_capabilities": [],
  "network_mode": "none",
  "memory_limit": "512m",
  "cpu_quota": 50000,
  "pids_limit": 100
}
```

### Secret Management

**Never** commit secrets to git:

```bash
# .gitignore should include:
mcp_tools/*/.env
mcp_tools/*/secrets/
```

**Use environment files**:

```bash
# In mcp_tools/tool-name/.env
MCP_API_KEY=your-secret-key
MCP_DATABASE_URL=postgresql://...
```

**Or secrets management**:

```bash
# Using environment variables
export MCP_API_KEY=$(security find-generic-password -s mcp-key -w)
```

---

## API Reference

### Discovery

#### `discover_mcp.py`

```bash
# Basic search
python3 discover_mcp.py --search "database"

# List all tools
python3 discover_mcp.py --list-all

# Specific source
python3 discover_mcp.py --source "https://custom-catalog.com/mcp.json"

# JSON output
python3 discover_mcp.py --search "api" --json > results.json
```

**Output Format**:

```json
[
  {
    "id": "tool-id",
    "name": "Tool Name",
    "capabilities": ["cap1", "cap2"],
    "transport": "stdio",
    "docker_image": "registry/image:tag",
    "docs_url": "https://..."
  }
]
```

### Attachment

#### `attach_mcp.py`

```bash
# Basic attachment
python3 attach_mcp.py \
  --skill-path .claude/skills/my-skill \
  --mcp-id "postgresql-mcp"

# Custom tool name
python3 attach_mcp.py \
  --skill-path .claude/skills/my-skill \
  --mcp-id "postgresql-mcp" \
  --tool-name "db-tools"

# Without Docker
python3 attach_mcp.py \
  --skill-path .claude/skills/my-skill \
  --mcp-id "rest-api" \
  --no-docker
```

**Generated Files**:

```
.claude/skills/my-skill/mcp_tools/tool-name/
├── manifest.json         # Tool configuration
├── .env.example          # Environment template
├── docker_config.json    # Docker settings (optional)
└── README.md            # Usage instructions
```

### Testing

#### `test_mcp.py`

```bash
# Basic test
python3 test_mcp.py \
  --skill-path .claude/skills/my-skill \
  --tool-name "db-tools"

# Verbose output
python3 test_mcp.py \
  --skill-path .claude/skills/my-skill \
  --tool-name "db-tools" \
  --verbose

# JSON report
python3 test_mcp.py \
  --skill-path .claude/skills/my-skill \
  --tool-name "db-tools" \
  --json > test-report.json
```

**Test Coverage**:

- ✅ Directory structure
- ✅ Manifest validity
- ✅ Environment configuration
- ✅ Docker setup (if enabled)
- ✅ Security settings

---

## Docker Runtime

### Prerequisites

```bash
# Check Docker is installed
docker --version

# Check Docker is running
docker ps
```

### Image Management

```bash
# Pull MCP image
docker pull mcp/postgresql:latest

# List available images
docker images | grep mcp

# Remove unused images
docker rmi mcp/postgresql:old-version
```

### Runtime Configuration

Customize Docker execution in `docker_config.json`:

```json
{
  "image": "mcp/postgresql:latest",
  "runtime_policy": {
    "read_only": true,
    "drop_capabilities": ["ALL"],
    "network_mode": "none",
    "memory_limit": "512m",
    "cpu_quota": 50000
  },
  "environment": {
    "MCP_LOG_LEVEL": "info"
  },
  "volumes": {
    "/tmp": "rw"
  }
}
```

### Health Checks

MCP Provider runs health checks before activating tools:

```bash
# Manual health check
docker run --rm mcp/postgresql:latest --health-check

# Expected output:
# ✅ MCP server responding
# ✅ Protocol version: 1.0
# ✅ Capabilities: [sql_query, schema_inspection]
```

---

## Troubleshooting

### Common Issues

#### MCP Tool Not Found

**Symptom**: `discover_mcp.py` returns no results

**Solutions**:
1. Check tool ID spelling
2. Verify catalog source is approved
3. Clear cache: `rm -rf ~/.cache/mcp-provider`
4. Try different search terms

#### Docker Runtime Fails

**Symptom**: Error when running MCP tool

**Solutions**:
1. Check Docker is running: `docker ps`
2. Verify image exists: `docker images | grep mcp`
3. Check permissions: `docker run hello-world`
4. Review logs: `docker logs <container-id>`

#### Permission Denied

**Symptom**: MCP tool can't access resources

**Solutions**:
1. Check sandbox level in `manifest.json`
2. Adjust runtime policy (carefully)
3. Verify environment variables are set
4. Check file permissions in skill directory

#### Network Connection Failed

**Symptom**: MCP tool can't connect to external services

**Solutions**:
1. Check `network_mode` in Docker config
2. Adjust to `bridge` if external access needed
3. Configure firewall rules
4. Use VPN/proxy if required

### Debug Mode

Enable verbose logging:

```bash
# Set environment variable
export MCP_DEBUG=1

# Run scripts with debug output
python3 discover_mcp.py --search "test" 2>&1 | tee debug.log
```

### Getting Help

1. Check MCP tool documentation
2. Review GitHub issues: `https://github.com/modelcontextprotocol/servers/issues`
3. Test with minimal configuration
4. Create isolated reproduction case

---

## Best Practices

### Security

1. ✅ Always use strict sandbox for untrusted tools
2. ✅ Never commit `.env` files with secrets
3. ✅ Regularly update Docker images
4. ✅ Review MCP tool source code before use
5. ✅ Limit network access when possible

### Performance

1. ✅ Cache catalog data locally
2. ✅ Set appropriate memory limits
3. ✅ Use specific tool versions (not `latest`)
4. ✅ Clean up unused Docker images

### Maintenance

1. ✅ Document custom configurations
2. ✅ Test after MCP tool updates
3. ✅ Monitor Docker resource usage
4. ✅ Keep skill README updated

---

## Examples

### Example 1: Database Integration

```bash
# 1. Find database tools
python3 discover_mcp.py --search "postgresql"

# 2. Attach to skill
python3 attach_mcp.py \
  --skill-path .claude/skills/data-processor \
  --mcp-id "postgresql-mcp" \
  --tool-name "postgres"

# 3. Configure environment
cd .claude/skills/data-processor/mcp_tools/postgres
cp .env.example .env
# Edit .env with database credentials

# 4. Test integration
python3 test_mcp.py \
  --skill-path .claude/skills/data-processor \
  --tool-name "postgres"
```

### Example 2: API Integration

```bash
# 1. Find API tools
python3 discover_mcp.py --search "REST API"

# 2. Attach with minimal permissions
python3 attach_mcp.py \
  --skill-path .claude/skills/api-client \
  --mcp-id "rest-api-client" \
  --tool-name "api-tools"

# 3. Configure for external access
# Edit docker_config.json: "network_mode": "bridge"

# 4. Test
python3 test_mcp.py \
  --skill-path .claude/skills/api-client \
  --tool-name "api-tools" \
  --verbose
```

---

*For more information, see the main [SKILL.md](../SKILL.md) or visit the MCP documentation.*
