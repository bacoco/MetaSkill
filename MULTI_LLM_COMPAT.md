# Multi-LLM Compatibility Guide

EvolveSkill is assistant-agnostic. It works with any AI that can read Markdown files and run local commands.

Key principles:
- Context via plain files: `.cortex_handoff.md`, `.cortex_log.md`, `.cortex_status.json`
- Orchestration via Python/Bash (no vendor SDKs)
- Git hooks for automatic tracking

How to use with common assistants:
- Claude Code / Cursor: Ask it to open and read `.cortex_handoff.md` at session start. Use `make analyze` or `./scripts/es analyze` to refresh recommendations.
- GPT (Code Interpreter/CLI): Have it run the same commands. Ensure Python 3.9+ is available.
- Gemini CLI or other CLIs: Run `./scripts/es trace` after commits, and open the handoff file in the editor.

Notes:
- Dotfiles: Some UIs hide dotfiles by default. Explicitly open `.cortex_handoff.md`.
- No proprietary “skills” runtime assumed: skills are folders with docs + scripts.
- “OU” (logical OR in docs/instructions) has no impact on execution; it’s documentation-only.

Quick commands:
- Install hooks: `make install` or `./scripts/es install`
- Trace now: `make trace`
- Analyze: `make analyze THRESHOLD=5 DAYS=7`
- Auto-generate: `make auto-generate THRESHOLD=5 DAYS=7`
- Package: `make package`
