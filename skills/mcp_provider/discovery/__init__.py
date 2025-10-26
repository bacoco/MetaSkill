"""Discovery utilities for the MCP Provider skill."""

from .catalogue_parser import parse_catalogue_stream
from .sources import resolve_sources

__all__ = ["parse_catalogue_stream", "resolve_sources"]
