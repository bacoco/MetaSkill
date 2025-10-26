"""Structured audit logging for the MCP Provider skill."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


@dataclass(slots=True)
class AuditLogger:
    """Minimal JSON lines audit logger."""

    logfile: Path

    def log(self, event: str, payload: Mapping[str, Any]) -> None:
        """Append an audit entry to the logfile."""

        if not event:
            raise ValueError("event must be provided")

        record = {
            "ts": datetime.now(tz=timezone.utc).isoformat(),
            "event": event,
            **dict(payload),
        }
        self.logfile.parent.mkdir(parents=True, exist_ok=True)
        with self.logfile.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
