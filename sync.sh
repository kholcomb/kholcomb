#!/bin/bash
# Convenience script for syncing local repo with remote
# Handles auto-generated files from GitHub Actions gracefully

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔄 Syncing local repo with remote...${NC}"

# Fetch latest changes
git fetch origin main

# Check if there are remote changes
if git diff --quiet HEAD origin/main; then
    echo -e "${GREEN}✓ Already up to date${NC}"
    exit 0
fi

# Show what will be updated
echo -e "${YELLOW}Remote changes detected:${NC}"
git log HEAD..origin/main --oneline --decorate

# Pull changes, handling auto-generated files
echo -e "${YELLOW}Merging remote changes...${NC}"

# Try to merge
if git merge origin/main --no-edit; then
    echo -e "${GREEN}✓ Successfully merged${NC}"
else
    # Handle conflicts in auto-generated files
    echo -e "${RED}⚠️  Merge conflicts detected${NC}"

    if git diff --name-only --diff-filter=U | grep -qE '(README.md|stats.json|\.svg)'; then
        echo -e "${YELLOW}Resolving conflicts in auto-generated files...${NC}"

        # Accept remote version of auto-generated files
        git checkout --theirs README.md 2>/dev/null || true
        git checkout --theirs cache/stats.json 2>/dev/null || true
        git checkout --theirs dark_mode.svg 2>/dev/null || true
        git checkout --theirs light_mode.svg 2>/dev/null || true

        # Add resolved files
        git add README.md cache/stats.json dark_mode.svg light_mode.svg 2>/dev/null || true

        # Complete the merge
        git commit --no-edit

        echo -e "${GREEN}✓ Conflicts resolved${NC}"
        echo -e "${YELLOW}Note: Auto-generated files were updated. Run 'python today.py' to regenerate with your latest changes.${NC}"
    else
        echo -e "${RED}✗ Manual conflict resolution required${NC}"
        echo -e "Files with conflicts:"
        git diff --name-only --diff-filter=U
        exit 1
    fi
fi

echo -e "${GREEN}✅ Sync complete!${NC}"
