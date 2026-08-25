#!/usr/bin/env bash
# ==============================================================================
# Patch-Based Upstream Sync Helper for PCD AV1 Database
# ==============================================================================
# Synchronizes upstream Dictionarry-Hub/database changes across severed git
# ancestry histories using SHA-range diffs and tracked last-upstream-sha pointer.
# ==============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SHA_FILE=".github/last-upstream-sha"
UPSTREAM_REPO="https://github.com/Dictionarry-Hub/database.git"
UPSTREAM_BRANCH="v2"

if [ ! -f "$SHA_FILE" ]; then
    echo "Error: $SHA_FILE not found." >&2
    exit 1
fi

LAST_SHA=$(tr -d '[:space:]' < "$SHA_FILE")

# Ensure upstream remote exists
if ! git remote get-url upstream >/dev/null 2>&1; then
    echo "Adding upstream remote: $UPSTREAM_REPO"
    git remote add upstream "$UPSTREAM_REPO"
fi

echo "Fetching upstream $UPSTREAM_BRANCH..."
git fetch upstream "$UPSTREAM_BRANCH"

CURRENT_UPSTREAM_SHA=$(git rev-parse upstream/"$UPSTREAM_BRANCH")

echo "================================================================================"
echo "UPSTREAM SYNC STATUS"
echo "================================================================================"
echo "  Last Synced Upstream SHA:  $LAST_SHA"
echo "  Current Upstream HEAD SHA: $CURRENT_UPSTREAM_SHA"
echo "================================================================================"

if [ "$LAST_SHA" = "$CURRENT_UPSTREAM_SHA" ]; then
    echo "Result: Already up-to-date with upstream $UPSTREAM_BRANCH."
    exit 0
fi

# Get list of upstream commits
COMMIT_COUNT=$(git rev-list --count "${LAST_SHA}..${CURRENT_UPSTREAM_SHA}")
echo "Found $COMMIT_COUNT new upstream commit(s):"
git log --oneline --reverse "${LAST_SHA}..${CURRENT_UPSTREAM_SHA}"
echo ""

# Generate and apply diff
DIFF_FILE=$(mktemp)
git diff "${LAST_SHA}..${CURRENT_UPSTREAM_SHA}" > "$DIFF_FILE"

if [ ! -s "$DIFF_FILE" ]; then
    echo "No diff generated between $LAST_SHA and $CURRENT_UPSTREAM_SHA."
    rm -f "$DIFF_FILE"
    echo "$CURRENT_UPSTREAM_SHA" > "$SHA_FILE"
    exit 0
fi

echo "Applying upstream diff..."
if ! git apply --3way "$DIFF_FILE" 2>/dev/null; then
    if ! git apply "$DIFF_FILE"; then
        echo "Error: Failed to apply upstream diff cleanly. Manual conflict resolution required." >&2
        rm -f "$DIFF_FILE"
        exit 1
    fi
fi
rm -f "$DIFF_FILE"

# Update tracked SHA
echo "$CURRENT_UPSTREAM_SHA" > "$SHA_FILE"
echo "Updated $SHA_FILE -> $CURRENT_UPSTREAM_SHA"
echo "Upstream patch applied successfully."
