# MetaSkill - Universal AI Agent Skills

Professional, production-ready skills for AI coding agents following progressive disclosure best practices.

## 🎯 Overview

MetaSkill is a collection of high-quality, reusable skills that extend AI agent capabilities. All skills are **LLM-agnostic** - they work with any AI coding assistant including Claude Code, GPT, Gemini, Cursor, Aider, and more.

Skills are pure markdown documentation + Python scripts - no vendor lock-in, no proprietary formats.

## 📦 Included Skills

### 🔮 SOUL - Session Orchestration & Universal Logging

**Score: 10/10**

Universal memory system that automatically tracks all sessions, enables agent handoffs, and provides inter-skill communication through persistent logs.

**Key Features:**
- Automatic session tracing via git hooks
- Agent handoff between sessions
- Python API for inter-skill communication
- Pattern detection for NEXUS
- Universal LLM support (works with all AI coding assistants)

**Documentation:**
- [SKILL.md](.claude/skills/soul/SKILL.md) - Quick start and overview (149 lines)
- [API_REFERENCE.md](.claude/skills/soul/references/API_REFERENCE.md) - Complete Python API
- [WORKFLOWS.md](.claude/skills/soul/references/WORKFLOWS.md) - 10 common usage patterns
- [MULTI_LLM.md](.claude/skills/soul/references/MULTI_LLM.md) - Cross-LLM integration guides

**Installation:**
```bash
cd .claude/skills/soul/scripts
./install.sh
```

---

### ⚡ NEXUS - Automatic Skill Generator

**Score: 10/10**

Unified analyzer that monitors SOUL memory, PRD files, and tasks to automatically generate skills based on detected patterns. The brain of the self-improving skills system.

**Key Features:**
- Automatic pattern detection from SOUL memory
- PRD and task list analysis
- Auto-generates skills when patterns reach threshold
- No user intervention required
- Multi-source pattern merging

**Documentation:**
- [SKILL.md](.claude/skills/nexus/SKILL.md) - Quick start and overview (231 lines)
- [EXAMPLES.md](.claude/skills/nexus/references/EXAMPLES.md) - 9 real-world scenarios
- [MANUAL_USAGE.md](.claude/skills/nexus/references/MANUAL_USAGE.md) - CLI reference
- [CONFIGURATION.md](.claude/skills/nexus/references/CONFIGURATION.md) - Complete config
- [ADVANCED.md](.claude/skills/nexus/references/ADVANCED.md) - Pattern merging, integrations
- [INSTALLATION.md](.claude/skills/nexus/references/INSTALLATION.md) - Setup guides
- [OUTPUT_FORMAT.md](.claude/skills/nexus/references/OUTPUT_FORMAT.md) - Recommendation format
- [MULTI_LLM.md](.claude/skills/nexus/references/MULTI_LLM.md) - Cross-LLM compatibility

**Quick Start:**
```bash
# Analyze patterns and auto-generate skills
python .claude/skills/nexus/scripts/auto_skill_generator.py

# Analysis only (no generation)
python .claude/skills/nexus/scripts/nexus_analyzer.py
```

---

### 🛠️ skill-generator - Official Skill Creation Tool

**Score: 10/10**

Official guide for creating effective skills that extends any AI agent's capabilities with specialized knowledge, workflows, or tool integrations.

**Key Features:**
- Complete skill creation workflow (6 steps)
- Progressive disclosure design patterns
- Skill validation and packaging
- Init scripts for quick setup
- Best practices and templates

**Documentation:**
- [SKILL.md](.claude/skills/skill-generator/SKILL.md) - Complete creation guide (356 lines)
- [workflows.md](.claude/skills/skill-generator/references/workflows.md) - Multi-step process patterns
- [output-patterns.md](.claude/skills/skill-generator/references/output-patterns.md) - Output quality patterns

