#!/usr/bin/env bash
# Extract real brand tokens + logo from a live URL into brands/<name>/.
# Usage: brand-extract.sh <url> <name>
set -euo pipefail

URL="${1:?url}"; NAME="${2:?brand name}"
ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
OUT="$ROOT/brands/$NAME"; mkdir -p "$OUT"

export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1
TMP="$(mktemp -d)"
npx --yes hyperframes@latest capture "$URL" -o "$TMP/cap" --max-screenshots 3 --skip-vision --json >/dev/null 2>&1 || true

if [ -f "$TMP/cap/extracted/tokens.json" ]; then
  cp "$TMP/cap/extracted/tokens.json" "$OUT/tokens.json"; echo "wrote $OUT/tokens.json"
else
  echo "WARN: no tokens.json produced — check the URL / capture output"
fi
if ls "$TMP"/cap/assets/svgs/logo-*.svg >/dev/null 2>&1; then
  cp "$(ls "$TMP"/cap/assets/svgs/logo-*.svg | head -1)" "$OUT/logo.svg"; echo "wrote $OUT/logo.svg"
else
  echo "note: no logo SVG captured — add $OUT/logo.svg by hand"
fi
echo "review $OUT/tokens.json → cssVariables / colors / fonts for the composition palette"
