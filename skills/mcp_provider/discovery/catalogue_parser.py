"""Streaming helpers for parsing MCP catalogues.

The final parsing logic will convert llms.txt style catalogues into structured
:class:`~skills.mcp_provider.provider_api.Candidate` objects. For now we expose a
lightweight placeholder that documents the expected behaviour and raises
``NotImplementedError`` to signal the missing implementation.
"""
from __future__ import annotations

from collections.abc import Iterable
from io import TextIOBase
from typing import Iterator

from skills.mcp_provider.provider_api import Candidate


def parse_catalogue_stream(stream: TextIOBase) -> Iterator[Candidate]:
    """Parse a textual catalogue stream into candidate entries.

    Parameters
    ----------
    stream:
        A text file-like object. Implementations must support large files via
        streaming without loading the entire content into memory.
    """

    raise NotImplementedError("Catalogue parsing is not implemented yet.")


def normalize_entries(entries: Iterable[dict]) -> Iterator[Candidate]:
    """Normalize raw dictionary entries into :class:`Candidate` instances."""

    raise NotImplementedError("Catalogue normalization is not implemented yet.")
