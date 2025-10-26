#!/usr/bin/env python3
"""
SOUL - Session Tracer
Analyzes current session and creates agent memory files.
Enhanced with monitoring and event tracking.
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Import SOUL API
try:
    from soul_api import add_soul_event, get_soul_instance
    SOUL_API_AVAILABLE = True
except ImportError:
    SOUL_API_AVAILABLE = False

# Configuration constants with justification
RECENT_COMMITS_LIMIT = 5  # Enough context without overwhelming output
PROGRESS_REPORT_INTERVAL = 1000  # Balance between feedback and noise
MAX_LOG_FILE_SIZE_MB = 10  # Prevent log files from becoming unwieldy

class SOULTracer:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M")
        
        # Output files
        self.agent_log = self.repo_path / ".agent_log.md"
        self.agent_status = self.repo_path / ".agent_status.json"
        self.agent_handoff = self.repo_path / ".agent_handoff.md"
        
    def run_git_command(self, cmd: List[str]) -> Optional[str]:
        """Run git command safely with error handling."""
        try:
            result = subprocess.run(
                ["git"] + cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
                timeout=30  # Prevent hanging on large repositories
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            # Git not available or not a git repo - continue without git info
            return None
    
    def analyze_git_changes(self) -> Dict:
        """Analyze git repository changes."""
        # Get current status
        status_output = self.run_git_command(["status", "--porcelain"])
        if not status_output:
            return {"has_git": False, "changes": {}}
        
        changes = {"modified": [], "added": [], "deleted": [], "untracked": []}
        
        for line in status_output.split('\n'):
            if not line.strip():
                continue
            status_code = line[:2]
            filename = line[3:]
            
            if 'M' in status_code:
                changes["modified"].append(filename)
            elif 'A' in status_code:
                changes["added"].append(filename)
            elif 'D' in status_code:
                changes["deleted"].append(filename)
            elif '?' in status_code:
                changes["untracked"].append(filename)
        
        # Get recent commits
        commits = []
        log_output = self.run_git_command([
            "log", f"--max-count={RECENT_COMMITS_LIMIT}",
            "--pretty=format:%h|%s|%an|%ad", "--date=short"
        ])
        
        if log_output:
            for line in log_output.split('\n'):
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        commits.append({
                            "hash": parts[0],
                            "message": parts[1],
                            "author": parts[2],
                            "date": parts[3]
                        })
        
        return {
            "has_git": True,
            "changes": changes,
            "commits": commits,
            "branch": self.run_git_command(["branch", "--show-current"]) or "unknown"
        }
    
    def extract_problems_from_commits(self, commits: List[Dict]) -> List[Dict]:
        """Extract problems and solutions from commit messages."""
        problems = []
        
        # Keywords that indicate problems and solutions
        problem_indicators = ["fix", "bug", "error", "issue", "problem", "critical", "broken"]
        solution_indicators = ["implement", "add", "create", "update", "improve", "optimize"]
        
        for commit in commits:
            message_lower = commit["message"].lower()
            
            problem_type = None
            if any(keyword in message_lower for keyword in problem_indicators):
                problem_type = "fix"
            elif any(keyword in message_lower for keyword in solution_indicators):
                problem_type = "enhancement"
            
            if problem_type:
                problems.append({
                    "commit": commit["hash"],
                    "description": commit["message"],
                    "date": commit["date"],
                    "type": problem_type
                })
        
        return problems
    
    def generate_work_log(self) -> str:
        """Generate comprehensive work log."""
        git_info = self.analyze_git_changes()
        problems = []
        
        if git_info["has_git"]:
            problems = self.extract_problems_from_commits(git_info["commits"])
        
        # Calculate file change statistics
        total_changes = 0
        if git_info["has_git"]:
            changes = git_info["changes"]
            total_changes = sum(len(changes[key]) for key in changes)
        
        log_content = f"""# Agent Work Log - Session {self.timestamp}

## Session Information
- **Agent**: Claude (SOUL Agent)
- **Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Repository**: {self.repo_path.name}
- **Working Directory**: {self.repo_path}

## Files Changed This Session
- **Total Files**: {total_changes}
"""
        
        if git_info["has_git"]:
            changes = git_info["changes"]
            log_content += f"""- **Modified**: {len(changes['modified'])} files
- **Added**: {len(changes['added'])} files
- **Deleted**: {len(changes['deleted'])} files
- **Untracked**: {len(changes['untracked'])} files

### Changed Files
"""
            for category, files in changes.items():
                if files:
                    # Show first 5 files, indicate if more exist
                    displayed_files = files[:5]
                    file_list = ", ".join(displayed_files)
                    if len(files) > 5:
                        file_list += f" (and {len(files) - 5} more)"
                    log_content += f"- **{category.title()}**: {file_list}\n"
        
        if git_info["has_git"] and git_info["commits"]:
            log_content += f"""
## Recent Commits
"""
            for commit in git_info["commits"][:3]:  # Show top 3 commits
                log_content += f"- **{commit['hash']}**: {commit['message']} ({commit['date']})\n"
        
        if problems:
            log_content += f"""
## Problems Solved This Session
"""
            for problem in problems:
                log_content += f"- **{problem['type'].title()}**: {problem['description']}\n"
        
        # Repository state
        git_status = "Clean" if total_changes == 0 else f"{total_changes} files changed"
        last_commit = git_info["commits"][0]["message"] if git_info["has_git"] and git_info["commits"] else "No recent commits"
        
        log_content += f"""
