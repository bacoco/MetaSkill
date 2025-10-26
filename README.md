# MetaSkill - Self-Improving AI Workflow

Your AI forgets everything between sessions. Every conversation starts from zero.

**MetaSkill fixes this** with three skills that work together to create a self-improving system:

**SOUL** (memory) → **NEXUS** (pattern detection) → **skill-generator** (automation)

The loop never stops. Your AI gets better with every session.

---

## How They Work Together

```
You code normally
        ↓
SOUL tracks automatically (git hooks)
        ↓
Creates .agent_handoff.md with session context
        ↓
Next session: Your AI reads handoff → Has context
        ↓
NEXUS analyzes SOUL data → Detects patterns in your work
        ↓
After 5-10 similar tasks: NEXUS recommends new skill
        ↓
skill-generator creates it → Tailored to YOUR workflow
        ↓
AI uses new skill → Works faster, smarter
        ↓
SOUL tracks improvements → Loop continues
        ↓
System gets better forever
```

**This is why all three are packaged together.** One without the others is incomplete.

---

## Real Examples (All Three Working Together)

### Sarah - API Authentication Work

**Week 1:**
- Sarah debugs JWT auth 5 times
- **SOUL**: Automatically tracks each debugging session
- **NEXUS**: Silent, collecting data
- **skill-generator**: Not triggered yet

**Week 2:**
- Sarah's AI reads `.agent_handoff.md`: "You're working on JWT auth in api/auth.py. Last session you fixed token refresh..."
- No need to re-explain the project every morning
- **NEXUS**: Detects pattern: "API auth debugging = 8 occurrences"

**Week 3:**
- **NEXUS**: Creates recommendation: "Generate api-auth-helper skill?"
- Sarah to her AI: "Create the recommended skill"
- **skill-generator**: Builds skill from NEXUS analysis + SOUL context
- New skill contains common JWT patterns, debugging steps

**Week 4+:**
- API debugging 70% faster (AI has specialized knowledge)
- **SOUL**: Continues tracking
- **NEXUS**: Monitors for new patterns
- **System keeps improving**

**Result:** Self-improving workflow, not just memory.

---

### Marc - Data Pipeline Development

**Day 1-5:**
- Marc builds ETL pipelines, transforms data
- **SOUL**: Tracks all sessions via git commits
- Creates handoffs: "Working on user_data pipeline, transforming JSON to SQL..."

**Day 6:**
- **NEXUS**: Analyzes SOUL logs
- Detects: "Data transformation pattern appears 12 times"
- Generates recommendation in `NEXUS_RECOMMENDATIONS.md`

**Day 7:**
- Marc's AI notices the recommendation
- Marc: "Build that data-pipeline-helper skill"
- **skill-generator**: Creates skill with data transformation templates
- Skill includes common pandas operations Marc uses

**Day 8+:**
- Marc's AI: "I see you're transforming data. Using data-pipeline-helper skill..."
- Pipeline work becomes systematic
- **SOUL** tracks new efficiency gains
- **NEXUS** detects if new sub-patterns emerge

**Result:** AI that adapts to Marc's specific domain.

---

### Julia - Joining a Team

**Team has used MetaSkill for 3 months:**
- **SOUL**: 3 months of session history in `.agent_log.md`
- **NEXUS**: Created 5 team-specific skills (api-helper, test-runner, deploy-checker, etc.)
- **skill-generator**: Used to build these shared skills

**Julia clones the repo:**
- Gets MetaSkill + all team history
- Her AI reads `.agent_handoff.md`: "Team is working on payment API. Current sprint: add Stripe integration..."
- **Day 1**: Julia is productive, not lost

**Julia's unique work:**
- She does a lot of CSS debugging (team doesn't)
- **SOUL**: Tracks her CSS work
- **NEXUS**: After 2 weeks, detects CSS pattern unique to Julia
- **skill-generator**: Creates css-debugger skill

**Next developer:**
- Gets Julia's CSS skill + all previous team skills
- Collective intelligence keeps growing

**Result:** Team knowledge that compounds, not individual silos.

---

## Installation (Works With Any AI Assistant)

**10 seconds. Works with Claude Code, GPT, Gemini, Cursor, Aider, any AI that reads markdown.**

### Copy this to your AI:

```
Clone https://github.com/bacoco/MetaSkill into .claude/skills and run install.sh
```

That's it. Your AI now has:
- Memory across sessions ✓
- Pattern detection ✓
- Auto-generated skills ✓

Start coding. The system activates automatically.

---

## Why All Three Together?

**SOUL alone:** Memory is helpful, but static. You still repeat the same tasks.

**NEXUS alone:** Can't detect patterns without SOUL's session data.

**skill-generator alone:** You manually create skills forever. No automation.

**All three together:**
1. SOUL tracks everything → Feeds NEXUS
2. NEXUS detects patterns → Triggers skill-generator
3. skill-generator creates skills → Improves your workflow
4. Better workflow → Better data for SOUL
5. Cycle repeats → System self-improves

**This is a loop, not a one-time tool.**

That's why they're packaged as one. Separating them breaks the loop.

---

## What Each Skill Does (Technical Details)

### SOUL - Universal Memory
- Installs git hooks (post-commit)
- Creates `.agent_handoff.md` (session summary)
- Creates `.agent_log.md` (detailed history)
- Creates `.agent_status.json` (machine-readable state)
- Your AI reads these for context

### NEXUS - Pattern Detector
- Analyzes SOUL data files
- Detects recurring tasks (API calls, testing, debugging, etc.)
- Threshold: 5+ occurrences = pattern
- Generates skill recommendations
- Can auto-create skills (optional)

### skill-generator - Skill Builder
- Templates for creating new skills
- Validation scripts
- Packaging tools
- Used by NEXUS or manually

**Together:** Memory → Patterns → Automation → Loop

---

## FAQ

**Q: Do I need to do anything after installing?**
A: No. SOUL runs via git hooks. NEXUS runs when you ask. Just code normally.

**Q: Will this work with [my AI]?**
A: Yes. If your AI reads markdown files and runs Python, it works. Claude, GPT, Gemini, Cursor, Aider - all compatible.

**Q: Can I use this in a team?**
A: Yes. Commit `.agent_*` files to git. Everyone gets shared context and skills.

**Q: Does NEXUS create skills automatically?**
A: It recommends them. You (or your AI) decide whether to create them. You're in control.

**Q: What if I don't want auto-generated skills?**
A: Just use SOUL for memory. NEXUS is optional. But you'll miss the self-improving loop.

---

## Documentation

Each skill has detailed docs:

- **SOUL**: [SKILL.md](.claude/skills/soul/SKILL.md) | [API Reference](.claude/skills/soul/references/API_REFERENCE.md)
- **NEXUS**: [SKILL.md](.claude/skills/nexus/SKILL.md) | [Examples](.claude/skills/nexus/references/EXAMPLES.md)
- **skill-generator**: [SKILL.md](.claude/skills/skill-generator/SKILL.md)

See [INSTALLATION.md](INSTALLATION.md) for detailed setup.

---

## The Self-Improving Loop

Traditional AI: Same intelligence every session.

MetaSkill AI:
- Week 1: Has memory (SOUL)
- Week 3: Detects your patterns (NEXUS)
- Week 5: Auto-generates your first custom skill
- Week 10: Has 3 custom skills tailored to you
- Week 20: Has 8 skills, each refined by usage
- **Intelligence compounds over time**

Install once. Improves forever.

---

**MetaSkill** - AI that remembers, learns, and improves

*Three skills. One self-improving system.*
