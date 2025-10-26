# MetaSkill Installation Guide

Simple installation for the complete MetaSkill package (SOUL + NEXUS + skill-generator).

---

## Quick Install

### 1. Download

```bash
# Option A: Download latest release
wget https://github.com/bacoco/MetaSkill/releases/latest/download/MetaSkill.zip

# Option B: Clone repository
git clone https://github.com/bacoco/MetaSkill.git
cd MetaSkill
```

### 2. Install in Your Project

```bash
# Extract (if downloaded zip)
unzip MetaSkill.zip

# Copy skills to your project
cp -r .claude/skills /path/to/your/project/.claude/

# Setup SOUL tracking
cd /path/to/your/project/.claude/skills/soul/scripts
./install.sh
```

**Done!** MetaSkill is now active in your project.

---

## What Just Happened?

1. **SOUL installed git hooks** - Automatically tracks your work on every commit
2. **NEXUS ready** - Will analyze patterns when you run it
3. **skill-generator available** - Tools ready for creating custom skills

---

## Verify Installation

```bash
# Check git hook installed
ls -la /path/to/your/project/.git/hooks/post-commit

# Should show: .git/hooks/post-commit (executable)
```

Make a test commit:

```bash
git commit --allow-empty -m "Test SOUL tracking"

# Check if files were created
ls -la .agent_handoff.md .agent_log.md .agent_status.json
```

If you see those files, SOUL is working!

---

## Using MetaSkill

### With Your AI Assistant

Just start your AI assistant as usual:

```bash
claude          # or gpt, gemini, cursor, aider, etc.
```

Your assistant can now:
- Read `.agent_handoff.md` for previous session context
- Access SOUL memory via Python API
- Use NEXUS to analyze patterns
- Create custom skills with skill-generator

### Running NEXUS

```bash
# Analyze patterns
python .claude/skills/nexus/scripts/nexus_analyzer.py

# Auto-generate skills from patterns
python .claude/skills/nexus/scripts/auto_skill_generator.py
```

### Creating Custom Skills

```bash
# Initialize new skill
python .claude/skills/skill-generator/scripts/init_skill.py my-skill --path ./output

# Validate skill
python .claude/skills/skill-generator/scripts/quick_validate.py ./output/my-skill

# Package skill
python .claude/skills/skill-generator/scripts/package_skill.py ./output/my-skill
```

---

## Optional: Automatic NEXUS Monitoring

Setup cron to run NEXUS every 30 minutes:

```bash
crontab -e

# Add this line:
*/30 * * * * cd /path/to/your/project && python .claude/skills/nexus/scripts/auto_skill_generator.py
```

This makes MetaSkill fully automatic - it will detect patterns and generate skills without manual intervention.

---

## Troubleshooting

### SOUL not tracking commits?

```bash
# Reinstall git hooks
cd .claude/skills/soul/scripts
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
python3 /full/path/to/.claude/skills/nexus/scripts/nexus_analyzer.py
```

### Permission denied on scripts?

```bash
# Make all scripts executable
chmod +x .claude/skills/soul/scripts/*.sh
chmod +x .claude/skills/soul/scripts/*.py
chmod +x .claude/skills/nexus/scripts/*.py
chmod +x .claude/skills/skill-generator/scripts/*.py
```

---

## Uninstallation

```bash
# Remove git hooks
rm /path/to/your/project/.git/hooks/post-commit

# Remove skills
rm -rf /path/to/your/project/.claude/skills

# Remove SOUL files (optional)
rm .agent_handoff.md .agent_log.md .agent_status.json
```

---

## Next Steps

1. **Start coding** - SOUL tracks automatically
2. **Check handoff** - After first session, read `.agent_handoff.md`
3. **Run NEXUS** - After a few sessions, let it analyze patterns
4. **Create skills** - Use skill-generator for project-specific needs

---

**MetaSkill** - Three skills working together to improve your AI coding workflow

For detailed documentation, see:
- [README.md](README.md) - Overview and usage
- [SOUL SKILL.md](.claude/skills/soul/SKILL.md) - Memory system details
- [NEXUS SKILL.md](.claude/skills/nexus/SKILL.md) - Pattern analyzer details
- [skill-generator SKILL.md](.claude/skills/skill-generator/SKILL.md) - Skill creation guide
