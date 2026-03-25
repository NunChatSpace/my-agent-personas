#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PERSONA_FILE="$SCRIPT_DIR/persona.md"
TARGETS_FILE="$SCRIPT_DIR/targets.txt"

# Validate
if [ ! -f "$PERSONA_FILE" ]; then
  echo "❌  persona.md not found at $PERSONA_FILE"
  exit 1
fi

if [ ! -f "$TARGETS_FILE" ]; then
  echo "❌  targets.txt not found at $TARGETS_FILE"
  exit 1
fi

echo "🔄  Syncing persona from: $PERSONA_FILE"
echo ""

success=0
skipped=0

while IFS= read -r target || [ -n "$target" ]; do
  # Skip empty lines and comments
  [[ -z "$target" || "$target" == \#* ]] && continue

  if [ ! -d "$target" ]; then
    echo "  ⚠️   Skipping (directory not found): $target"
    ((skipped++)) || true
    continue
  fi

  echo "  ✓  $target"
  python3 "$SCRIPT_DIR/inject.py" "$PERSONA_FILE" "$target/AGENTS.md"
  ((success++)) || true

done < "$TARGETS_FILE"

echo ""
echo "✅  Done — synced: $success, skipped: $skipped"