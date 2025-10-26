# EvolveSkill - Self-Improving AI Workflow

Your AI forgets everything between sessions. Every conversation starts from zero.

**EvolveSkill fixes this** with three skills that work together to create a self-improving system:

**Cortex** (memory) → **Synapse** (pattern detection) → **Forge** (automation)

The loop never stops. Your AI gets better with every session.

---

## How They Work Together

```
You code normally
        ↓
Cortex tracks automatically (git hooks)
        ↓
Creates .cortex_handoff.md with session context
        ↓
Next session: Your AI reads handoff → Has context
        ↓
Synapse analyzes Cortex data → Detects patterns in your work
        ↓
After 5-10 similar tasks: Synapse recommends new skill
        ↓
Forge creates it → Tailored to YOUR workflow
        ↓
AI uses new skill → Works faster, smarter
        ↓
Cortex tracks improvements → Loop continues
        ↓
System gets better forever
```

**This is why all three are packaged together.** One without the others is incomplete.

---

## How It Works - Visual Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                          YOU CODE NORMALLY                        │
│                     (git commits, file changes)                   │
└──────────────────────────────────────────────────────────────────┘
                                   ↓
        ┌──────────────────────────────────────────────────┐
        │         CORTEX (Memory Brain)                    │
        │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
        │  • Tracks EVERYTHING via git hooks               │
        │  • Creates .cortex_log.md (session history)      │
        │  • Creates .cortex_status.json (current state)   │
        │  • Creates .cortex_handoff.md (next session)     │
        │                                                   │
        │  → Your AI reads these files for context         │
        └──────────────────────────────────────────────────┘
                                   ↓
        ┌──────────────────────────────────────────────────┐
        │        SYNAPSE (Pattern Brain)                   │
        │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
        │  • Reads Cortex memory files                     │
        │  • Detects recurring patterns                    │
        │  • Threshold: 5+ similar tasks                   │
        │  • Priority: Critical (2+/day) → Low (<3/week)   │
        │                                                   │
        │  → Generates SYNAPSE_RECOMMENDATIONS.md          │
        └──────────────────────────────────────────────────┘
                                   ↓
        ┌──────────────────────────────────────────────────┐
        │          FORGE (Skill Builder)                   │
        │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
        │  • Takes Synapse recommendations                 │
        │  • Uses Cortex context for details               │
        │  • Generates custom skill code                   │
        │  • Validates and packages                        │
        │                                                   │
        │  → Creates .claude/skills/your-new-skill/        │
        └──────────────────────────────────────────────────┘
                                   ↓
        ┌──────────────────────────────────────────────────┐
        │           NEW CUSTOM SKILLS                       │
        │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
        │  • Tailored to YOUR workflow                     │
        │  • Use Cortex API to record events               │
        │  • Make your AI faster at specific tasks         │
        └──────────────────────────────────────────────────┘
                                   ↓
                    ┌──────────────────────────┐
                    │   BETTER PATTERNS  ──────┼───┐
                    └──────────────────────────┘   │
                                   ↓               │
                         LOOP CONTINUES ───────────┘
                    (System gets smarter forever)
