#!/bin/sh
# One-way sync: winnie-skills (source of truth) -> workspace-template toolkit (shipped copy).
# Usage: scripts/sync-to-toolkit.sh [--check]   (--check only reports drift, changes nothing)
set -e
SRC="$(cd "$(dirname "$0")/.." && pwd)/plugins/product-research/skills"
DST="${TOOLKIT_SKILLS:-$HOME/Developer/ai-design-workflow-class/workspace-template/toolkit/skills}"
rc=0
for s in "$SRC"/*/; do
  n=$(basename "$s")
  if [ "$1" = "--check" ]; then
    diff -rq "$s" "$DST/$n" >/dev/null 2>&1 || { echo "DRIFT: $n"; rc=1; }
  else
    rsync -a --delete "$s" "$DST/$n/" && echo "synced: $n"
  fi
done
exit $rc
