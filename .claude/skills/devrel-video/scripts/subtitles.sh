#!/usr/bin/env bash
# Burn an SRT into a project's rendered video (a social / autoplay-muted cut).
# Soft subtitles need no burning — just ship the .srt next to the video (YouTube/LinkedIn read it,
# toggleable, one file per language). Use this only for hard-baked captions.
# Usage: subtitles.sh <project-dir> <captions.srt> [in.mp4] [out.mp4]
set -euo pipefail

PROJ="$(cd "${1:?project dir}" && pwd)"; SRT="${2:?path to .srt}"
IN="${3:-renders/out-web.mp4}"; OUT="${4:-renders/subtitled.mp4}"
cd "$PROJ"
srt="$(basename "$SRT")"
[ -f "$srt" ] || cp "$SRT" "$srt"   # libass resolves relative to cwd

ffmpeg -v error -y -i "$IN" \
  -vf "subtitles=$srt:force_style='FontName=DejaVu Sans,Fontsize=23,PrimaryColour=&H00FFFFFF,BackColour=&HA0000000,BorderStyle=4,Outline=0,Shadow=0,MarginV=34,Alignment=2'" \
  -c:a copy "$OUT"
echo "wrote $PROJ/$OUT"
echo "Soft-subs alternative: ship $srt next to the clean video — platforms show it toggleable, and one .srt per language covers 'alternative subtitles'."
