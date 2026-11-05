#!/usr/bin/env bash
# Record a Claude Code (or any terminal) beat with VHS, then convert to a dense-keyframe MP4.
# Usage: capture-terminal.sh <script.tape> [out.mp4]
# The .tape MUST declare `Output <name>.mp4`. We render it headlessly, then re-encode with dense
# keyframes (HyperFrames seeks every frame; a sparse GOP freezes footage between keyframes — same
# reason capture.sh re-encodes the browser webm).
#
# The terminal is the CLI's "browser" — SANITIZE it like capture step 2 so a public video leaks
# nothing: record in a clean throwaway dir, `unset CLAUDE_CODE_CHILD_SESSION` (kills the
# "transcript saving is off" warning), and Escape onboarding popups. The template tape does this.
set -euo pipefail

TAPE="${1:?path to .tape}"; OUT_ARG="${2:-}"
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS="$SKILL/.vhs"; mkdir -p "$TOOLS"
export PATH="$HOME/go/bin:$TOOLS:$PATH"

# vhs (Charm) renders a .tape headlessly to video; ttyd + ffmpeg are its runtime deps.
# Headless chromium inside vhs launched clean on an AppArmor/Wayland host — no sandbox flag needed.
if ! command -v vhs >/dev/null; then
  command -v go >/dev/null || { echo "ERROR: need 'go' to install vhs (https://github.com/charmbracelet/vhs)"; exit 1; }
  echo "installing vhs (one-time)…"; GOBIN="$HOME/go/bin" go install github.com/charmbracelet/vhs@latest
fi
if ! command -v ttyd >/dev/null; then
  echo "fetching ttyd static binary (one-time)…"
  V="$(curl -fsSL https://api.github.com/repos/tsl0922/ttyd/releases/latest | grep -oP '"tag_name":\s*"\K[^"]+' || echo 1.7.7)"
  curl -fsSL -o "$TOOLS/ttyd" "https://github.com/tsl0922/ttyd/releases/download/${V}/ttyd.x86_64" && chmod +x "$TOOLS/ttyd"
fi

TAPEDIR="$(cd "$(dirname "$TAPE")" && pwd)"; TAPEFILE="$(basename "$TAPE")"
cd "$TAPEDIR"

RAW="$(grep -oP '^\s*Output\s+\K\S+\.mp4' "$TAPEFILE" | head -1)"
[ -n "$RAW" ] || { echo "ERROR: the tape must declare 'Output <name>.mp4'"; exit 1; }

vhs "$TAPEFILE"
[ -f "$RAW" ] || { echo "ERROR: vhs did not produce $RAW"; exit 1; }

OUT="${OUT_ARG:-$RAW}"
TMP="$(mktemp --suffix=.mp4)"
ffmpeg -v error -y -i "$RAW" -c:v libx264 -r 30 -g 30 -keyint_min 30 -sc_threshold 0 \
  -pix_fmt yuv420p -movflags +faststart "$TMP"
mv -f "$TMP" "$OUT"
echo "wrote $TAPEDIR/$OUT ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s)"
