# MetaSkill - Universal AI Agent Skills

Three interdependent skills that work together to create a self-improving AI coding environment.

**Compatible with ALL AI coding assistants:** Claude Code, GPT, Gemini, Cursor, Aider, or any assistant that can read markdown and run Python.

---

## What's Included

### 🔮 SOUL - Universal Memory System
Automatically tracks all your work sessions via git hooks. Creates `.agent_handoff.md`, `.agent_log.md`, and `.agent_status.json` files that persist across sessions and enable seamless handoffs between different AI assistants.

**Key feature:** Your AI assistant always knows what was done previously.

---

### ⚡ NEXUS - Automatic Skill Generator
Monitors SOUL memory and automatically detects patterns in your work. When it sees you doing the same thing repeatedly (API calls, data processing, testing, etc.), it generates skill recommendations.

**Key feature:** Your workflow improves automatically based on actual usage.

---

### 🛠️ skill-generator - Skill Creation Tool
Tools and guides for creating new skills. Includes initialization scripts, validation, and packaging utilities.

**Key feature:** Easily create custom skills tailored to your project needs.

---

## Installation

**These three skills must be installed together** - they're interdependent.

### Quick Install

```bash
# Download latest release
wget https://github.com/bacoco/MetaSkill/releases/latest/download/MetaSkill.zip

# Extract
unzip MetaSkill.zip

# Copy to your project
cp -r .claude/skills /path/to/your/project/.claude/

# Setup SOUL tracking
cd /path/to/your/project/.claude/skills/soul/scripts
./install.sh
```

That's it! SOUL will automatically track your work, NEXUS will analyze patterns, and you can create custom skills with skill-generator.

### What Happens After Installation

1. **SOUL starts tracking** - Every git commit updates your session memory
2. **Check `.agent_handoff.md`** - Your AI assistant reads this for context
3. **NEXUS monitors** - Runs in background (optional cron setup)
4. **Skills improve your workflow** - Automatically over time

---

## Usage

### With Any AI Assistant

```bash
# Start your AI assistant
claude          # or gpt, gemini, cursor, aider, etc.

# Your assistant can now:
# - Read .agent_handoff.md for previous session context
# - Access SOUL memory via Python API
# - Use NEXUS recommendations to create new skills
```

### Running NEXUS Manually

```bash
# Analyze patterns and generate recommendations
python .claude/skills/nexus/scripts/nexus_analyzer.py

# Auto-generate high-priority skills
python .claude/skills/nexus/scripts/auto_skill_generator.py
```

### Creating Custom Skills

```bash
# Initialize new skill
python .claude/skills/skill-generator/scripts/init_skill.py my-skill --path ./output

# Validate
python .claude/skills/skill-generator/scripts/quick_validate.py .claude/skills/my-skill

# Package
python .claude/skills/skill-generator/scripts/package_skill.py .claude/skills/my-skill
```

---

## Documentation

Each skill includes detailed documentation:

- **SOUL**: [SKILL.md](.claude/skills/soul/SKILL.md) | [API Reference](.claude/skills/soul/references/API_REFERENCE.md) | [Workflows](.claude/skills/soul/references/WORKFLOWS.md)
- **NEXUS**: [SKILL.md](.claude/skills/nexus/SKILL.md) | [Examples](.claude/skills/nexus/references/EXAMPLES.md) | [Configuration](.claude/skills/nexus/references/CONFIGURATION.md)
- **skill-generator**: [SKILL.md](.claude/skills/skill-generator/SKILL.md) | [Workflows](.claude/skills/skill-generator/references/workflows.md)

---

## How It Works Together

```
You work normally
        ↓
SOUL tracks everything (git hooks)
        ↓
.agent_handoff.md updated
        ↓
Next session: AI reads handoff
        ↓
NEXUS analyzes patterns
        ↓
Recommends new skills
        ↓
Use skill-generator to create them
        ↓
Your workflow improves
```

---

## Troubleshooting

### SOUL not tracking?
```bash
cd .claude/skills/soul/scripts
./install.sh  # Reinstall git hooks
```

### NEXUS not finding patterns?
```bash
# Run with verbose output
python .claude/skills/nexus/scripts/nexus_analyzer.py --verbose
```

### Need help?
- Check individual SKILL.md files
- See detailed references/ directories
- Open an issue on GitHub

---

## License

[License details to be added]

---

## Contributing

Three skills, one ecosystem. Improvements to any skill benefit the whole system.

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**MetaSkill** - Self-improving skills for AI coding assistants

*Open source, LLM-agnostic, community-driven*
