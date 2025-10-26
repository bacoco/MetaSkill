# MetaSkill - Universal Claude Code Skills Repository

Professional, production-ready skills for Claude Code following progressive disclosure best practices.

## 🎯 Overview

MetaSkill is a collection of high-quality, reusable skills that extend Claude Code's capabilities. All skills follow professional standards with progressive disclosure documentation and achieve 10/10 quality ratings.

## 📦 Included Skills

### 🔮 SOUL - Session Orchestration & Universal Logging

**Score: 10/10**

Universal memory system that automatically tracks all sessions, enables agent handoffs, and provides inter-skill communication through persistent logs.

**Key Features:**
- Automatic session tracing via git hooks
- Agent handoff between sessions
- Python API for inter-skill communication
- Pattern detection for NEXUS
- Multi-LLM support (Claude, GPT, Gemini, Cursor, Aider)

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
Claude uses them automatically
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

### 4. Use with Claude Code

```bash
# Claude automatically loads skills from .claude/skills/
claude

# SOUL will track your work
# NEXUS will analyze patterns
# Skills will be generated automatically
```

---

## 📊 Quality Standards

All skills in MetaSkill follow these standards:

✅ **Progressive Disclosure**: SKILL.md < 500 lines, details in references/
✅ **Complete Documentation**: API references, examples, workflows
✅ **Multi-LLM Support**: Works with Claude, GPT, Gemini, and more
✅ **Validation**: All skills pass skill-creator validation
✅ **Professional Code**: Clean, maintainable, well-commented
✅ **Comprehensive Testing**: Integration tests included

### Validation Scores

| Skill | SKILL.md Lines | Score | Status |
|-------|----------------|-------|--------|
| SOUL | 149 | 10/10 | ✅ Excellent |
| NEXUS | 231 | 10/10 | ✅ Good |

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
# Validate a skill (requires skill-creator)
python .claude/skills/skill-creator/scripts/quick_validate.py .claude/skills/soul

# Package a skill
python .claude/skills/skill-creator/scripts/package_skill.py .claude/skills/nexus
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

---

## 🌐 Multi-LLM Support

These skills work with multiple LLM platforms:

| Feature | Claude Code | GPT CLI | Gemini CLI | Cursor | Aider |
|---------|-------------|---------|------------|--------|-------|
| SOUL memory | ✅ Full | ⚠️ API only | ⚠️ API only | ❌ No | ⚠️ API only |
| NEXUS analysis | ✅ Auto | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ⚠️ Semi |
| Auto skill generation | ✅ Full | ❌ No | ❌ No | ❌ No | ⚠️ Semi |
| Skill loading | ✅ Auto | ❌ No | ❌ No | ❌ No | ❌ No |

See individual skill documentation for LLM-specific guides.

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

- Built for [Claude Code](https://claude.com/claude-code)
- Follows [Claude Skills best practices](https://docs.claude.com/)
- Generated and validated with Claude AI

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/bacoco/MetaSkill/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bacoco/MetaSkill/discussions)
- **Documentation**: See individual skill SKILL.md files

---

**MetaSkill** - Self-improving skills for intelligent AI agents 🤖✨

*Professional • Progressive • Powerful*
