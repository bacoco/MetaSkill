#!/bin/bash
# EvolveSkill - One-command installation
# Usage: curl -sL https://raw.githubusercontent.com/bacoco/EvolveSkill/main/install.sh | bash

set -e

echo "🧠 Installing EvolveSkill..."
echo ""

# Detect if we're in the cloned repo or installing remotely
if [ -f "dist/EvolveSkill-v2.0.0.zip" ]; then
    echo "📦 Using local package..."
    ZIP_FILE="dist/EvolveSkill-v2.0.0.zip"
else
    echo "📥 Downloading latest package..."
    ZIP_FILE="/tmp/EvolveSkill-v2.0.0.zip"
    curl -sL https://github.com/bacoco/EvolveSkill/raw/main/dist/EvolveSkill-v2.0.0.zip -o "$ZIP_FILE"
fi

# Create .claude/skills directory if it doesn't exist
mkdir -p .claude/skills

# Extract skills
echo "📂 Extracting skills..."
unzip -q -o "$ZIP_FILE" -d .claude/skills

# Run Cortex installation (git hooks)
echo "🔧 Setting up git hooks..."
cd .claude/skills/cortex/scripts
./install.sh
cd - > /dev/null

echo ""
echo "✅ EvolveSkill installed successfully!"
echo ""
echo "📋 Installed skills:"
echo "  • Cortex - Universal memory system"
echo "  • Synapse - Pattern detection"
echo "  • Forge - Skill creation tools"
echo ""
echo "🚀 You're ready! Just start coding."
echo "   Your AI now has memory, pattern detection, and skill generation."
echo ""
