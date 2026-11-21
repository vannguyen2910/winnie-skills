#!/bin/sh
# One-way sync: winnie-skills (source of truth) -> workspace-template toolkit (shipped copy).
# Only the skills listed in SKILLS are shipped to the course. Usage: [--check] (reports drift only)
set -e
SRC="$(cd "$(dirname "$0")/.." && pwd)/plugins/product-workspace/skills"
DST="${TOOLKIT_SKILLS:-$HOME/Developer/ai-design-workflow-class/workspace-template/toolkit/skills}"
SKILLS="stakeholder-map pestel-analysis survey interview user-voice-synthesis"
rc=0
for n in $SKILLS; do
  if [ "$1" = "--check" ]; then
    diff -rq "$SRC/$n" "$DST/$n" >/dev/null 2>&1 || { echo "DRIFT: $n"; rc=1; }
  else
    rsync -a --delete "$SRC/$n/" "$DST/$n/" && echo "synced: $n"
  fi
done
exit $rc
