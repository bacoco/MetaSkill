# Synapse Multi-LLM Support

Using Synapse with different LLM platforms.

## Universal Output Format

Synapse uses LLM-agnostic formats:
- **Markdown** for human-readable recommendations
- **JSON** for machine-readable data
- **Python** for programmatic access

No LLM-specific syntax required.

## Supported LLMs

### Claude Code (Native)

**How It Works:**
- Synapse runs automatically via cron/git hooks
- Auto-generates skills when patterns detected
- Skills immediately available to Claude
- Full integration with Cortex memory

**Setup:**

```bash
# Run manually
python .claude/skills/synapse/scripts/auto_skill_generator.py

# Or setup automatic monitoring
*/30 * * * * /path/to/.claude/skills/scripts/nexus_auto_watch.sh
```

**Usage:**

```bash
# Claude automatically uses generated skills
claude

# Synapse has already created skills based on your patterns
# Claude loads them automatically
```

**Features:**
- ✅ Automatic skill generation
- ✅ Cortex integration
- ✅ Immediate skill loading
- ✅ Full progressive disclosure support

---

### OpenAI GPT (CLI)

**How It Works:**
- Synapse runs in background
- Generates `Synapse_RECOMMENDATIONS.md`
- GPT reads recommendations manually or via system prompt

**Setup:**

```bash
# 1. Setup Synapse monitoring (same as Claude)
*/30 * * * * /path/to/.claude/skills/scripts/nexus_auto_watch.sh

# 2. Configure GPT to read recommendations
cat > ~/.config/gpt/system_prompt.txt << 'EOF'
Check Synapse_RECOMMENDATIONS.md for skill recommendations.
If high-priority skills are recommended, notify the user.
EOF
```

**Usage:**

```bash
# Start GPT session
gpt

# Ask about recommendations
> Check Synapse recommendations

# GPT reads Synapse_RECOMMENDATIONS.md and reports:
"Synapse recommends 2 high-priority skills:
1. api-optimizer (CRITICAL)
2. test-guardian (HIGH)

Would you like me to create these skills?"
```

**Manual Workflow:**

```bash
# 1. Run Synapse analysis
python .claude/skills/synapse/scripts/nexus_analyzer.py

# 2. Read recommendations
cat Synapse_RECOMMENDATIONS.md

# 3. Ask GPT to create recommended skills
gpt
> Create the api-optimizer skill as recommended by Synapse
```

**Features:**
- ✅ Reads recommendations
- ⚠️ Manual skill creation
- ⚠️ No automatic monitoring
- ✅ Cortex integration (via Python API)

---

### Google Gemini (CLI)

**How It Works:**
- Synapse generates recommendations
- Gemini reads markdown recommendations
- Manual or semi-automatic skill creation

**Setup:**

```bash
# 1. Setup Synapse monitoring
*/30 * * * * /path/to/.claude/skills/scripts/nexus_auto_watch.sh

# 2. Configure Gemini startup script
cat > ~/.gemini/startup.sh << 'EOF'
#!/bin/bash
if [ -f "Synapse_RECOMMENDATIONS.md" ]; then
    echo "📊 Synapse recommendations available. Type 'check nexus' to review."
fi
EOF
```

**Usage:**

```bash
# Start Gemini
gemini

# Check recommendations
> Read Synapse_RECOMMENDATIONS.md and summarize

# Create recommended skills
> Create the api-optimizer skill following Synapse recommendations
```

**Features:**
- ✅ Reads recommendations
- ⚠️ Manual skill creation
- ⚠️ No automatic monitoring
- ✅ Cortex integration (via Python API)

---

### Cursor

**How It Works:**
- Synapse runs in background
- Cursor reads recommendations via sidebar
- Skills created manually

**Setup:**

