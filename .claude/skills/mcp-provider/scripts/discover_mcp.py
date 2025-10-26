#!/usr/bin/env python3
"""
MCP Discovery Script - Find MCP tools from approved catalogs

Usage:
    python3 discover_mcp.py --search "database tools"
    python3 discover_mcp.py --list-all
    python3 discover_mcp.py --source "https://github.com/modelcontextprotocol/servers"
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any


DEFAULT_SOURCES = [
    "https://github.com/modelcontextprotocol/servers",
]


def load_config() -> Dict[str, Any]:
    """Load MCP provider configuration"""
    config_path = Path(__file__).parent.parent / "config.json"

    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)

    # Default configuration
    return {
        "approved_sources": DEFAULT_SOURCES,
        "max_candidates": 10,
        "cache_enabled": True
    }


def discover_mcp_tools(search_query: str = None, source: str = None) -> List[Dict[str, Any]]:
    """
    Discover MCP tools from approved catalogs

    Args:
        search_query: Optional search term to filter results
        source: Specific catalog source to search

    Returns:
        List of discovered MCP tool candidates
    """
    config = load_config()
    sources = [source] if source else config.get("approved_sources", DEFAULT_SOURCES)

    print(f"🔍 Searching MCP catalogs...")
    print(f"   Sources: {len(sources)}")
    if search_query:
        print(f"   Query: '{search_query}'")
    print()

    # In a real implementation, this would fetch from GitHub/catalogs
    # For now, return example data
    candidates = [
        {
            "id": "postgresql-mcp",
            "name": "PostgreSQL MCP Server",
            "capabilities": ["sql_query", "schema_inspection", "data_export"],
            "transport": "stdio",
            "docker_image": "mcp/postgresql:latest",
            "docs_url": "https://github.com/modelcontextprotocol/servers/tree/main/postgresql",
            "source": sources[0]
        },
        {
            "id": "rest-api-client",
            "name": "REST API Client MCP",
            "capabilities": ["http_request", "api_discovery", "auth_management"],
            "transport": "stdio",
            "docker_image": "mcp/rest-api:latest",
            "docs_url": "https://github.com/modelcontextprotocol/servers/tree/main/rest-api",
            "source": sources[0]
        }
    ]

    # Filter by search query if provided
    if search_query:
        query_lower = search_query.lower()
        candidates = [
            c for c in candidates
            if query_lower in c["name"].lower() or
               query_lower in " ".join(c["capabilities"]).lower()
        ]

    return candidates


def print_candidates(candidates: List[Dict[str, Any]]):
    """Pretty print discovered candidates"""
    if not candidates:
        print("❌ No MCP tools found matching your criteria")
        return

    print(f"✅ Found {len(candidates)} MCP tool(s):\n")

    for i, candidate in enumerate(candidates, 1):
        print(f"{i}. {candidate['name']} ({candidate['id']})")
        print(f"   Capabilities: {', '.join(candidate['capabilities'])}")
        print(f"   Transport: {candidate['transport']}")
        if candidate.get('docker_image'):
            print(f"   Docker: {candidate['docker_image']}")
        print(f"   Docs: {candidate['docs_url']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Discover MCP tools from approved catalogs"
    )
    parser.add_argument(
        "--search",
        help="Search query to filter results"
    )
    parser.add_argument(
        "--source",
        help="Specific catalog source URL"
    )
    parser.add_argument(
        "--list-all",
        action="store_true",
        help="List all available MCP tools"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    # Discover MCP tools
    candidates = discover_mcp_tools(
        search_query=args.search,
        source=args.source
    )

    # Output results
    if args.json:
        print(json.dumps(candidates, indent=2))
    else:
        print_candidates(candidates)

    return 0


if __name__ == "__main__":
    sys.exit(main())
