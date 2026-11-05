#!/usr/bin/env bash
# variant.sh — regenerate a narrated project in a DIFFERENT VOICE, end to end.
#
# Usage:  variant.sh <project_dir> <voice> [--no-avatar]
#   voice: male leo/dan/zac, female leah/tara/jess/mia/zoe (match the presenter)
#
# Does the whole voice swap deterministically: re-TTS the lines -> narrate.py (voice.wav + captions +
# timing.json) -> retime.py (apply the new timing to index.html) -> music bed + ducked mix -> re-lip-sync
# the avatar bubbles to the new voice (if the project has one) -> render. Output: renders/out-<voice>.mp4.
# Needs <project>/narrate.py (copy templates/narrate.py + adapt: SPOKEN lines, caps, captions).
set -euo pipefail
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env.sh"

PROJ="${1:?project dir}"; VOICE="${2:?voice (leo/dan/zac/leah/tara/jess/mia/zoe)}"
NO_AVATAR=0; [[ "${3:-}" == "--no-avatar" ]] && NO_AVATAR=1
SC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[ -f "$PROJ/narrate.py" ] || { echo "variant: need $PROJ/narrate.py (copy templates/narrate.py + adapt)"; exit 1; }

echo "[variant] TTS the narration lines in voice '$VOICE'"
mapfile -t LINES < <(python3 "$PROJ/narrate.py" --lines)
i=1; for line in "${LINES[@]}"; do
  "$SC/tts.sh" "$line" "$PROJ/vo$i.wav" "$VOICE" >/dev/null
  i=$((i + 1))
done

echo "[variant] assemble voice.wav + captions + timing.json"
( cd "$PROJ" && python3 narrate.py >/dev/null )

echo "[variant] re-time the composition to the new voice"
python3 "$SC/retime.py" "$PROJ"

echo "[variant] music bed + ducked mix"
TOTAL="$(python3 -c "import json;print(json.load(open('$PROJ/timing.json'))['total'])")"
python3 "$SC/gen-bgm.py" "$PROJ/bgm.wav" "$TOTAL" >/dev/null
"$SC/mix-audio.sh" "$PROJ/bgm.wav" "$PROJ/voice.wav" "$PROJ/narration-mix.mp3" >/dev/null

# avatar bubbles (only if this project uses one): re-lip-sync intro (vo1) + cta (vo5) to the new voice
PLATE="$(sed -nE 's/^[[:space:]]*avatar_plate:[[:space:]]*//p' "$PROJ/brief.yaml" 2>/dev/null | sed -E 's/[[:space:]]*#.*$//' | tr -d '"' | head -1)"
PLATE="${PLATE/#\~/$HOME}"
if [ "$NO_AVATAR" = 0 ] && [ -n "$PLATE" ] && grep -q 'id="avatar"' "$PROJ/index.html"; then
  HOST="${AVATAR_HOST:?set AVATAR_HOST to the ssh target with a LatentSync checkout (see scripts/_env.sh)}"
  echo "[variant] re-lip-sync avatar bubbles to '$VOICE' (GPU on $HOST, ~10 min)…"
  ssh -o ConnectTimeout=45 "$HOST" 'sudo systemctl stop ollama' >/dev/null 2>&1 || true
  AVATAR_HOST="$HOST" "$SC/avatar.sh" "$PLATE" "$PROJ/vo1.wav" "$PROJ/avatar-face.mp4"
  AVATAR_HOST="$HOST" "$SC/avatar.sh" "$PLATE" "$PROJ/vo5.wav" "$PROJ/avatar-cta.mp4"
  ssh -o ConnectTimeout=45 "$HOST" 'sudo systemctl start ollama' >/dev/null 2>&1 || true
else
  echo "[variant] no avatar for this project (skipped)"
fi

echo "[variant] render"
"$SC/render-qa.sh" "$PROJ" >/dev/null
cp "$PROJ/renders/out.mp4" "$PROJ/renders/out-$VOICE.mp4"
echo "[variant] ✓ $PROJ/renders/out-$VOICE.mp4  (voice=$VOICE, ${TOTAL}s)"
