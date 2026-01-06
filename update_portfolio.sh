#!/bin/bash

# Professional Portfolio Update Script
# Run this script to update your GitHub portfolio with latest changes

echo "🚀 Updating Professional Portfolio..."

# Add all changes
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "✅ No changes to commit"
    exit 0
fi

# Prompt for commit message
echo "Enter commit message (or press Enter for default):"
read commit_message

if [ -z "$commit_message" ]; then
    commit_message="Update professional portfolio - $(date +'%Y-%m-%d %H:%M')"
fi

# Commit changes
git commit -m "$commit_message"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo "✅ Portfolio updated successfully!"
echo "🌐 View your portfolio at: https://github.com/YOUR_USERNAME/professional-portfolio"
echo "📄 README at: https://github.com/YOUR_USERNAME/professional-portfolio#readme"

echo ""
echo "💡 Tip: Update your LinkedIn and resume to link to your GitHub portfolio!"
echo "🎯 Use this repository to showcase your system reliability expertise to employers."