```bash
# 1. Setup Synapse monitoring
*/30 * * * * /path/to/.claude/skills/scripts/nexus_auto_watch.sh

# 2. Add to workspace settings (.vscode/settings.json)
{
  "cursor.ai.systemPrompt": "Check Synapse_RECOMMENDATIONS.md for skill recommendations. Notify user if high-priority skills are recommended."
}
```

**Usage:**

Open Cursor → AI will notify if Synapse has recommendations → Create skills manually

**Features:**
- ⚠️ Manual recommendation checking
- ⚠️ Manual skill creation
- ❌ No automatic skill generation
- ⚠️ Limited Cortex integration

---

### Aider

**How It Works:**
- Synapse generates recommendations
- Aider reads via file context
- Semi-automatic skill creation

**Setup:**

```bash
# 1. Setup Synapse monitoring
*/30 * * * * /path/to/.claude/skills/scripts/nexus_auto_watch.sh

# 2. Add to .aider.conf.yml
read:
  - Synapse_RECOMMENDATIONS.md

message: |
  Check Synapse_RECOMMENDATIONS.md for skill recommendations.
  Create high-priority skills automatically.
```

**Usage:**

```bash
# Start Aider
aider

# Aider automatically reads Synapse_RECOMMENDATIONS.md
# Ask to create skills:
> Create the skills recommended by Synapse
```

**Features:**
- ✅ Automatic recommendation reading
- ⚠️ Semi-automatic skill creation
- ✅ Cortex integration
- ✅ Good file context management

---

## Cross-LLM Workflows

### Scenario 1: Claude Generates, GPT Uses

```bash
# Developer A uses Claude Code
# Synapse auto-generates api-optimizer skill

# Developer B uses GPT
# Checks out same repository
# GPT can't load skills automatically but can read:
gpt
> Read .claude/skills/api-optimizer/SKILL.md and apply its patterns
```

### Scenario 2: Shared Recommendations

```bash
# Project team uses different LLMs
# Synapse generates universal recommendations

# All team members can:
cat Synapse_RECOMMENDATIONS.md

# Each LLM handles skill creation differently:
# - Claude: Automatic
# - GPT: Manual via skill-creator
# - Gemini: Manual via skill-creator
```

---

## LLM Comparison Table

| Feature | Claude Code | GPT CLI | Gemini CLI | Cursor | Aider |
|---------|-------------|---------|------------|--------|-------|
| Auto skill generation | ✅ Full | ❌ No | ❌ No | ❌ No | ⚠️ Semi |
| Read recommendations | ✅ Auto | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ✅ Auto |
| Cortex integration | ✅ Full | ⚠️ API only | ⚠️ API only | ❌ No | ⚠️ API only |
| Skill loading | ✅ Auto | ❌ No | ❌ No | ❌ No | ❌ No |
| Progressive disclosure | ✅ Full | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual |
| Monitoring setup | ✅ Easy | ✅ Easy | ✅ Easy | ✅ Easy | ✅ Easy |

**Legend:**
- ✅ Full support
- ⚠️ Partial / Manual
- ❌ Not supported

---

## Recommendation Consumption

### For Humans

Read the markdown file directly:

```bash
cat Synapse_RECOMMENDATIONS.md
```

### For Claude Code

Claude automatically:
1. Runs Synapse in background
2. Generates skills when patterns detected
3. Loads skills automatically

### For Other LLMs

**Option 1: Manual Creation**

```bash
# 1. Read recommendations
cat Synapse_RECOMMENDATIONS.md

# 2. Ask LLM to create skill
your-llm
> Create a skill called api-optimizer based on Synapse recommendations
```

**Option 2: Use skill-creator**

```bash
# 1. Read recommendations
python .claude/skills/synapse/scripts/nexus_analyzer.py

# 2. Use skill-creator meta-skill
your-llm
> Use skill-creator to generate the api-optimizer skill
```

**Option 3: Python Script**

