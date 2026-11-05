#!/usr/bin/env bash
# Build a YouTube thumbnail (1280x720 JPG, <2MB) from a project's thumbnail.html + a hero frame of capture.mp4.
# Every DevRel video ships one (not just the QA contact sheet). Usage: thumbnail.sh <project-dir> [hero_time_s]
set -euo pipefail
PROJ="$(cd "${1:?project dir}" && pwd)"; HERO_T="${2:-2.0}"
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
[ -f "$PROJ/thumbnail.html" ] || { echo "thumbnail: need $PROJ/thumbnail.html (copy templates/thumbnail.html + fill)"; exit 1; }
[ -f "$PROJ/capture.mp4" ]   || { echo "thumbnail: need $PROJ/capture.mp4 (run capture.sh first)"; exit 1; }
mkdir -p "$PROJ/renders"

echo "[thumbnail] hero frame @ ${HERO_T}s -> renders/hero.png"
ffmpeg -v error -y -ss "$HERO_T" -i "$PROJ/capture.mp4" -frames:v 1 "$PROJ/renders/hero.png"

export PLAYWRIGHT_MCP_SANDBOX=false
BIN="$SKILL/.pw/node_modules/.bin/playwright-cli"
[ -x "$BIN" ] || ( mkdir -p "$SKILL/.pw" && cd "$SKILL/.pw" && npm i @playwright/cli@latest >/dev/null 2>&1 )
export PATH="$SKILL/.pw/node_modules/.bin:$PATH"

# playwright-cli blocks file:// — serve the project over http so thumbnail.html + renders/hero.png load.
PORT="${THUMB_PORT:-8757}"
python3 -m http.server "$PORT" --directory "$PROJ" >/dev/null 2>&1 &
SRV=$!; trap 'kill $SRV 2>/dev/null || true' EXIT
sleep 1

echo "[thumbnail] render 1280x720"
playwright-cli open   >/dev/null 2>&1
playwright-cli resize 1280 720 >/dev/null 2>&1
playwright-cli goto "http://localhost:$PORT/thumbnail.html" >/dev/null 2>&1
playwright-cli eval "() => new Promise(r => setTimeout(r, 1200))" >/dev/null 2>&1  # fonts + hero img settle
playwright-cli screenshot --filename="$PROJ/renders/thumbnail.png" >/dev/null 2>&1
playwright-cli close  >/dev/null 2>&1

echo "[thumbnail] -> JPG (<2MB)"
ffmpeg -v error -y -i "$PROJ/renders/thumbnail.png" -q:v 3 "$PROJ/renders/thumbnail.jpg"
echo "[thumbnail] ✓ $PROJ/renders/thumbnail.jpg ($(du -h "$PROJ/renders/thumbnail.jpg" | cut -f1), $(ffprobe -v error -show_entries stream=width,height -of csv=p=0:s=x "$PROJ/renders/thumbnail.jpg"))"
