# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MetaSkill is a self-improving AI workflow system consisting of three interdependent skills:
- **SOUL**: Universal memory system (git hooks, session tracking, agent handoffs)
- **NEXUS**: Pattern detector and automatic skill generator
- **skill-generator**: Tools for creating new skills

These three skills work together in a loop: SOUL tracks work → NEXUS detects patterns → skill-generator creates automations → cycle repeats.

## Important: Three-Skill Package Philosophy

**All three skills MUST be distributed together.** They are interdependent:
- SOUL provides the data NEXUS analyzes
- NEXUS uses skill-generator templates to create new skills
- Generated skills use SOUL API to record events

Do not split them into separate packages. The single MetaSkill.zip contains all three.

## Build and Package Commands

### Building Distribution
```bash
# Package MetaSkill (creates dist/MetaSkill-v{VERSION}.zip)
./package_metaskill.sh [VERSION]

# Default version is 1.0.0
./package_metaskill.sh
```

This creates a single universal zip containing:
- `.claude/skills/soul/`
- `.claude/skills/nexus/`
- `.claude/skills/skill-generator/`
- README.md, INSTALLATION.md, .gitignore

### Testing Installation Locally
```bash
# Install in a test project
cd /path/to/test-project
unzip /path/to/MetaSkill/dist/MetaSkill-v*.zip
cd .claude/skills/soul/scripts
./install.sh

# Verify SOUL tracking
git commit --allow-empty -m "Test commit"
ls -la .agent_handoff.md .agent_log.md .agent_status.json
```

### Individual Skill Scripts

**SOUL:**
```bash
# Install git hooks
.claude/skills/soul/scripts/install.sh

# Manual session tracing
python3 .claude/skills/soul/scripts/trace_session.py

# Manual handoff generation
python3 .claude/skills/soul/scripts/handoff_generator.py
```

**NEXUS:**
```bash
# Analyze patterns (creates NEXUS_RECOMMENDATIONS.md)
python .claude/skills/nexus/scripts/nexus_analyzer.py

# Auto-generate skills from patterns
python .claude/skills/nexus/scripts/auto_skill_generator.py
```

**skill-generator:**
```bash
# Initialize new skill
python .claude/skills/skill-generator/scripts/init_skill.py <skill-name> --path <output-dir>

# Validate skill
python .claude/skills/skill-generator/scripts/quick_validate.py <path/to/skill>

# Package skill
python .claude/skills/skill-generator/scripts/package_skill.py <path/to/skill> [output-dir]
```

## Architecture

### Directory Structure
```
.claude/skills/
├── soul/
│   ├── SKILL.md                    # Main skill documentation
│   ├── scripts/
│   │   ├── soul_api.py             # Python API for inter-skill communication
│   │   ├── trace_session.py        # Updates .agent_log.md and .agent_status.json
│   │   ├── handoff_generator.py    # Creates .agent_handoff.md
│   │   └── install.sh              # Sets up git hooks
│   └── references/
│       ├── API_REFERENCE.md        # Complete API documentation
│       ├── WORKFLOWS.md            # Common usage patterns
│       └── MULTI_LLM.md            # Non-Claude LLM integration
├── nexus/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── nexus_analyzer.py       # Analyzes SOUL data for patterns
│   │   ├── auto_skill_generator.py # Auto-generates skills from patterns
│   │   ├── prd_analyzer.py         # Extracts patterns from PRD files
│   │   ├── pattern_detector.py     # Core pattern detection logic
│   │   └── soul_integration.py     # SOUL API integration
│   └── references/
│       ├── EXAMPLES.md             # Real-world examples
│       ├── CONFIGURATION.md        # Config reference
│       ├── ADVANCED.md             # Pattern merging, customization
│       └── OUTPUT_FORMAT.md        # NEXUS_RECOMMENDATIONS.md format
└── skill-generator/
    ├── SKILL.md
    └── scripts/
        ├── init_skill.py           # Generate skill template
        ├── quick_validate.py       # Validate skill structure
        └── package_skill.py        # Create .skill zip file
```

### SOUL Memory Files (Generated)

SOUL creates three files in project roots (NOT in this repo):
- `.agent_log.md` - Detailed session history
- `.agent_status.json` - Machine-readable state
- `.agent_handoff.md` - Quick context for next session

These are in `.gitignore` but users may choose to commit them for team collaboration.

### NEXUS Output Files (Generated)

NEXUS creates in project roots (NOT in this repo):
- `NEXUS_RECOMMENDATIONS.md` - Prioritized skill recommendations

### The Self-Improving Loop

```
User codes normally
    ↓
SOUL tracks via git hooks → Updates .agent_log.md, .agent_status.json
    ↓
User or cron runs NEXUS → Analyzes SOUL data
    ↓
NEXUS detects patterns (≥5 occurrences) → Creates NEXUS_RECOMMENDATIONS.md
    ↓
User or NEXUS auto-generates skills → Uses skill-generator templates
    ↓
New skills use SOUL API → Record their own events
    ↓
Better data for NEXUS → Cycle continues
```

