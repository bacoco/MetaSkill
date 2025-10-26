#!/bin/bash
# Package MetaSkill - Create universal distribution zip
# Works with all LLMs: Claude Code, GPT, Gemini, Cursor, Aider, etc.

set -e

VERSION="${1:-1.0.0}"
OUTPUT_DIR="dist"
ARCHIVE_NAME="MetaSkill-v${VERSION}.zip"

echo "📦 Packaging MetaSkill v${VERSION}..."
echo ""

# Create dist directory
mkdir -p "$OUTPUT_DIR"

# Clean previous build
rm -f "$OUTPUT_DIR/$ARCHIVE_NAME"

# Create temporary build directory
BUILD_DIR=$(mktemp -d)
trap "rm -rf $BUILD_DIR" EXIT

# Copy skills and documentation
echo "📋 Copying skills..."
mkdir -p "$BUILD_DIR/.claude/skills"
cp -r .claude/skills/soul "$BUILD_DIR/.claude/skills/"
cp -r .claude/skills/nexus "$BUILD_DIR/.claude/skills/"
cp -r .claude/skills/skill-generator "$BUILD_DIR/.claude/skills/"

echo "📚 Copying documentation..."
cp README.md "$BUILD_DIR/"
cp INSTALLATION.md "$BUILD_DIR/"
cp .gitignore "$BUILD_DIR/"

# Create LICENSE if not exists
if [ ! -f LICENSE ]; then
    echo "⚠️  No LICENSE file found, skipping..."
else
    cp LICENSE "$BUILD_DIR/"
fi

# Clean Python cache
echo "🧹 Cleaning Python cache and artifacts..."
find "$BUILD_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$BUILD_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$BUILD_DIR" -type f -name "*.pyo" -delete 2>/dev/null || true

# Clean OS artifacts
find "$BUILD_DIR" -type f -name ".DS_Store" -delete 2>/dev/null || true
find "$BUILD_DIR" -type f -name "Thumbs.db" -delete 2>/dev/null || true

# Clean individual skill zips (we have one global zip now)
find "$BUILD_DIR" -type f -name "*.zip" -delete 2>/dev/null || true

# Create zip
echo "🗜️  Creating archive..."
CURRENT_DIR=$(pwd)
cd "$BUILD_DIR"
zip -r "$CURRENT_DIR/$OUTPUT_DIR/$ARCHIVE_NAME" . -x "*.git*" > /dev/null

cd "$CURRENT_DIR" > /dev/null

# Display results
SIZE=$(ls -lh "$OUTPUT_DIR/$ARCHIVE_NAME" | awk '{print $5}')
echo ""
echo "✅ Package created successfully!"
echo ""
echo "📦 Archive: $OUTPUT_DIR/$ARCHIVE_NAME"
echo "📏 Size: $SIZE"
echo ""
echo "📋 MetaSkill - Complete Package:"
echo "  ✅ SOUL - Universal memory system"
echo "  ✅ NEXUS - Automatic skill generator"
echo "  ✅ skill-generator - Skill creation tool"
echo "  ✅ Complete documentation"
echo ""
echo "📦 Single archive - all three skills together"
echo "   (They're interdependent, must be installed as a set)"
echo ""
echo "🚀 Installation:"
echo "  unzip $ARCHIVE_NAME"
echo "  cp -r .claude/skills /path/to/your/project/.claude/"
echo "  cd /path/to/your/project/.claude/skills/soul/scripts"
echo "  ./install.sh"
echo ""
echo "🌐 Compatible with ALL AI coding assistants!"
echo ""
