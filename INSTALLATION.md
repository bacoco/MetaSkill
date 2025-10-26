# EvolveSkill Installation Guide

Simple installation for the complete EvolveSkill package (Cortex + Synapse + Forge).

---

## Quick Install

### 1. Download

```bash
# Option A: Download latest release
wget https://github.com/bacoco/EvolveSkill/releases/latest/download/EvolveSkill.zip

# Option B: Clone repository
git clone https://github.com/bacoco/EvolveSkill.git
cd EvolveSkill
```

### 2. Install in Your Project

```bash
# Extract (if downloaded zip)
unzip EvolveSkill.zip

# Copy skills to your project
cp -r .claude/skills /path/to/your/project/.claude/

# Setup Cortex tracking
cd /path/to/your/project/.claude/skills/cortex/scripts
./install.sh
```

**Done!** EvolveSkill is now active in your project.

---

## What Just Happened?

1. **Cortex installed git hooks** - Automatically tracks your work on every commit
2. **Synapse ready** - Will analyze patterns when you run it
3. **Forge available** - Tools ready for creating custom skills

---

## Verify Installation

```bash
# Check git hook installed
ls -la /path/to/your/project/.git/hooks/post-commit

# Should show: .git/hooks/post-commit (executable)
```

Make a test commit:

```bash
git commit --allow-empty -m "Test Cortex tracking"

# Check if files were created
ls -la .cortex_handoff.md .cortex_log.md .cortex_status.json
```

If you see those files, Cortex is working!

---

## Using EvolveSkill

### With Your AI Assistant

Just start your AI assistant as usual:

```bash
claude          # or gpt, gemini, cursor, aider, etc.
```

Your assistant can now:
- Read `.cortex_handoff.md` for previous session context
- Access Cortex memory via Python API
- Use Synapse to analyze patterns
- Create custom skills with Forge

### Running Synapse

```bash
# Analyze patterns
python .claude/skills/synapse/scripts/synapse_analyzer.py

# Auto-generate skills from patterns
python .claude/skills/synapse/scripts/auto_skill_generator.py
```

### Creating Custom Skills

```bash
# Initialize new skill
python .claude/skills/forge/scripts/init_skill.py my-skill --path ./output

# Validate skill
python .claude/skills/forge/scripts/quick_validate.py ./output/my-skill

# Package skill
python .claude/skills/forge/scripts/package_skill.py ./output/my-skill
```

---

## Optional: Automatic Synapse Monitoring

Setup cron to run Synapse every 30 minutes:

```bash
crontab -e

# Add this line:
*/30 * * * * cd /path/to/your/project && python .claude/skills/synapse/scripts/auto_skill_generator.py
```

This makes EvolveSkill fully automatic - it will detect patterns and generate skills without manual intervention.

---

## Troubleshooting

### Cortex not tracking commits?

```bash
# Reinstall git hooks
cd .claude/skills/cortex/scripts
./install.sh

# Verify hook exists
ls -la /path/to/your/project/.git/hooks/post-commit
chmod +x /path/to/your/project/.git/hooks/post-commit
```

### Python import errors?

```bash
# Verify Python 3.9+
python3 --version

# Run scripts with full path
python3 /full/path/to/.claude/skills/synapse/scripts/synapse_analyzer.py
```

### Permission denied on scripts?

```bash
# Make all scripts executable
chmod +x .claude/skills/cortex/scripts/*.sh
chmod +x .claude/skills/cortex/scripts/*.py
chmod +x .claude/skills/synapse/scripts/*.py
chmod +x .claude/skills/forge/scripts/*.py
```

---

## Uninstallation

```bash
# Remove git hooks
rm /path/to/your/project/.git/hooks/post-commit

# Remove skills
rm -rf /path/to/your/project/.claude/skills

# Remove Cortex files (optional)
rm .cortex_handoff.md .cortex_log.md .cortex_status.json
```

---

## Next Steps

1. **Start coding** - Cortex tracks automatically
2. **Check handoff** - After first session, read `.cortex_handoff.md`
3. **Run Synapse** - After a few sessions, let it analyze patterns
4. **Create skills** - Use Forge for project-specific needs

---

**EvolveSkill** - Three skills working together to improve your AI coding workflow

For detailed documentation, see:
- [README.md](README.md) - Overview and usage
- [Cortex SKILL.md](.claude/skills/cortex/SKILL.md) - Memory system details
- [Synapse SKILL.md](.claude/skills/synapse/SKILL.md) - Pattern analyzer details
- [Forge SKILL.md](.claude/skills/forge/SKILL.md) - Skill creation guide