## Key Design Principles

### Progressive Disclosure
Skills use three-level loading:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words, <500 lines)
3. **Bundled resources** - Loaded as needed (unlimited)

When SKILL.md approaches 500 lines, split content into `references/`.

### Skill Structure
```
skill-name/
├── SKILL.md              # Required: YAML frontmatter + markdown instructions
├── scripts/              # Optional: Executable code (Python/Bash)
├── references/           # Optional: Documentation loaded as needed
└── assets/               # Optional: Files used in output (templates, etc.)
```

### What NOT to Include
Do not create auxiliary documentation:
- No README.md (SKILL.md is sufficient)
- No INSTALLATION_GUIDE.md
- No CHANGELOG.md
- No QUICK_REFERENCE.md

Skills are for AI agents, not human end-users.

## Development Practices

### When Editing Skills

1. **Keep SKILL.md concise** - Under 500 lines, prefer examples over explanations
2. **Test scripts by running them** - Don't just write code and assume it works
3. **Use progressive disclosure** - Split long content into `references/`
4. **Include clear when-to-use guidance** - Description field is critical for skill selection
5. **Validate before packaging** - `package_skill.py` auto-validates

### When Creating New Skills

Follow skill-generator's 6-step process:
1. Understand with concrete examples
2. Plan reusable contents (scripts/references/assets)
3. Initialize (`init_skill.py`)
4. Edit (implement resources, write SKILL.md)
5. Package (`package_skill.py`)
6. Iterate based on real usage

### Python Conventions

- All scripts use Python 3.9+
- SOUL API import: `from soul_api import add_soul_event, get_soul_memory, get_pattern_analysis`
- No external dependencies (uses stdlib only)
- Scripts are standalone executables

### Shell Script Conventions

- Use `#!/bin/bash`
- Include `set -e` for error handling
- Provide clear echo messages for user feedback
- Check working directory before critical operations

## Multi-LLM Compatibility

MetaSkill works with any CLI-based AI assistant:
- Claude Code (native)
- GPT/Codex
- Gemini CLI
- Cursor
- Aider

All skills use universal formats (markdown, JSON) and avoid Claude-specific features.

## Common Tasks

### Add New Functionality to SOUL
1. Edit `.claude/skills/soul/scripts/soul_api.py` or related script
2. Update `.claude/skills/soul/references/API_REFERENCE.md` if API changes
3. Test by running script directly
4. No need to repackage MetaSkill unless releasing new version

### Add New Pattern Detection to NEXUS
1. Edit `.claude/skills/nexus/scripts/pattern_detector.py`
2. Update threshold logic or pattern types
3. Test with real SOUL data (create test commits)
4. Document in `.claude/skills/nexus/references/ADVANCED.md`

### Create New Skill Template
1. Edit `.claude/skills/nexus/scripts/enhanced_skill_templates.py`
2. Add template following existing pattern structure
3. Test by running `auto_skill_generator.py` to trigger generation
4. Validate generated skill with `quick_validate.py`

### Release New Version
1. Update version number in `package_metaskill.sh` call
2. Run `./package_metaskill.sh X.Y.Z`
3. Test installation in clean project
4. Create GitHub release with dist/MetaSkill-vX.Y.Z.zip

## Testing Workflow

Since this is a meta-framework, testing requires a real project:

```bash
# 1. Setup test project
mkdir /tmp/test-project
cd /tmp/test-project
git init

# 2. Install MetaSkill
unzip /path/to/MetaSkill/dist/MetaSkill-v*.zip
cd .claude/skills/soul/scripts
./install.sh
cd /tmp/test-project

# 3. Test SOUL tracking
git commit --allow-empty -m "Test commit"
cat .agent_handoff.md  # Should show session summary

# 4. Create test pattern (repeat 5+ times)
for i in {1..6}; do
  echo "Test API call" >> test.txt
  git add test.txt
  git commit -m "API call test $i"
done

# 5. Test NEXUS detection
python /path/to/MetaSkill/.claude/skills/nexus/scripts/nexus_analyzer.py
cat NEXUS_RECOMMENDATIONS.md  # Should show pattern recommendation

# 6. Test auto-generation
python /path/to/MetaSkill/.claude/skills/nexus/scripts/auto_skill_generator.py
ls .claude/skills/  # Should see generated skill if pattern was HIGH/CRITICAL
```

## Files to Never Commit (Already in .gitignore)

- `__pycache__/`, `*.pyc` - Python cache
- `.DS_Store`, `Thumbs.db` - OS artifacts
- `NEXUS_RECOMMENDATIONS.md` - Generated output
- `.agent_*` files - SOUL memory (user decision whether to commit)
- `dist/*.skill`, `dist/*.zip` - Build artifacts (commit to releases, not main branch)

## Documentation Standards

- Use imperative mood in SKILL.md ("Use this", not "This is used")
- Keep descriptions specific and include trigger keywords
- YAML frontmatter: only `name` and `description` fields
- Reference files from SKILL.md with clear when-to-read guidance
- Table of contents for reference files >100 lines
