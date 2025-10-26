#!/bin/bash
# MetaSkill Auto-Install
# Sets up SOUL tracking (git hooks)

set -e

echo "🚀 Installing MetaSkill..."
echo ""

# Check we're in .claude/skills directory
if [[ ! $(pwd) =~ \.claude/skills ]]; then
    echo "⚠️  Warning: Not in .claude/skills directory"
    echo "   Current: $(pwd)"
    echo "   Expected: .../project/.claude/skills"
    echo ""
    echo "   Install should be run from .claude/skills/"
    echo "   Or let your AI handle the installation."
    exit 1
fi

# Navigate to SOUL install script
cd soul/scripts

# Run SOUL installation
echo "📦 Setting up SOUL tracking..."
./install.sh

cd ../..

echo ""
echo "✅ MetaSkill installed successfully!"
echo ""
echo "What just happened:"
echo "  - SOUL: Git hooks installed (tracks your work automatically)"
echo "  - NEXUS: Ready (analyzes patterns when you run it)"
echo "  - skill-generator: Ready (creates custom skills)"
echo ""
echo "Next steps:"
echo "  1. Start coding normally"
echo "  2. SOUL tracks automatically on each commit"
echo "  3. Check .agent_handoff.md after your first commit"
echo "  4. Your AI can now read it for context"
echo ""
echo "That's it. The self-improving loop is active."
echo ""
