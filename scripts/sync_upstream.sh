#!/usr/bin/env bash
# Pull Dumpstarr stable and Dictionarry v2, rebuild the pruned profile and
# the layer, run the tests, and commit only when those tests pass.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

git clone --depth 1 --branch stable https://github.com/Dumpstarr/Database.git "$WORK/dumpstarr"
git clone --depth 1 --branch v2 https://github.com/Dictionarry-Hub/database.git "$WORK/dictionarry"
git clone --depth 1 --branch 1.1.0 https://github.com/Dictionarry-Hub/schema.git "$WORK/schema"

python3 scripts/sync_upstream.py \
  --schema "$WORK/schema/ops" \
  --dumpstarr "$WORK/dumpstarr" \
  --dictionarry "$WORK/dictionarry"

if [ -z "$(git status --porcelain -- ops tweaks .github/upstream.json)" ]; then
  echo "No upstream changes."
  exit 0
fi

export PCD_SCHEMA_PATH="$WORK/schema/ops"
python3 tests/test_database.py

if [ -n "$(git status --porcelain -- ops tweaks .github/upstream.json)" ]; then
  git add -- ops tweaks .github/upstream.json
  SHA="$(git -C "$WORK/dumpstarr" rev-parse --short HEAD)"
  git commit -m "chore(upstream): sync Dumpstarr Movies 2160p (${SHA})"
fi
