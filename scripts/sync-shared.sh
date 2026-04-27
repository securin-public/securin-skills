#!/usr/bin/env bash
# Mirror skills/_shared/ into each skill's references/_shared/ so individual
# skill folders are self-contained when extracted.
#
# Source of truth: skills/_shared/. Per-skill copies are generated.
#
# Usage:
#   scripts/sync-shared.sh           # rewrite all per-skill copies
#   scripts/sync-shared.sh --check   # exit non-zero if any copy is stale (CI)

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHARED="$ROOT/skills/_shared"
CHECK=0
[[ "${1:-}" == "--check" ]] && CHECK=1

if [[ ! -d "$SHARED" ]]; then
  echo "fatal: $SHARED not found" >&2
  exit 2
fi

stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT

# Build the canonical staging copy with a banner prepended to each markdown file.
cp -R "$SHARED/." "$stage/"
while IFS= read -r -d '' md; do
  rel="${md#$stage/}"
  banner="<!-- Mirrored from skills/_shared/${rel}. Do not edit here — edit the source and run scripts/sync-shared.sh. -->"
  { printf '%s\n\n' "$banner"; cat "$md"; } > "$md.tmp"
  mv "$md.tmp" "$md"
done < <(find "$stage" -type f -name '*.md' -print0)

drift=0
for skill_dir in "$ROOT"/skills/securin-*/; do
  dest="$skill_dir/references/_shared"
  if (( CHECK )); then
    if [[ ! -d "$dest" ]] || ! diff -rq "$stage" "$dest" >/dev/null 2>&1; then
      echo "drift: ${dest#$ROOT/}" >&2
      drift=1
    fi
  else
    rm -rf "$dest"
    mkdir -p "$(dirname "$dest")"
    cp -R "$stage" "$dest"
    echo "synced: ${dest#$ROOT/}"
  fi
done

if (( CHECK )) && (( drift )); then
  echo >&2
  echo "Per-skill _shared copies are out of sync. Run scripts/sync-shared.sh and commit." >&2
  exit 1
fi
