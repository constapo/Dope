# Quickstart run: 001 free reel builder

**Date**: 2026-11-04 · **Where**: cloud container (Linux, 4 CPUs, Python 3.13, ffmpeg 6.1), branch
`claude/project-init-claude-integration-7rawyu`. Commands run with `PYTHONPATH=tools` (or `bin/reelkit`).

| Step | Result | Notes |
|---|---|---|
| Prerequisites | Pass | `reelkit setup` downloaded the Kokoro model to `~/.cache/kokoro` (earlier in the session) |
| 1. Offline tests | Pass | `88 passed, 1 deselected` (the deselected one is the slow real-Kokoro test, also passed when run alone) |
| 2. House-rule refusal | Pass | exit 2; named `από €500` in the Greek subtitle (Principle I) and "overhead" in the shot (Principle II/III) |
| 3. Build from own pictures | Pass | 1080x1920, 8.73 s; `review.md` lists Greek native review; re-run took 2.2 s with 7 cache hits in `build.log` |
| 4. Free generation | Pass | exit 3 with line 1 to review after 69 s (AI Horde, anonymous); still is a realistic worn-tile floor, no faces or text; after `--accept 1` the build wrote 5.2 s; `credits.md` shows `ai-horde` / `ai-generated`; `review.md` has the "illustration" label reminder |
| 5. Existing reel as a plan | Pass | `tiles-black-marble-90s.yaml`: same 19 lines, subtitles and order as `free-build/archive/build_tiles_photo.py`; 90.0 s |

## SC-002 timing (T047)

Edited one line of the tile reel (line 16 speech: "...cleaned and polished." → "...cleaned and polished
by hand.") and rebuilt with all other pictures, voice clips and video segments cached:

| Build | Time |
|---|---|
| First build with the per-line segment renderer (fills the cache) | 2 min 54 s |
| One-line edit rebuild | **14.8 s** (target < 2 min: pass) |
| Rebuild of the unchanged plan | 4.8 s |

`build.log` for the edited rebuild shows only `segment line 16: rendered`; every other line and the end
card were cache hits. Before per-line segment caching the same edit took 2 min 50 s (fail), which is why
`render.py` now renders each line to its own cached segment and joins them without re-encoding.

## Open items

- T041 (Video 01 landscape plan) not done: `free-build/build_v01.py` splits the Greek subtitles by time,
  not by sentence, so its lines cannot be mapped one-to-one without a native speaker re-cutting the Greek.
- `credits.md` leaves the Credit column empty for AI Horde stills; the source and licence columns are filled.