**Quick Start:**
```bash
# Initialize a new skill
python .claude/skills/skill-generator/scripts/init_skill.py my-skill --path ./output

# Validate a skill
python .claude/skills/skill-generator/scripts/quick_validate.py .claude/skills/my-skill

# Package a skill
python .claude/skills/skill-generator/scripts/package_skill.py .claude/skills/my-skill
```

---

## 🏗️ Architecture

### The Self-Improving System

```
You work normally
        ↓
SOUL traces everything
        ↓
NEXUS monitors automatically
        ↓
Detects patterns >= threshold
        ↓
Auto-generates skills
        ↓
New skills ready immediately!
        ↓
AI assistant uses them
        ↓
New skills use SOUL API
        ↓
Pattern detection improves
        ↓
(cycle continues)
```

### Integration Flow

**SOUL** → Records all work patterns and events
**NEXUS** → Analyzes patterns and recommends skills
**Auto-generator** → Creates skills from recommendations
**Generated skills** → Use SOUL API to record their own patterns
**Improved detection** → Better skills over time

---

## 🚀 Quick Start

### 1. Install Skills

```bash
# Clone this repository
git clone https://github.com/bacoco/MetaSkill.git
cd MetaSkill

# Install in your project
cp -r .claude/skills /path/to/your/project/.claude/

# Setup SOUL
cd /path/to/your/project/.claude/skills/soul/scripts
./install.sh
```

### 2. Configure NEXUS (Optional)

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
  }
}
EOF
```

### 3. Setup Automatic Monitoring

```bash
# Add to crontab for every 30 minutes
crontab -e

# Add this line:
*/30 * * * * /path/to/your/project/.claude/skills/scripts/nexus_auto_watch.sh
```

### 4. Use with Your AI Assistant

```bash
# Start your preferred AI assistant (examples):
claude          # Claude Code
gpt             # OpenAI GPT
gemini          # Google Gemini
cursor          # Cursor AI
aider           # Aider

# SOUL will track your work
# NEXUS will analyze patterns
# Skills enhance your workflow
```

---

## 📊 Quality Standards

All skills in MetaSkill follow these standards:

✅ **Progressive Disclosure**: SKILL.md < 500 lines, details in references/
✅ **Complete Documentation**: API references, examples, workflows
✅ **Multi-LLM Support**: Works with Claude, GPT, Gemini, and more
✅ **Validation**: All skills pass skill-generator validation
✅ **Professional Code**: Clean, maintainable, well-commented
✅ **Comprehensive Testing**: Integration tests included

### Validation Scores

| Skill | SKILL.md Lines | Score | Status |
|-------|----------------|-------|--------|
| SOUL | 149 | 10/10 | ✅ Excellent |
| NEXUS | 231 | 10/10 | ✅ Good |
| skill-generator | 356 | 10/10 | ✅ Good |

---

## 🔧 Development

### Skill Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Main documentation (<500 lines)
├── scripts/ (optional)
│   └── *.py - Executable code
└── references/ (optional)
    └── *.md - Detailed documentation
```

### Validation

```bash
# Validate a skill (requires skill-generator)
python .claude/skills/skill-generator/scripts/quick_validate.py .claude/skills/soul

# Package a skill
python .claude/skills/skill-generator/scripts/package_skill.py .claude/skills/nexus
```

---

## 🤝 Contributing

