#!/usr/bin/env bash
# Đồng bộ vi-voice-rules.md giữa Google Drive (bản gốc) và plugin (bản sao dùng trong mọi phiên).
# Dùng:  sync_rules.sh            Drive -> plugin
#        sync_rules.sh --to-drive plugin -> Drive
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
COPY="$HERE/../../vi-voice/references/vi-voice-rules.md"
SRC="$(ls -d "$HOME"/Library/CloudStorage/GoogleDrive-*/"My Drive"/03_Mentoring/_system/rules/vi-voice.md 2>/dev/null | head -1 || true)"
if [ -z "$SRC" ]; then echo "Không thấy file vi-voice.md trên Drive" >&2; exit 1; fi
if [ "${1:-}" = "--to-drive" ]; then cp "$COPY" "$SRC"; echo "plugin -> Drive: $SRC"
else cp "$SRC" "$COPY"; echo "Drive -> plugin: $COPY"; fi