```python
#!/usr/bin/env python3
"""Auto-create skills from Synapse for non-Claude LLMs"""
import subprocess
import json

# Read recommendations
with open("Synapse_RECOMMENDATIONS.md") as f:
    content = f.read()

# Parse recommendations (simplified)
if "🔴 CRITICAL" in content or "🟠 HIGH" in content:
    # Trigger skill-creator
    subprocess.run([
        "your-llm-cli",
        "--prompt",
        "Create skills based on Synapse_RECOMMENDATIONS.md"
    ])
```

---

## JSON Format for Programmatic Access

Generate machine-readable format:

```bash
python .claude/skills/synapse/scripts/nexus_analyzer.py --format json
```

```json
{
  "recommendations": [
    {
      "skill_name": "api-optimizer",
      "priority": "critical",
      "pattern_type": "api_call",
      "frequency": 3.4,
      "contexts": [...]
    }
  ]
}
```

Parse with any language:

```python
# Python
import json
with open("Synapse_RECOMMENDATIONS.json") as f:
    recs = json.load(f)

# JavaScript
const recs = require('./Synapse_RECOMMENDATIONS.json');

# Ruby
require 'json'
recs = JSON.parse(File.read('Synapse_RECOMMENDATIONS.json'))
```

---

## Best Practices by LLM

### For Claude Code Users

**Do:**
- ✅ Setup automatic monitoring (cron/git hooks)
- ✅ Let Synapse auto-generate skills
- ✅ Trust the automation

**Don't:**
- ❌ Manually create skills that Synapse recommends
- ❌ Disable auto-generation without reason

### For GPT Users

**Do:**
- ✅ Check `Synapse_RECOMMENDATIONS.md` regularly
- ✅ Use skill-creator to generate recommended skills
- ✅ Integrate Cortex API in custom scripts

**Don't:**
- ❌ Ignore high-priority recommendations
- ❌ Recreate skills that Synapse would auto-generate

### For Gemini Users

**Do:**
- ✅ Setup monitoring (Synapse runs same way)
- ✅ Read recommendations at session start
- ✅ Create skills for critical/high priorities

**Don't:**
- ❌ Skip checking recommendations
- ❌ Create skills for low-priority patterns

### For Cursor Users

**Do:**
- ✅ Add Synapse to workspace awareness
- ✅ Review recommendations weekly
- ✅ Create high-priority skills manually

**Don't:**
- ❌ Ignore Synapse entirely (limited value)

### For Aider Users

**Do:**
- ✅ Add Synapse_RECOMMENDATIONS.md to read list
- ✅ Configure auto-reading in .aider.conf.yml
- ✅ Batch-create recommended skills

**Don't:**
- ❌ Skip configuration step
- ❌ Ignore semi-automation opportunities

---

## Troubleshooting by LLM

### GPT: Can't Read Recommendations

**Problem:**
GPT doesn't automatically check Synapse_RECOMMENDATIONS.md

**Solution:**
```bash
# Explicitly ask GPT:
> Read Synapse_RECOMMENDATIONS.md and tell me what skills are recommended
```

### Gemini: Skill Creation Failed

**Problem:**
Gemini doesn't understand skill structure

**Solution:**
```bash
# Provide skill-creator guidance:
> Use the skill-creator skill to generate the api-optimizer skill following the template in .claude/skills/skill-creator/
```

### Cursor: No Skill Awareness

**Problem:**
Cursor doesn't load Claude skills

**Solution:**
```bash
# Manual skill application:
> Read .claude/skills/api-optimizer/SKILL.md and apply those patterns to this API call
```

---

## See Also

- [INSTALLATION.md](INSTALLATION.md) - Setup guide
- [MANUAL_USAGE.md](MANUAL_USAGE.md) - Command-line options
- [EXAMPLES.md](EXAMPLES.md) - Real-world examples
- Cortex [MULTI_LLM.md](../../soul/references/MULTI_LLM.md) - Cortex multi-LLM guide
- Main SKILL.md - Synapse overview
