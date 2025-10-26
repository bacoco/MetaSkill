# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EvolveSkill is a self-improving AI workflow system consisting of three interdependent skills:
- **Cortex**: Universal memory system (git hooks, session tracking, agent handoffs)
- **Synapse**: Pattern detector and automatic skill generator
- **Forge**: Tools for creating new skills

These three skills work together in a loop: Cortex tracks work → Synapse detects patterns → Forge creates automations → cycle repeats.

## Important: Three-Skill Package Philosophy

**All three skills MUST be distributed together.** They are interdependent:
- Cortex provides the data Synapse analyzes
- Synapse uses Forge templates to create new skills
- Generated skills use Cortex API to record events

Do not split them into separate packages. The single EvolveSkill.zip contains all three.

## Build and Package Commands

### Building Distribution
```bash
# Package EvolveSkill (creates dist/EvolveSkill-v{VERSION}.zip)
./package_evolveskill.sh [VERSION]

# Default version is 2.0.0
./package_evolveskill.sh
```

This creates a single universal zip containing:
- `.claude/skills/cortex/`
- `.claude/skills/synapse/`
- `.claude/skills/forge/`
- README.md, INSTALLATION.md, .gitignore

### Testing Installation Locally
```bash
# Install in a test project
cd /path/to/test-project
unzip /path/to/EvolveSkill/dist/EvolveSkill-v*.zip
cd .claude/skills/cortex/scripts
./install.sh

# Verify Cortex tracking
git commit --allow-empty -m "Test commit"
ls -la .cortex_handoff.md .cortex_log.md .cortex_status.json
```

### Individual Skill Scripts

**Cortex:**
```bash
# Install git hooks
.claude/skills/cortex/scripts/install.sh

# Manual session tracing
python3 .claude/skills/cortex/scripts/trace_session.py

# Manual handoff generation
python3 .claude/skills/cortex/scripts/handoff_generator.py
```

**Synapse:**
```bash
# Analyze patterns (creates Synapse_RECOMMENDATIONS.md)
python .claude/skills/synapse/scripts/synapse_analyzer.py

# Auto-generate skills from patterns
python .claude/skills/synapse/scripts/auto_skill_generator.py
```

**Forge:**
```bash
# Initialize new skill
python .claude/skills/forge/scripts/init_skill.py <skill-name> --path <output-dir>

# Validate skill
python .claude/skills/forge/scripts/quick_validate.py <path/to/skill>

# Package skill
python .claude/skills/forge/scripts/package_skill.py <path/to/skill> [output-dir]
```

## Architecture

### Directory Structure
```
.claude/skills/
├── cortex/
│   ├── SKILL.md                    # Main skill documentation
│   ├── scripts/
│   │   ├── cortex_api.py           # Python API for inter-skill communication
│   │   ├── trace_session.py        # Updates .cortex_log.md and .cortex_status.json
│   │   ├── handoff_generator.py    # Creates .cortex_handoff.md
│   │   └── install.sh              # Sets up git hooks
│   └── references/
│       ├── API_REFERENCE.md        # Complete API documentation
│       ├── WORKFLOWS.md            # Common usage patterns
│       └── MULTI_LLM.md            # Non-Claude LLM integration
├── synapse/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── synapse_analyzer.py     # Analyzes Cortex data for patterns
│   │   ├── auto_skill_generator.py # Auto-generates skills from patterns
│   │   ├── prd_analyzer.py         # Extracts patterns from PRD files
│   │   ├── pattern_detector.py     # Core pattern detection logic
│   │   └── cortex_integration.py   # Cortex API integration
│   └── references/
│       ├── EXAMPLES.md             # Real-world examples
│       ├── CONFIGURATION.md        # Config reference
│       ├── ADVANCED.md             # Pattern merging, customization
│       └── OUTPUT_FORMAT.md        # Synapse_RECOMMENDATIONS.md format
└── forge/
    ├── SKILL.md
    └── scripts/
        ├── init_skill.py           # Generate skill template
        ├── quick_validate.py       # Validate skill structure
        └── package_skill.py        # Create .skill zip file
```

### Cortex Memory Files (Generated)

Cortex creates three files in project roots (NOT in this repo):
- `.cortex_log.md` - Detailed session history
- `.cortex_status.json` - Machine-readable state
- `.cortex_handoff.md` - Quick context for next session

These are in `.gitignore` but users may choose to commit them for team collaboration.

### Synapse Output Files (Generated)

