# MetaSkill Installation Guide

Complete installation guide for SOUL, NEXUS, and skill-generator.

## Quick Install

### Option 1: Direct Copy (Recommended)

```bash
# Clone MetaSkill repository
git clone https://github.com/bacoco/MetaSkill.git
cd MetaSkill

# Copy skills to your project
cp -r .claude/skills /path/to/your/project/.claude/

# Install SOUL git hooks
cd /path/to/your/project/.claude/skills/soul/scripts
./install.sh
```

### Option 2: Git Submodule

```bash
cd /path/to/your/project

# Add MetaSkill as submodule
git submodule add https://github.com/bacoco/MetaSkill.git .metaskill

# Create symlink
ln -s .metaskill/.claude/skills .claude/skills

# Install SOUL git hooks
cd .claude/skills/soul/scripts
./install.sh
```

## Individual Skill Installation

### SOUL Installation

SOUL requires git hooks to automatically track your work:

```bash
# Navigate to SOUL scripts
cd /path/to/your/project/.claude/skills/soul/scripts

# Run installation script
./install.sh

# Verify installation
ls -la /path/to/your/project/.git/hooks/post-commit
```

**What the installation does:**
- Creates post-commit git hook
- Automatically traces sessions on each commit
- Generates `.agent_log.md`, `.agent_status.json`, `.agent_handoff.md`

### NEXUS Installation

NEXUS can run manually or automatically via cron:

**Manual Usage:**
```bash
# Analyze patterns and auto-generate skills
python .claude/skills/nexus/scripts/auto_skill_generator.py

# Analysis only (no generation)
python .claude/skills/nexus/scripts/nexus_analyzer.py
```

**Automatic Monitoring (Optional):**
```bash
# Add to crontab
crontab -e

# Add this line for every 30 minutes
*/30 * * * * /path/to/your/project/.claude/skills/scripts/nexus_auto_watch.sh
```

**Configuration (Optional):**
```bash
# Create config in your project root
cat > .nexus_config.json << 'EOF'
{
  "analysis": {
    "threshold": 5,
    "window_days": 7,
    "auto_threshold": "high"
  },
  "auto_generation": {
    "enabled": true,
    "max_skills_per_run": 5
  },
  "sources": {
    "soul_memory": true,
    "prd_files": true,
    "task_lists": true
  }
}
EOF
```

### skill-generator Installation

No installation required! Use the scripts directly:

```bash
# Initialize a new skill
python .claude/skills/skill-generator/scripts/init_skill.py my-skill --path ./output

# Validate a skill
python .claude/skills/skill-generator/scripts/quick_validate.py .claude/skills/my-skill

# Package a skill
python .claude/skills/skill-generator/scripts/package_skill.py .claude/skills/my-skill
```

## Requirements

### Python Dependencies

All skills require Python 3.9+:

```bash
# No external dependencies required for basic functionality
# SOUL and NEXUS use only Python standard library

# For development/validation (optional):
pip install pytest  # For running tests
```

### System Requirements

- **Git**: Required for SOUL git hooks
- **Bash**: Required for installation scripts (Linux/macOS)
- **Python 3.9+**: Required for all Python scripts
- **Cron**: Optional, for automatic NEXUS monitoring

## Verification

### Verify SOUL Installation

```bash
# Make a test commit
git commit --allow-empty -m "Test SOUL tracking"

# Check if files were created
ls -la .agent_handoff.md .agent_log.md .agent_status.json
```

### Verify NEXUS Installation

```bash
# Run analysis (dry-run mode)
python .claude/skills/nexus/scripts/auto_skill_generator.py --dry-run --verbose

# Check for recommendations file
cat NEXUS_RECOMMENDATIONS.md
```

### Verify skill-generator Installation

```bash
# Validate an existing skill
python .claude/skills/skill-generator/scripts/quick_validate.py .claude/skills/soul

# Should show validation results
```

## Uninstallation

### Remove SOUL Git Hooks

```bash
# Remove post-commit hook
rm /path/to/your/project/.git/hooks/post-commit

# Remove SOUL files (optional)
rm .agent_handoff.md .agent_log.md .agent_status.json
```

### Remove NEXUS Cron Job

```bash
# Edit crontab
crontab -e

# Remove the nexus_auto_watch.sh line
```

### Remove All Skills

```bash
# Remove skills directory
rm -rf .claude/skills

# Or remove symlink if using submodule
rm .claude/skills
```

## Troubleshooting

### SOUL Not Creating Files

**Problem:** `.agent_*` files are not being created

**Solution:**
```bash
# Reinstall git hooks
cd .claude/skills/soul/scripts
./install.sh

# Verify hook exists and is executable
ls -la /path/to/your/project/.git/hooks/post-commit
chmod +x /path/to/your/project/.git/hooks/post-commit
```

### NEXUS Not Finding Patterns

**Problem:** NEXUS doesn't detect any patterns

**Solution:**
```bash
# Ensure SOUL is working first
ls -la .agent_status.json

# Run NEXUS with verbose output
python .claude/skills/nexus/scripts/nexus_analyzer.py --verbose

# Lower the threshold temporarily
python .claude/skills/nexus/scripts/nexus_analyzer.py --threshold 1
```

### Permission Denied Errors

**Problem:** Scripts fail with permission errors

**Solution:**
```bash
# Make all scripts executable
chmod +x .claude/skills/soul/scripts/*.sh
chmod +x .claude/skills/soul/scripts/*.py
chmod +x .claude/skills/nexus/scripts/*.py
chmod +x .claude/skills/skill-generator/scripts/*.py
chmod +x .claude/skills/scripts/*.sh
```

### Python Import Errors

**Problem:** `ModuleNotFoundError` when running scripts

**Solution:**
```bash
# Verify Python version
python3 --version  # Should be 3.9+

# Check if scripts are being run from correct directory
cd /path/to/your/project
python3 .claude/skills/nexus/scripts/nexus_analyzer.py
```

## Next Steps

After installation:

1. **Start working** - SOUL will automatically track your work
2. **Check `.agent_handoff.md`** after each session for context
3. **Run NEXUS** periodically to discover skill opportunities
4. **Create custom skills** using skill-generator when needed

For more information, see individual skill documentation:
- [SOUL Documentation](.claude/skills/soul/SKILL.md)
- [NEXUS Documentation](.claude/skills/nexus/SKILL.md)
- [skill-generator Documentation](.claude/skills/skill-generator/SKILL.md)

---

**MetaSkill** - Professional skills for intelligent AI agents 🤖✨