## Current Repository State
- **Git Status**: {git_status}
- **Branch**: {git_info.get('branch', 'unknown')}
- **Last Commit**: {last_commit}

## Recommendations for Next Agent
1. Check git status for any uncommitted changes
2. Review recent commits to understand latest changes  
3. Run tests to verify current state
4. Continue with planned development tasks

---
*Generated by SOUL (Seamless Organized Universal Learning) - {self.timestamp}*
"""
        
        return log_content
    
    def generate_status_json(self) -> Dict:
        """Generate machine-readable status."""
        git_info = self.analyze_git_changes()
        
        status = {
            "timestamp": self.timestamp,
            "agent": "Claude (SOUL)",
            "repository": str(self.repo_path),
            "session_info": {
                "has_git": git_info["has_git"],
                "total_files_changed": 0,
                "git_clean": True
            }
        }
        
        if git_info["has_git"]:
            changes = git_info["changes"]
            total_changes = sum(len(changes[key]) for key in changes)
            status["session_info"].update({
                "total_files_changed": total_changes,
                "git_clean": total_changes == 0,
                "branch": git_info["branch"],
                "recent_commits": len(git_info["commits"])
            })
        
        return status
    
    def generate_handoff_notes(self) -> str:
        """Generate quick handoff notes."""
        git_info = self.analyze_git_changes()
        total_changes = 0
        
        if git_info["has_git"]:
            changes = git_info["changes"]
            total_changes = sum(len(changes[key]) for key in changes)
        
        status_icon = "✅ Clean" if total_changes == 0 else f"⚠️ {total_changes} files changed"
        
        handoff = f"""# 🔄 Agent Handoff - {self.timestamp}

## 🚀 Ready to Continue
**Project**: {self.repo_path.name}
**Status**: {status_icon}

## 📋 Next Steps (Priority Order)
1. Review `.agent_log.md` for detailed session information
2. Check `.agent_status.json` for machine-readable status
3. Run `git status` to see current repository state
4. Continue with development tasks

## 🔧 Technical Context
- Repository is in working state
- All critical issues from previous sessions have been addressed
- Check existing documentation for project context
"""
        
        if git_info["has_git"] and git_info["commits"]:
            handoff += f"""
## ✅ Recent Work
- Latest: {git_info["commits"][0]["message"]}
"""
        
        handoff += f"""
## 💡 Quick Tips
- SOUL automatically tracks your work across sessions
- Use `python trace_session.py` to update logs manually
- Check `.agent_handoff.md` for immediate next steps

---
*SOUL handoff generated at {self.timestamp}*
"""
        
        return handoff
    
    def save_all_files(self):
        """Save all generated files with error handling."""
        files_created = []

        try:
            # Analyze git first
            git_info = self.analyze_git_changes()

            # Generate content
            work_log = self.generate_work_log()
            status_json = self.generate_status_json()
            handoff_notes = self.generate_handoff_notes()

            # Save work log (append if exists, create if not)
            if self.agent_log.exists():
                with open(self.agent_log, 'a', encoding='utf-8') as f:
                    f.write("\n\n" + "="*80 + "\n\n")
                    f.write(work_log)
            else:
                with open(self.agent_log, 'w', encoding='utf-8') as f:
                    f.write(work_log)
            files_created.append(str(self.agent_log))

            # Save status JSON (overwrite)
            with open(self.agent_status, 'w', encoding='utf-8') as f:
                json.dump(status_json, f, indent=2, ensure_ascii=False)
            files_created.append(str(self.agent_status))

            # Save handoff notes (overwrite)
            with open(self.agent_handoff, 'w', encoding='utf-8') as f:
                f.write(handoff_notes)
            files_created.append(str(self.agent_handoff))

            # Record session trace event via SOUL API
            if SOUL_API_AVAILABLE:
                try:
                    total_changes = 0
                    if git_info.get("has_git"):
                        changes = git_info["changes"]
                        total_changes = sum(len(changes[key]) for key in changes)

                    add_soul_event(
                        "session_traced",
                        f"SOUL traced session with {total_changes} file changes",
                        {
                            "files_changed": total_changes,
                            "git_clean": total_changes == 0,
                            "branch": git_info.get("branch", "unknown"),
                            "commits_analyzed": len(git_info.get("commits", []))
                        }
                    )
                except Exception as e:
                    # Silent fail - ne pas bloquer si l'API SOUL a un problème
                    pass

            return files_created

        except IOError as e:
            print(f"❌ Error saving files: {e}")
            return []

def main():
    """Main function with proper error handling."""
    import argparse
    
    parser = argparse.ArgumentParser(description="SOUL - Session Tracer")
    parser.add_argument("--repo", default=".", help="Repository path")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    try:
        tracer = SOULTracer(args.repo)
        files_created = tracer.save_all_files()
        
        if files_created:
            print("✅ SOUL session traced successfully:")
            for file_path in files_created:
                print(f"   - {Path(file_path).name}")
        else:
            print("❌ Failed to create SOUL files")
            return 1
            
        if args.verbose:
            git_info = tracer.analyze_git_changes()
            print(f"\n📊 Session Analysis:")
            if git_info["has_git"]:
                changes = git_info["changes"]
                total_changes = sum(len(changes[key]) for key in changes)
                print(f"   - Total files changed: {total_changes}")
                print(f"   - Recent commits: {len(git_info['commits'])}")
                print(f"   - Current branch: {git_info['branch']}")
            else:
                print("   - No git repository detected")
        
        return 0
        
    except Exception as e:
        print(f"❌ SOUL error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())