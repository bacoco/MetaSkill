#!/bin/bash
# Synapse Auto Watch - Monitors and auto-generates skills
# Usage:
# - Manually: ./synapse_auto_watch.sh
# - Via cron: */30 * * * * /path/to/.claude/skills/synapse/scripts/synapse_auto_watch.sh
# - Via git hook: add to .git/hooks/post-commit

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/synapse_auto_watch.log"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Synapse Auto Watch started" >> "$LOG_FILE"

# Run from repository root
cd "$SCRIPT_DIR/../../.."

if python3 ".claude/skills/synapse/scripts/auto_skill_generator.py" >> "$LOG_FILE" 2>&1; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Auto-generation completed" >> "$LOG_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Auto-generation failed" >> "$LOG_FILE"
fi