We welcome contributions! To add or improve skills:

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/my-skill`
3. Follow progressive disclosure principles
4. Validate your skill
5. Submit a pull request

### Skill Requirements

- SKILL.md with proper YAML frontmatter
- Progressive disclosure (main doc < 500 lines)
- Complete references/ documentation
- Multi-LLM compatibility
- Passes validation

---

## 📖 Documentation

### SOUL Documentation

- [Quick Start](.claude/skills/soul/SKILL.md)
- [API Reference](.claude/skills/soul/references/API_REFERENCE.md)
- [Workflows](.claude/skills/soul/references/WORKFLOWS.md)
- [Multi-LLM](.claude/skills/soul/references/MULTI_LLM.md)

### NEXUS Documentation

- [Quick Start](.claude/skills/nexus/SKILL.md)
- [Examples](.claude/skills/nexus/references/EXAMPLES.md)
- [Manual Usage](.claude/skills/nexus/references/MANUAL_USAGE.md)
- [Configuration](.claude/skills/nexus/references/CONFIGURATION.md)
- [Advanced Features](.claude/skills/nexus/references/ADVANCED.md)
- [Installation](.claude/skills/nexus/references/INSTALLATION.md)
- [Output Format](.claude/skills/nexus/references/OUTPUT_FORMAT.md)
- [Multi-LLM](.claude/skills/nexus/references/MULTI_LLM.md)

### skill-generator Documentation

- [Complete Guide](.claude/skills/skill-generator/SKILL.md)
- [Workflow Patterns](.claude/skills/skill-generator/references/workflows.md)
- [Output Patterns](.claude/skills/skill-generator/references/output-patterns.md)
- [LICENSE](.claude/skills/skill-generator/LICENSE.txt)

---

## 🌐 Universal LLM Support

**All skills work identically across AI assistants.** Skills are markdown + Python - completely LLM-agnostic.

### ✅ Compatible With

- **Claude Code** - Full compatibility
- **GPT (OpenAI)** - Full compatibility
- **Gemini (Google)** - Full compatibility
- **Cursor** - Full compatibility
- **Aider** - Full compatibility
- **Any AI coding assistant** - If it can read markdown and run Python, it works!

### How Skills Work

1. **Read** - AI assistant reads SKILL.md (markdown documentation)
2. **Execute** - AI assistant runs scripts (Python) or follows workflows
3. **Track** - SOUL records work automatically via git hooks

No special integration needed. No vendor lock-in. Pure open formats.

### LLM-Specific Notes

Different AI assistants handle file reading differently:
- Some auto-read `.agent_handoff.md` at startup
- Others need explicit prompting: "Read .agent_handoff.md"
- All can access Python API identically

See [SOUL Multi-LLM Guide](.claude/skills/soul/references/MULTI_LLM.md) for specific setup instructions per assistant.

---

## 📦 Distribution

### Using in Your Project

**Option 1: Copy directly**
```bash
cp -r .claude/skills /path/to/your/project/.claude/
```

**Option 2: Git submodule**
```bash
cd /path/to/your/project
git submodule add https://github.com/bacoco/MetaSkill.git .metaskill
ln -s .metaskill/.claude/skills .claude/skills
```

**Option 3: Download release**
```bash
# Download latest release
wget https://github.com/bacoco/MetaSkill/releases/latest/download/skills.zip
unzip skills.zip -d .claude/
```

---

## 🐛 Troubleshooting

### SOUL Not Tracking

```bash
# Reinstall git hooks
cd .claude/skills/soul/scripts
./install.sh
```

### NEXUS Not Generating Skills

```bash
# Check configuration
cat .nexus_config.json

# Run in dry-run mode
python .claude/skills/nexus/scripts/auto_skill_generator.py --dry-run --verbose
```

### Permission Issues

```bash
# Make scripts executable
chmod +x .claude/skills/soul/scripts/*.py
chmod +x .claude/skills/nexus/scripts/*.py
chmod +x .claude/skills/scripts/*.sh
```

---

## 📄 License

[License details to be added]

---

## 🙏 Acknowledgments

- Built for the AI coding assistant ecosystem
- Follows progressive disclosure and skill design best practices
- Open source, LLM-agnostic, community-driven

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/bacoco/MetaSkill/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bacoco/MetaSkill/discussions)
- **Documentation**: See individual skill SKILL.md files

---

**MetaSkill** - Self-improving skills for intelligent AI agents 🤖✨

*Professional • Progressive • Powerful*