```

### The Self-Improving Cycle

1. **Week 1**: Cortex tracks your work → Creates memory
2. **Week 2**: Synapse analyzes → Detects you debug APIs 8 times
3. **Week 3**: Forge creates → "api-debugger" skill custom to you
4. **Week 4+**: AI uses new skill → Works 70% faster on API tasks
5. **Forever**: New patterns emerge → More skills generated → Intelligence compounds

---

## Real Examples (All Three Working Together)

### Sarah - API Authentication Work

**Week 1:**
- Sarah debugs JWT auth 5 times
- **Cortex**: Automatically tracks each debugging session
- **Synapse**: Silent, collecting data
- **Forge**: Not triggered yet

**Week 2:**
- Sarah's AI reads `.cortex_handoff.md`: "You're working on JWT auth in api/auth.py. Last session you fixed token refresh..."
- No need to re-explain the project every morning
- **Synapse**: Detects pattern: "API auth debugging = 8 occurrences"

**Week 3:**
- **Synapse**: Creates recommendation: "Generate api-auth-helper skill?"
- Sarah to her AI: "Create the recommended skill"
- **Forge**: Builds skill from Synapse analysis + Cortex context
- New skill contains common JWT patterns, debugging steps

**Week 4+:**
- API debugging 70% faster (AI has specialized knowledge)
- **Cortex**: Continues tracking
- **Synapse**: Monitors for new patterns
- **System keeps improving**

**Result:** Self-improving workflow, not just memory.

---

### Marc - Data Pipeline Development

**Day 1-5:**
- Marc builds ETL pipelines, transforms data
- **Cortex**: Tracks all sessions via git commits
- Creates handoffs: "Working on user_data pipeline, transforming JSON to SQL..."

**Day 6:**
- **Synapse**: Analyzes Cortex logs
- Detects: "Data transformation pattern appears 12 times"
- Generates recommendation in `Synapse_RECOMMENDATIONS.md`

**Day 7:**
- Marc's AI notices the recommendation
- Marc: "Build that data-pipeline-helper skill"
- **Forge**: Creates skill with data transformation templates
- Skill includes common pandas operations Marc uses

**Day 8+:**
- Marc's AI: "I see you're transforming data. Using data-pipeline-helper skill..."
- Pipeline work becomes systematic
- **Cortex** tracks new efficiency gains
- **Synapse** detects if new sub-patterns emerge

**Result:** AI that adapts to Marc's specific domain.

---

### Julia - Joining a Team

**Team has used EvolveSkill for 3 months:**
- **Cortex**: 3 months of session history in `.cortex_log.md`
- **Synapse**: Created 5 team-specific skills (api-helper, test-runner, deploy-checker, etc.)
- **Forge**: Used to build these shared skills

**Julia clones the repo:**
- Gets EvolveSkill + all team history
- Her AI reads `.cortex_handoff.md`: "Team is working on payment API. Current sprint: add Stripe integration..."
- **Day 1**: Julia is productive, not lost

**Julia's unique work:**
- She does a lot of CSS debugging (team doesn't)
- **Cortex**: Tracks her CSS work
- **Synapse**: After 2 weeks, detects CSS pattern unique to Julia
- **Forge**: Creates css-debugger skill

**Next developer:**
- Gets Julia's CSS skill + all previous team skills
- Collective intelligence keeps growing

**Result:** Team knowledge that compounds, not individual silos.

---

## Installation (Works With Any AI Assistant)

**10 seconds. Works with Claude Code, GPT, Gemini, Cursor, Aider, any AI that reads markdown.**

### Say this to your AI:

```
Install EvolveSkill from https://github.com/bacoco/EvolveSkill
```

That's it. Your AI will:
- Download and install the skills ✓
- Set up git hooks automatically ✓
- Be ready with memory, patterns, and skill generation ✓

Start coding. The system activates automatically.

---

## Why All Three Together?

**Cortex alone:** Memory is helpful, but static. You still repeat the same tasks.

**Synapse alone:** Can't detect patterns without Cortex's session data.

**Forge alone:** You manually create skills forever. No automation.

**All three together:**
1. Cortex tracks everything → Feeds Synapse
2. Synapse detects patterns → Triggers Forge
3. Forge creates skills → Improves your workflow
4. Better workflow → Better data for Cortex
5. Cycle repeats → System self-improves

**This is a loop, not a one-time tool.**

That's why they're packaged as one. Separating them breaks the loop.

---

## What Each Skill Does (Technical Details)

### Cortex - Universal Memory
- Installs git hooks (post-commit)
- Creates `.cortex_handoff.md` (session summary)
- Creates `.cortex_log.md` (detailed history)
- Creates `.cortex_status.json` (machine-readable state)
- Your AI reads these for context

### Synapse - Pattern Detector
- Analyzes Cortex data files
- Detects recurring tasks (API calls, testing, debugging, etc.)
- Threshold: 5+ occurrences = pattern
- Generates skill recommendations
- Can auto-create skills (optional)

### Forge - Skill Builder
- Templates for creating new skills
- Validation scripts
- Packaging tools
- Used by Synapse or manually

**Together:** Memory → Patterns → Automation → Loop

---

## FAQ

**Q: Do I need to do anything after installing?**
A: No. Cortex runs via git hooks. Synapse runs when you ask. Just code normally.

**Q: Will this work with [my AI]?**
A: Yes. If your AI reads markdown files and runs Python, it works. Claude, GPT, Gemini, Cursor, Aider - all compatible.

**Q: Can I use this in a team?**
A: Yes. Commit `.cortex_*` files to git. Everyone gets shared context and skills.

**Q: Does Synapse create skills automatically?**
A: It recommends them. You (or your AI) decide whether to create them. You're in control.

**Q: What if I don't want auto-generated skills?**
A: Just use Cortex for memory. Synapse is optional. But you'll miss the self-improving loop.

---

## Documentation

Each skill has detailed docs:

- **Cortex**: [SKILL.md](.claude/skills/cortex/SKILL.md) | [API Reference](.claude/skills/cortex/references/API_REFERENCE.md)
- **Synapse**: [SKILL.md](.claude/skills/synapse/SKILL.md) | [Examples](.claude/skills/synapse/references/EXAMPLES.md)
- **Forge**: [SKILL.md](.claude/skills/forge/SKILL.md)

See [INSTALLATION.md](INSTALLATION.md) for detailed setup.

---

## The Self-Improving Loop

Traditional AI: Same intelligence every session.

EvolveSkill AI:
- Week 1: Has memory (Cortex)
- Week 3: Detects your patterns (Synapse)
- Week 5: Auto-generates your first custom skill
- Week 10: Has 3 custom skills tailored to you
- Week 20: Has 8 skills, each refined by usage
- **Intelligence compounds over time**

Install once. Improves forever.

---

**EvolveSkill** - AI that remembers, learns, and improves

*Three skills. One self-improving system.*
