# Implementation Plan: Free Reel and Video Builder Pipeline

**Branch**: `001-free-reel-builder` (work committed on `claude/project-init-claude-integration-7rawyu`)
| **Date**: 2026-11-04 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-free-reel-builder/spec.md`

## Summary

Replace the four one-off build scripts in `inonda-youtube-videos/free-build/` with one reusable
tool, `reelkit`. The content maker writes a YAML reel plan (lines of English speech, Greek
subtitle, optional label, picture); `reelkit` checks it against the house rules, obtains missing
pictures from free sources only (own files, licensed free stock, AI Horde generation with a
human review step), voices each line with the free Kokoro voice, renders every picture with the
approved handheld-phone camera move, burns in Greek subtitles, appends the bilingual end card, and
writes the video with a credits list and a pre-publish review list. Everything is cached so a
one-line edit rebuilds in under two minutes. See [research.md](research.md) for each decision.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: Pillow, numpy (installed); PyYAML (installed); jsonschema; kokoro-onnx
0.6.x + soundfile (free local TTS); ffmpeg 6.x (system binary); AI Horde HTTP API (free,
anonymous) via the standard library

**Storage**: files only. Plans in `inonda-youtube-videos/reels/`; builds and caches in
`media/reels/<slug>/` (git-ignored)

**Testing**: pytest; offline unit and integration tests with a stub voice engine and bundled test
stills; one opt-in slow test with real Kokoro

**Target Platform**: Linux (this cloud container) and the owner's computer (macOS/Linux/WSL) with
Python 3.13 and ffmpeg

**Project Type**: command-line tool (single Python package)

**Performance Goals**: rebuild after a one-line edit < 2 min for a 90 s reel (SC-002); full first
build dominated by AI Horde queue (minutes per picture, run in parallel)

**Constraints**: zero spend, no paid APIs or credits (Principle IV); works without a GPU; runs
offline once pictures and the voice model are cached; 1080x1920 (reel) or 1920x1080 (video) at
30 fps

**Scale/Scope**: one content maker; plans of 1-30 lines, 15-180 s; ~20 videos planned
(`scripts/v01-v20`) plus reels

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | How the design complies | Status |
|---|---|---|
| I. No prices, no budget talk | Rule checker refuses currency, price and budget words (EN + GR) in title, speech, subtitles, labels and shot descriptions before any work (FR-009) | Pass |
| II. Real-looking footage only | Shots asking for drawings, cartoons, animation, illustration are refused; generation prompts force photorealism with a negative prompt; no drawn scenes are produced (the drawn-preview mode of `build_tiles_preview.py` is not carried over) | Pass |
| III. Handheld phone camera | Motion is always a level, chest-height frame with hand shake; no angle field exists; overhead/drone/ceiling/floor-level shot descriptions are refused (FR-010) | Pass |
| IV. Free and licensed sources only | Sources limited to own files, allowed free-stock licences and AI Horde; payment-required answers count as failure; no paid tool is a dependency; credits list for every picture (FR-006, FR-008) | Pass |
| V. Honest footage | Generated stills need human acceptance on a contact sheet; prompts exclude faces, text, logos; review list reminds to label AI shots that could pass as a real Inonda job | Pass |
| VI. Bilingual and reviewed | Every line requires a Greek subtitle; review list always includes Greek native review; placeholders are refused | Pass |
| Production standards | Default voice Kokoro `am_michael` 0.90; Inonda shared AI style; media kept out of git | Pass |

No violations, so Complexity Tracking is empty.

**Post-design re-check (after Phase 1)**: the data model, schema and CLI contract add no source,
angle or text path that bypasses the checks above. Still pass.

## Project Structure

### Documentation (this feature)

```text
specs/001-free-reel-builder/
├── plan.md              # This file
├── research.md          # Phase 0 decisions
├── data-model.md        # Entities and fields
├── quickstart.md        # End-to-end validation guide
├── contracts/
│   ├── reel-plan.schema.json   # Reel plan file format
│   └── cli.md                  # Command-line contract
├── checklists/requirements.md
└── tasks.md             # Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
tools/reelkit/
├── __main__.py          # CLI: check, pictures, build, new, setup
├── plan.py              # load YAML, schema validation, defaults
├── rules.py             # house-rule checker
├── rules.yaml           # rule data (words, patterns, messages); one line per owner rule
├── voice.py             # Kokoro engine, Edge fallback, stub engine for tests, clip cache
├── pictures/
│   ├── __init__.py      # source order, records, contact sheet
│   ├── own.py           # supplied files
│   ├── stock.py         # licensed stock download
│   └── horde.py         # AI Horde generation (parallel, retries, payment-demand = fail)
├── motion.py            # handheld frame + shake (ported from build_tiles_photo.py)
├── render.py            # timeline, subtitles, labels, end card, ffmpeg pipe
├── endcard.py           # Inonda bilingual end card (from build_tiles_preview.py)
├── report.py            # credits.md, review.md, build.log
├── cache.py             # content-hash keys
├── requirements.txt
└── tests/
    ├── test_plan.py
    ├── test_rules.py
    ├── test_timing.py
    ├── test_cache.py
    ├── test_build_offline.py
    ├── stills/          # small test images
    └── plans/           # good and bad example plans

inonda-youtube-videos/reels/   # reel plans (YAML), committed
media/reels/                   # build outputs, git-ignored
```

**Structure Decision**: a single Python package under `tools/`, next to the existing
`tools/higgsfield` and `tools/wasmer`, run with `python3 -m reelkit` (with `tools/` on the path via
a tiny launcher or `pip install -e`). Plans live with the other Inonda content; outputs go to
`media/`, which the constitution keeps out of git. The old `free-build/` scripts stay until User
Story 4 proves the plans reproduce them, then move to an `archive/` folder.

## Complexity Tracking

No constitution violations to justify.
