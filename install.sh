#!/bin/bash
# EvolveSkill Auto-Install
# Sets up Cortex tracking (git hooks)

set -e

echo "🚀 Installing EvolveSkill..."
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

# Navigate to Cortex install script
cd soul/scripts

# Run Cortex installation
echo "📦 Setting up Cortex tracking..."
./install.sh

cd ../..

echo ""
echo "✅ EvolveSkill installed successfully!"
echo ""
echo "What just happened:"
echo "  - Cortex: Git hooks installed (tracks your work automatically)"
echo "  - Synapse: Ready (analyzes patterns when you run it)"
echo "  - Forge: Ready (creates custom skills)"
echo ""
echo "Next steps:"
echo "  1. Start coding normally"
echo "  2. Cortex tracks automatically on each commit"
echo "  3. Check .cortex_handoff.md after your first commit"
echo "  4. Your AI can now read it for context"
echo ""
echo "That's it. The self-improving loop is active."
echo ""
