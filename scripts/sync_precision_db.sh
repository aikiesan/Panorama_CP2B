#!/bin/bash
# Auto-sync precision database from Jupyter validation to webapp
# Usage: ./scripts/sync_precision_db.sh [optional commit message]

set -e  # Exit on error

# Paths
SOURCE="C:/Users/Lucas/Documents/CP2B/Validacao_dados/CP2B_Precision_Biogas.db"
DEST="C:/Users/Lucas/Documents/CP2B/PanoramaCP2B/data/CP2B_Precision_Biogas.db"

# Check source exists
if [ ! -f "$SOURCE" ]; then
    echo "❌ Error: Source database not found at $SOURCE"
    exit 1
fi

# Get database info
SOURCE_SIZE=$(du -h "$SOURCE" | cut -f1)
SOURCE_COUNT=$(sqlite3 "$SOURCE" "SELECT COUNT(*) FROM chemical_parameters WHERE is_validated=1")

echo "📊 Source Database Info:"
echo "   Size: $SOURCE_SIZE"
echo "   Validated parameters: $SOURCE_COUNT"
echo ""

# Confirm sync
read -p "Sync database to webapp? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Sync cancelled"
    exit 0
fi

# Copy database
echo "📦 Copying database..."
cp "$SOURCE" "$DEST"

# Verify copy
DEST_COUNT=$(sqlite3 "$DEST" "SELECT COUNT(*) FROM chemical_parameters WHERE is_validated=1")
if [ "$SOURCE_COUNT" -ne "$DEST_COUNT" ]; then
    echo "❌ Error: Parameter count mismatch after copy!"
    echo "   Source: $SOURCE_COUNT"
    echo "   Dest: $DEST_COUNT"
    exit 1
fi

echo "✅ Database copied successfully"
echo ""

# Git operations
cd "C:/Users/Lucas/Documents/CP2B/PanoramaCP2B"

# Stage database
git add data/CP2B_Precision_Biogas.db

# Check if there are changes
if git diff --cached --quiet; then
    echo "ℹ️  No database changes to commit"
    exit 0
fi

# Create commit message
if [ -n "$1" ]; then
    # Custom message provided
    COMMIT_MSG="data: $1"
else
    # Auto-generated message
    COMMIT_MSG="data: Sync precision database - $SOURCE_COUNT validated parameters ($(date +'%Y-%m-%d %H:%M'))"
fi

# Commit
echo "📝 Committing changes..."
git commit -m "$COMMIT_MSG

Updated CP2B_Precision_Biogas.db from Jupyter validation workflow.
Validated parameters: $SOURCE_COUNT
Database size: $SOURCE_SIZE

🤖 Generated with Claude Code sync script

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push
echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Sync complete!"
echo "🌐 Streamlit Cloud will auto-deploy in 1-3 minutes"
echo "   Visit: https://panoramacp2b.streamlit.app/"
