# Git Workflow Guide

This repository has **auto-generated files** that are updated daily by GitHub Actions. This guide helps you stay in sync.

## 🔄 Auto-Generated Files

These files are regenerated daily at midnight UTC:
- `README.md` (cache-busting parameters)
- `cache/stats.json` (GitHub statistics)
- `cache/resume_data.json` (resume data)
- `light_mode.svg` (GitHub stats graphic)
- `dark_mode.svg` (GitHub stats graphic)

## ✅ Recommended Workflow

### Option 1: Use the Sync Script (Easiest)

```bash
# Before starting work - sync with remote
./sync.sh

# Make your changes
vim today.py  # or edit other files

# Commit and push (pre-push hook will auto-sync)
git add .
git commit -m "Your message"
git push
```

### Option 2: Manual Sync

```bash
# Before starting work
git fetch origin main
git merge origin/main --no-edit

# If conflicts in auto-generated files
git checkout --theirs README.md cache/stats.json dark_mode.svg light_mode.svg
git add README.md cache/stats.json dark_mode.svg light_mode.svg
git commit --no-edit

# Make your changes and push
git add .
git commit -m "Your message"
git push
```

## 🛠️ What's Been Set Up

### 1. Pre-Push Hook
Automatically installed at `.git/hooks/pre-push`
- Syncs with remote before every push
- Handles auto-generated file conflicts automatically
- You don't need to do anything - it just works!

### 2. Sync Script (`sync.sh`)
Convenient script for manual syncing:
```bash
./sync.sh  # That's it!
```

## 💡 Common Scenarios

### Scenario 1: Starting a New Work Session
```bash
./sync.sh          # Get latest changes
# Edit files...
git add .
git commit -m "Update skills section"
git push           # Pre-push hook auto-syncs again
```

### Scenario 2: Push Failed Due to Remote Changes
```bash
# If push fails:
./sync.sh          # Sync with remote
git push           # Try again
```

### Scenario 3: Regenerate Stats Locally
```bash
./sync.sh          # Get latest first
python today.py    # Regenerate with your code
git add .
git commit -m "Regenerate stats with updated code"
git push
```

## 📝 Best Practices

1. **Always sync before starting work**: Run `./sync.sh`
2. **Commit logical changes separately**: Don't mix feature changes with stats regeneration
3. **Let GitHub Actions handle daily updates**: You don't need to run `today.py` unless you changed its logic
4. **If you modify `today.py`**: Regenerate locally to test, then commit

## 🚨 Troubleshooting

### "Push rejected - fetch first"
```bash
./sync.sh
git push
```

### "Merge conflict in README.md"
```bash
# Accept remote version (it's auto-generated anyway)
git checkout --theirs README.md cache/stats.json dark_mode.svg light_mode.svg
git add README.md cache/stats.json dark_mode.svg light_mode.svg
git commit --no-edit
```

### "I want to see what changed remotely"
```bash
git fetch origin main
git log HEAD..origin/main --oneline
git diff HEAD..origin/main
```

## 🎯 Quick Commands

```bash
# Sync with remote
./sync.sh

# See remote changes without pulling
git fetch origin main && git log HEAD..origin/main --oneline

# Force pull (nuclear option - discards local changes)
git reset --hard origin/main

# Check if local is behind remote
git fetch origin main && git status
```

## ⚙️ Git Aliases (Optional)

Add these to your `~/.gitconfig`:

```ini
[alias]
    sync = "!./sync.sh"
    update = "pull --no-edit origin main"
    conflicts = "diff --name-only --diff-filter=U"
```

Then use:
```bash
git sync      # Run sync script
git update    # Pull and merge
git conflicts # Show conflicted files
```
