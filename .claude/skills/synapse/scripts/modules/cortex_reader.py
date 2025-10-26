#!/usr/bin/env python3
"""
Cortex data reader for Synapse pattern detection
"""

import re
import json
import os
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from .data_models import SessionData
from .config_manager import ConfigManager


class CortexDataReader:
    """Reads and parses Cortex files"""

    def __init__(self, repo_root: str, config: ConfigManager):
        self.repo_root = Path(repo_root)
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Cortex file paths
        self.agent_log_path = self.repo_root / ".cortex_log.md"
        self.agent_status_path = self.repo_root / ".cortex_status.json"
        self.agent_handoff_path = self.repo_root / ".cortex_handoff.md"

    def read_all_cortex_data(self) -> Dict:
        """Read all Cortex files and return structured data"""
        data = {
            "sessions": [],
            "current_status": {},
            "handoff_info": {},
            "git_commits": []
        }

        try:
            # Read session logs
            if self.agent_log_path.exists():
                data["sessions"] = self.parse_agent_log()
            else:
                self.logger.warning(f"Agent log not found: {self.agent_log_path}")

            # Read current status
            if self.agent_status_path.exists():
                data["current_status"] = self.parse_agent_status()
            else:
                self.logger.warning(f"Agent status not found: {self.agent_status_path}")

            # Read handoff info
            if self.agent_handoff_path.exists():
                data["handoff_info"] = self.parse_agent_handoff()
            else:
                self.logger.warning(f"Agent handoff not found: {self.agent_handoff_path}")

            # Read Git commits
            data["git_commits"] = self.read_git_commits()

        except Exception as e:
            self.logger.error(f"Error reading Cortex data: {e}")

        return data

    def parse_agent_log(self) -> List[SessionData]:
        """Parse .cortex_log.md into structured session data"""
        sessions = []

        try:
            content: str
            try:
                size = self.agent_log_path.stat().st_size
            except Exception:
                size = 0

            max_bytes = self.config.get("analysis", "max_log_parse_bytes", default=2_000_000)
            sep = "=" * 80

            if size > max_bytes:
                # Read only the last max_bytes to avoid huge memory usage
                with open(self.agent_log_path, 'rb') as f:
                    f.seek(-max_bytes, os.SEEK_END)
                    data = f.read()
                content = data.decode('utf-8', errors='replace')
                # Align to the next full session separator if present
                idx = content.find(sep)
                if idx != -1:
                    content = content[idx:]
            else:
                with open(self.agent_log_path, 'r', encoding='utf-8') as f:
                    content = f.read()

            # Split by session separator
            session_blocks = content.split(sep)

            for block in session_blocks:
                if not block.strip():
                    continue

                session = self._parse_session_block(block)
                if session:
                    sessions.append(session)

            self.logger.info(f"Parsed {len(sessions)} sessions from agent log")

        except Exception as e:
            self.logger.error(f"Error parsing agent log: {e}")

        return sessions

    def _parse_session_block(self, block: str) -> Optional[SessionData]:
        """Parse a single session block from agent log"""
        try:
            # Extract timestamp
            timestamp_match = re.search(r'Session (\d{4}-\d{2}-\d{2}-\d{2}:\d{2})', block)
            timestamp = timestamp_match.group(1) if timestamp_match else ""

            # Extract agent
            agent_match = re.search(r'\*\*Agent\*\*: (.+)', block)
            agent = agent_match.group(1) if agent_match else ""

            # Extract repository
            repo_match = re.search(r'\*\*Repository\*\*: (.+)', block)
            repository = repo_match.group(1) if repo_match else ""

            # Extract file counts
            total_files = self._extract_number(block, r'\*\*Total Files\*\*: (\d+)')
            modified_files = self._extract_number(block, r'\*\*Modified\*\*: (\d+)')
            added_files = self._extract_number(block, r'\*\*Added\*\*: (\d+)')
            deleted_files = self._extract_number(block, r'\*\*Deleted\*\*: (\d+)')
            untracked_files = self._extract_number(block, r'\*\*Untracked\*\*: (\d+)')

            # Extract problems solved
            problems_solved = []
            problem_matches = re.findall(r'\*\*Fix\*\*: (.+)', block)
            problems_solved.extend(problem_matches)

            # Extract git status
            git_status_match = re.search(r'\*\*Git Status\*\*: (.+)', block)
            git_status = git_status_match.group(1) if git_status_match else ""

            # Extract branch
            branch_match = re.search(r'\*\*Branch\*\*: (.+)', block)
            branch = branch_match.group(1) if branch_match else "main"

            # Extract changed files
            changed_files = []
            changed_files_section = re.search(r'### Changed Files\n(.+?)(?:\n\n|\n##|$)', block, re.DOTALL)
            if changed_files_section:
                file_matches = re.findall(r'(?:Modified|Deleted|Added|Untracked): (.+?)(?:\n|,|\(and)', changed_files_section.group(1))
                changed_files.extend(file_matches)

            # Extract recent commits
            recent_commits = []
            commit_matches = re.findall(r'\*\*([a-f0-9]+)\*\*: (.+?) \((\d{4}-\d{2}-\d{2})\)', block)
            for commit_hash, message, date in commit_matches:
                recent_commits.append({
                    "hash": commit_hash,
                    "message": message,
                    "date": date
                })

            return SessionData(
                timestamp=timestamp,
                agent=agent,
                repository=repository,
                total_files=total_files,
                modified_files=modified_files,
                added_files=added_files,
                deleted_files=deleted_files,
                untracked_files=untracked_files,
                file_categories={},
                recent_commits=recent_commits,
                problems_solved=problems_solved,
                git_status=git_status,
                branch=branch,
                changed_files=changed_files
            )

        except Exception as e:
            self.logger.warning(f"Error parsing session block: {e}")
            return None

    def _extract_number(self, text: str, pattern: str) -> int:
        """Extract number from text using regex pattern"""
        match = re.search(pattern, text)
        return int(match.group(1)) if match else 0

    def parse_agent_status(self) -> Dict:
        """Parse .cortex_status.json"""
        try:
            with open(self.agent_status_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error parsing agent status: {e}")
            return {}

    def parse_agent_handoff(self) -> Dict:
        """Parse .cortex_handoff.md"""
        handoff_info = {}

        try:
            with open(self.agent_handoff_path, 'r') as f:
                content = f.read()

            # Extract project name
            project_match = re.search(r'\*\*Project\*\*: (.+)', content)
            handoff_info["project"] = project_match.group(1) if project_match else ""

            # Extract status
            status_match = re.search(r'\*\*Status\*\*: (.+)', content)
            handoff_info["status"] = status_match.group(1) if status_match else ""

            # Extract next steps
            next_steps = []
            steps_section = re.search(r'## 📋 Next Steps.*?\n(.*?)(?:\n##|$)', content, re.DOTALL)
            if steps_section:
                step_matches = re.findall(r'\d+\.\s+(.+)', steps_section.group(1))
                next_steps.extend(step_matches)
            handoff_info["next_steps"] = next_steps

            # Extract recent work
            recent_work_match = re.search(r'- Latest: (.+)', content)
            handoff_info["recent_work"] = recent_work_match.group(1) if recent_work_match else ""

        except Exception as e:
            self.logger.error(f"Error parsing agent handoff: {e}")

        return handoff_info

    def read_git_commits(self, limit: int = 50) -> List[Dict]:
        """Read recent Git commits"""
        commits = []

        try:
            result = subprocess.run(
                ["git", "log", f"-{limit}", "--pretty=format:%H|%an|%ae|%ad|%s"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if not line:
                        continue
                    parts = line.split('|')
                    if len(parts) == 5:
                        commits.append({
                            "hash": parts[0],
                            "author": parts[1],
                            "email": parts[2],
                            "date": parts[3],
                            "message": parts[4]
                        })

            self.logger.info(f"Read {len(commits)} Git commits")

        except Exception as e:
            self.logger.warning(f"Error reading Git commits: {e}")

        return commits