Synapse creates in project roots (NOT in this repo):
- `Synapse_RECOMMENDATIONS.md` - Prioritized skill recommendations

### The Self-Improving Loop

```
User codes normally
    ↓
Cortex tracks via git hooks → Updates .cortex_log.md, .cortex_status.json
    ↓
User or cron runs Synapse → Analyzes Cortex data
    ↓
Synapse detects patterns (≥5 occurrences) → Creates Synapse_RECOMMENDATIONS.md
    ↓
User or Synapse auto-generates skills → Uses Forge templates
    ↓
New skills use Cortex API → Record their own events
    ↓
Better data for Synapse → Cycle continues
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

Follow Forge's 6-step process:
1. Understand with concrete examples
2. Plan reusable contents (scripts/references/assets)
3. Initialize (`init_skill.py`)
4. Edit (implement resources, write SKILL.md)
5. Package (`package_skill.py`)
6. Iterate based on real usage

### Python Conventions

- All scripts use Python 3.9+
- Cortex API import: `from cortex_api import add_cortex_event, get_cortex_memory, get_pattern_analysis`
- No external dependencies (uses stdlib only)
- Scripts are standalone executables

### Shell Script Conventions

- Use `#!/bin/bash`
- Include `set -e` for error handling
- Provide clear echo messages for user feedback
- Check working directory before critical operations

## Multi-LLM Compatibility

EvolveSkill works with any CLI-based AI assistant:
- Claude Code (native)
- GPT/Codex
- Gemini CLI
- Cursor
- Aider

All skills use universal formats (markdown, JSON) and avoid Claude-specific features.

## Common Tasks

### Add New Functionality to Cortex
1. Edit `.claude/skills/cortex/scripts/cortex_api.py` or related script
2. Update `.claude/skills/cortex/references/API_REFERENCE.md` if API changes
3. Test by running script directly
4. No need to repackage EvolveSkill unless releasing new version

### Add New Pattern Detection to Synapse
1. Edit `.claude/skills/synapse/scripts/pattern_detector.py`
2. Update threshold logic or pattern types
3. Test with real Cortex data (create test commits)
4. Document in `.claude/skills/synapse/references/ADVANCED.md`

### Create New Skill Template
1. Edit `.claude/skills/synapse/scripts/enhanced_skill_templates.py`
2. Add template following existing pattern structure
3. Test by running `auto_skill_generator.py` to trigger generation
4. Validate generated skill with `quick_validate.py`

### Release New Version
1. Update version number in `package_metaskill.sh` call
2. Run `./package_metaskill.sh X.Y.Z`
3. Test installation in clean project
4. Create GitHub release with dist/EvolveSkill-vX.Y.Z.zip

## Testing Workflow

Since this is a meta-framework, testing requires a real project:

```bash
# 1. Setup test project
mkdir /tmp/test-project
cd /tmp/test-project
git init

# 2. Install EvolveSkill
unzip /path/to/EvolveSkill/dist/EvolveSkill-v*.zip
cd .claude/skills/cortex/scripts
./install.sh
cd /tmp/test-project

# 3. Test Cortex tracking
git commit --allow-empty -m "Test commit"
cat .cortex_handoff.md  # Should show session summary

# 4. Create test pattern (repeat 5+ times)
for i in {1..6}; do
  echo "Test API call" >> test.txt
  git add test.txt
  git commit -m "API call test $i"
done

# 5. Test Synapse detection
python /path/to/EvolveSkill/.claude/skills/synapse/scripts/synapse_analyzer.py
cat Synapse_RECOMMENDATIONS.md  # Should show pattern recommendation

# 6. Test auto-generation
python /path/to/EvolveSkill/.claude/skills/synapse/scripts/auto_skill_generator.py
ls .claude/skills/  # Should see generated skill if pattern was HIGH/CRITICAL
```

## Files to Never Commit (Already in .gitignore)

- `__pycache__/`, `*.pyc` - Python cache
- `.DS_Store`, `Thumbs.db` - OS artifacts
- `Synapse_RECOMMENDATIONS.md` - Generated output
- `.cortex_*` files - Cortex memory (user decision whether to commit)
- `dist/*.skill`, `dist/*.zip` - Build artifacts (commit to releases, not main branch)

## Documentation Standards

- Use imperative mood in SKILL.md ("Use this", not "This is used")
- Keep descriptions specific and include trigger keywords
- YAML frontmatter: only `name` and `description` fields
- Reference files from SKILL.md with clear when-to-read guidance
- Table of contents for reference files >100 lines
