---

description: "Task list for the free reel and video builder pipeline (reelkit)"
---

# Tasks: Free Reel and Video Builder Pipeline

**Input**: Design documents from `/specs/001-free-reel-builder/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md)

**Tests**: Included. The plan and quickstart call for offline pytest tests, and SC-004 needs a
rule-checker test set with 100% refusal.

**Organization**: Tasks are grouped by user story so each story can be built and tested on its own.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel (different files, no dependency on an unfinished task)
- **[Story]**: US1-US4 from spec.md
- Paths are from the repository root. The package lives in `tools/reelkit/` and runs as
  `python3 -m reelkit` with `tools/` on `PYTHONPATH` (see T003).

## Constitution reminders for every task

No prices or budget words anywhere, including test fixtures meant to pass; no drawn or cartoon
output; camera always level and chest-height; no paid services or credits; generated pictures
never show faces, text or logos; every line has a Greek subtitle.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: create the package skeleton and tooling.

- [X] T001 Create the package layout from plan.md: `tools/reelkit/{__init__.py,__main__.py,plan.py,rules.py,rules.yaml,voice.py,motion.py,render.py,endcard.py,report.py,cache.py}`, `tools/reelkit/pictures/{__init__.py,own.py,stock.py,horde.py}`, `tools/reelkit/tests/{stills,plans}/` and an empty `inonda-youtube-videos/reels/` folder with a `.gitkeep`
- [X] T002 [P] Write `tools/reelkit/requirements.txt` with `pillow`, `numpy`, `pyyaml`, `jsonschema`, `kokoro-onnx>=0.6,<0.7`, `soundfile`, `pytest` (no paid-service SDKs)
- [X] T003 [P] Add `pytest.ini` at the repo root (`pythonpath = tools`, `testpaths = tools/reelkit/tests`, marker `slow` for tests needing the real Kokoro model or network) and a launcher `bin/reelkit` (bash: `PYTHONPATH="$(dirname "$0")/../tools" exec python3 -m reelkit "$@"`, executable)
- [X] T004 [P] Add `media/reels/` to `.gitignore` so builds, caches and licensed media stay out of git
- [X] T005 [P] Create three small test stills (solid-colour JPEGs, 1600x1200, 1200x1600, 2000x1000, made with Pillow by a script in `tools/reelkit/tests/make_stills.py`) in `tools/reelkit/tests/stills/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: plan loading, caching and the CLI shell that every story uses.

**⚠️ No user story work starts until this phase is done.**

- [X] T006 Copy `specs/001-free-reel-builder/contracts/reel-plan.schema.json` to `tools/reelkit/reel-plan.schema.json` (packaged copy used at runtime)
- [X] T007 Implement `tools/reelkit/plan.py`: `load_plan(path) -> ReelPlan` reads YAML (UTF-8), validates with the schema, fills defaults (voice `kokoro`/`am_michael`/`0.9`; end card `6` s `inonda-bilingual`; move `zoom_from 1.00`, `zoom_to 1.07`, `slide_x 0`, `slide_y 0`, `shake normal`), and returns dataclasses `ReelPlan`, `Line`, `Picture`, `Move` per data-model.md. Enforce: `slug` matches `^[a-z0-9]+(-[a-z0-9]+)*$`; `format` is `reel` (1080x1920) or `video` (1920x1080); `lines` has at least 1 item; every line has non-empty `speech` and `greek`; a `reuse` picture must point to an earlier line number (1-based); a `stock` picture's licence must be one of `mixkit-free`, `pexels`, `pixabay`, `coverr`, `cc0`, `cc-by`, and `cc-by` requires `credit`. Errors are a list of `PlanError(line, field, message)`
- [X] T008 [P] Implement `tools/reelkit/cache.py`: `key(*parts) -> str` (sha256 of a stable JSON dump, first 16 hex chars), `voice_key(text, engine, name, speed)`, `picture_key(picture_spec)`, and `build_dir(slug, out=None)` returning `media/reels/<slug>/` (created with `voice/` and `pictures/` subfolders)
- [X] T009 Implement the CLI shell in `tools/reelkit/__main__.py` with argparse subcommands `check`, `pictures`, `build`, `new`, `setup` and the exit codes from contracts/cli.md (0 ok, 2 rule/structure problems, 3 pictures awaiting review, 4 pictures missing, 5 voice engine unavailable). `check` prints `OK: <n> lines, <format>` or one `line <i>: <field>: <message>` per problem. Wire `check` to `plan.load_plan` now; other subcommands raise "not implemented" until their stories land
- [X] T010 [P] Implement `new` in `tools/reelkit/__main__.py`: writes `inonda-youtube-videos/reels/<slug>.yaml` with a comment header explaining each field and two example lines (one `file` picture, one `generate` picture) that pass every house rule; refuses to overwrite an existing file
- [X] T011 [P] Tests in `tools/reelkit/tests/test_plan.py`: a valid minimal plan loads with defaults applied; missing `greek`, bad slug, unknown licence, `cc-by` without credit, `reuse` pointing forward, and an unknown key are each reported with the right line and field
- [X] T012 [P] Tests in `tools/reelkit/tests/test_cache.py`: same inputs give the same key; changing text, voice, speed or picture spec changes the key

**Checkpoint**: `bin/reelkit check` validates plan structure; tests pass.

---

## Phase 3: User Story 1 - Build a reel from a written reel plan (Priority: P1) 🎯 MVP

**Goal**: one command turns a plan whose pictures are all supplied files into a finished video
with English voice, Greek subtitles, handheld camera moves and the end card.

**Independent Test**: `bin/reelkit build tools/reelkit/tests/plans/two-lines-own-photos.yaml`
with the stub voice produces a 1080x1920 30 fps video whose length is speech + gaps + end card,
with `credits.md` and `review.md`; a second run reuses every cached clip.

### Tests for User Story 1

- [X] T013 [P] [US1] Create `tools/reelkit/tests/plans/two-lines-own-photos.yaml`: format `reel`, two lines with English speech, Greek subtitles and `file:` pictures pointing at the test stills, one line with a label `BEFORE · ΠΡΙΝ`; no prices, budgets or placeholders
- [X] T014 [P] [US1] Tests in `tools/reelkit/tests/test_timing.py` for `render.timeline()`: lead-in 0.4 s, gap 0.35 s between lines, each line lasts max(speech length + gap, `min_seconds`), subtitle shown from line start to speech end + 0.3 s, end card appended last, total = sum of spans + end card
- [X] T015 [US1] Integration test `tools/reelkit/tests/test_build_offline.py`: builds the two-line plan with `voice.StubEngine` (sine-free silence of length proportional to word count) into a tmp folder; asserts with `ffprobe` that the mp4 is 1080x1920, 30 fps, has audio, and duration matches `timeline()` within 0.1 s; asserts `credits.md` lists both files as `own`; asserts `review.md` contains "Greek native review"; re-runs and asserts `build.log` reports 2 voice cache hits and 0 new clips; edits line 2's speech and asserts exactly 1 new clip

### Implementation for User Story 1

- [X] T016 [P] [US1] Implement `tools/reelkit/voice.py`: `Engine` protocol `speak(text) -> (samples: np.ndarray, sample_rate: int)`; `KokoroEngine(name, speed)` loading `kokoro-v1.0.onnx` and `voices-v1.0.bin` from `~/.cache/kokoro` (lang `en-us`); `EdgeEngine` (optional, imported lazily, `en-GB-ThomasNeural`, rate -3%, pitch -14Hz, as in `inonda-youtube-videos/free-build/build_reel_v01_george.py`); `StubEngine` for tests; `voice_lines(plan, build_dir, engine)` that writes one WAV per line to `voice/<voice_key>.wav`, reusing existing files, and logs hits/misses. Raise a clear error (CLI exit 5) when the Kokoro model files are missing, telling the user to run `bin/reelkit setup`
- [X] T017 [P] [US1] Implement `setup` in `tools/reelkit/__main__.py`: downloads `kokoro-v1.0.onnx` and `voices-v1.0.bin` into `~/.cache/kokoro` from the Hugging Face repo `onnx-community/Kokoro-82M-v1.0-ONNX` (free; GitHub release assets are blocked in the cloud container), skipping files already present, and prints where they are
- [X] T018 [P] [US1] Implement `tools/reelkit/motion.py` by porting `shake(n, seed, amp)`, `frame(src, p, z0, z1, sx, sy, jx, jy, rot)` and `load_still()` (scale to 118 % of the frame, `OVERSIZE = 1.18`) from `inonda-youtube-videos/free-build/build_tiles_photo.py`, parameterised by frame width/height; shake amplitudes per `Move.shake`: `still` (0, 0, 0), `normal` (9 px, 7 px, 0.35°), `strong` (14 px, 11 px, 0.5°). Horizon stays level apart from the tiny roll; no other angle parameter exists. A still with a different aspect ratio is centre-cropped and the crop is reported to the caller
- [X] T019 [P] [US1] Implement `tools/reelkit/endcard.py` by porting `end_card()` and the colours (`NAVY (22,35,43)`, `ACCENT (79,195,247)`), fonts (DejaVu Sans Bold/Regular) and text from `inonda-youtube-videos/free-build/build_tiles_preview.py`, sized for both `reel` and `video` formats; silent, bilingual, no prices
- [X] T020 [US1] Implement `tools/reelkit/render.py`: `timeline(plan, clip_lengths)` per T014; `render(plan, build_dir, pictures, clips)` that concatenates voice clips with gaps and the silent end card into `voice.wav`, then pipes RGB frames to ffmpeg (`libx264 -crf 19 -preset medium -pix_fmt yuv420p`, AAC 160k, `+faststart`) exactly as `build_tiles_photo.py` does: picture with handheld move per line, label box top-left when set (accent colour if it contains `AFTER`), Greek subtitle wrapped to at most 2 lines above the bottom 20 % safe area, end card last. Writes `<slug>.mp4`. Subtitles needing more than 2 lines are drawn on 2 lines and reported as a warning
- [X] T021 [P] [US1] Implement `tools/reelkit/pictures/own.py` and the `file`/`reuse` path in `tools/reelkit/pictures/__init__.py`: `obtain(plan, build_dir)` returns one `PictureRecord` per line (`source: own`, `licence: own`, `ai_generated` from the plan, `accepted: true`), resolving `reuse` to the earlier line's record; missing files are listed and cause exit 4
- [X] T022 [P] [US1] Implement `tools/reelkit/report.py`: `write_credits(records, path)` (one row per picture: line, file, source, licence, credit), `write_review(plan, records, warnings, path)` always listing "Greek native review before publishing", plus "Add an 'illustration' label" for every `ai_generated` picture, plus all warnings; `write_log(path, entries)`; and the length warning when `target_seconds` is set and the video differs by more than 2 s (FR-014)
- [X] T023 [US1] Wire `build` in `tools/reelkit/__main__.py`: load plan → obtain pictures → voice lines → render → write credits, review and log → print `wrote <path> <seconds>s` and warnings. Supports `--out DIR`
- [X] T024 [US1] Run `python3 -m pytest -q` and the quickstart step 3 command; fix until both pass

**Checkpoint**: US1 is a working MVP: any plan built from own photos produces a compliant video.

---

## Phase 4: User Story 2 - Get missing pictures from free sources (Priority: P2)

**Goal**: lines with `stock` or `generate` pictures get them for free, with source and licence
recorded and generated stills reviewed before use.

**Independent Test**: `bin/reelkit pictures tools/reelkit/tests/plans/one-generated-line.yaml`
exits 3 with a contact sheet; after `--accept 1`, `build` succeeds and `credits.md` lists the
picture as `ai-horde`, `ai-generated`. Nothing is paid for.

### Tests for User Story 2

- [X] T025 [P] [US2] Create `tools/reelkit/tests/plans/one-generated-line.yaml` (one `generate:` line describing "close-up of cracked beige 1990s floor tiles in a Cyprus apartment, natural daylight") and `tools/reelkit/tests/plans/one-stock-line.yaml` (one `stock:` line with a Mixkit URL and `licence: mixkit-free`)
- [X] T026 [P] [US2] Tests in `tools/reelkit/tests/test_horde.py` using a fake HTTP layer (no network): prompt contains the shared Inonda style and the negative prompt; a 402 or a response mentioning payment/kudos purchase is treated as failure and never retried with another account; after 3 failed attempts the line is reported missing (exit 4) and earlier results are kept; parallel requests take the first good result
- [X] T027 [P] [US2] Tests in `tools/reelkit/tests/test_pictures.py`: stock download is cached by key and recorded with its licence and credit; generated pictures start `accepted: false` and block `build` with exit 3; `--accept 1` and `--accept-all` flip them; `--retry 1` deletes the file and requests a new one

### Implementation for User Story 2

- [X] T028 [P] [US2] Implement `tools/reelkit/pictures/stock.py`: download the URL once (standard library `urllib`, honouring `HTTPS_PROXY`), save under `pictures/<key>.<ext>`, record `source` (host name, e.g. `mixkit`), `licence`, `credit`; for a page URL rather than a media file, fail with a message asking for the direct file link. Video clips (`.mp4`) are supported by taking a still from the middle with ffmpeg in v1, noted in the review list
- [X] T029 [P] [US2] Implement `tools/reelkit/pictures/horde.py` against the AI Horde v2 API (`https://aihorde.net/api/v2/generate/async`, poll `/generate/check/<id>`, fetch `/generate/status/<id>`), anonymous key `0000000000`, photoreal SDXL model, size within 768x1344 (portrait for `reel`, landscape for `video`), prompt = `describe` + shared style ("Photorealistic, handheld documentary look, natural Mediterranean daylight, warm slightly desaturated tones, shallow depth of field, typical Cyprus home, no faces, no on-screen text, no logos") + negative prompt ("people, faces, text, letters, logos, watermark, cartoon, illustration, drawing, painting, 3d render, anime, overhead, top-down, aerial, drone, bird's-eye, fisheye"); 2 parallel requests per line, first good one wins; max 3 attempts; timeout 15 min per attempt; any payment demand counts as failure. Records `source: ai-horde`, `licence: ai-generated`, `ai_generated: true`, `accepted: false`, `attempts`
- [X] T030 [US2] Extend `tools/reelkit/pictures/__init__.py`: source order own → stock → generate per line; write `pictures/index.json`; build `contact-sheet.jpg` (thumbnails of all generated stills, labelled with line numbers and acceptance state); implement `--accept LINE...`, `--accept-all`, `--retry LINE...`
- [X] T031 [US2] Wire the `pictures` subcommand in `tools/reelkit/__main__.py` (exit 0/3/4 per contracts/cli.md) and make `build` stop with exit 3 or 4 when pictures are pending or missing
- [X] T032 [US2] Run the offline tests, then quickstart step 4 with the network (one real AI Horde generation) and check the contact sheet by eye: realistic, no faces, no text, level phone-height view

**Checkpoint**: US1 + US2: plans can mix own, stock and generated pictures.

---

## Phase 5: User Story 3 - House-rule check before the video is built (Priority: P3)

**Goal**: plans that break the constitution are refused before any download or render, with
each problem named.

**Independent Test**: `bin/reelkit check tools/reelkit/tests/plans/bad-price-and-angle.yaml`
exits 2 naming the `€` amount and the "overhead view" shot.

### Tests for User Story 3

- [X] T033 [P] [US3] Create `tools/reelkit/tests/plans/bad-price-and-angle.yaml` (a subtitle with `από €500` and a `generate:` shot "overhead view of a bathroom floor")
- [X] T034 [P] [US3] Rule test set in `tools/reelkit/tests/test_rules.py`, parametrised, each case must be refused and name its field: `from €300`, `under 500 euros`, `€45 per m²`, `only 99 EUR`, `$200`, `£150`, `a budget kitchen`, `on a budget`, `what it costs`, `save here, spend there`, `without spending a fortune`, `cheap tiles`, `προϋπολογισμός`, `τιμή`, `κόστος`, `ευρώ`, `φθηνά`, `[ADD job details]`, `TODO`, shots `top-down view`, `overhead`, `aerial`, `drone shot`, `from the ceiling`, `bird's-eye`, `floor-level`, `cartoon`, `drawing`, `illustration`, `animated`. And pass cases that must NOT be refused: `We give a clear written quote`, `free inspection`, `every job is different`, `two days of work`, `3 coats of sealant`, `1990s tiles` (SC-004: 100 % of refuse cases refused, 0 false refusals in the pass set)

### Implementation for User Story 3

- [X] T035 [P] [US3] Write `tools/reelkit/rules.yaml`: rule groups `money` (currency symbols €, $, £; words euro/euros/EUR/ευρώ; patterns "from/under/only/just + number", "number + per m²/sqm/m2", Greek "από €"), `budget` (budget, afford, cheap, cost/costs, price/prices/pricing, fortune, "save … spend", προϋπολογισμός, φθηνό/φτηνό/φθηνά, κόστος, τιμή/τιμές), `placeholder` (`[ADD`, `TODO`, `[...]`, `XXX`), `forbidden_shot` (drawing, drawn, cartoon, animation, animated, illustration, illustrated, sketch, top-down, overhead, aerial, drone, crane, ceiling view, from the ceiling, bird's-eye, floor-level, worm's-eye, low angle); each group has the constitution principle it enforces and a message template. Word matching is case-insensitive and on word boundaries so "price" does not match inside other words
- [X] T036 [US3] Implement `tools/reelkit/rules.py`: `check(plan) -> list[PlanError]` applying `money`, `budget` and `placeholder` to `title`, every `speech`, `greek` and `label`, and `forbidden_shot` plus `placeholder` to every `generate` description; message format `price mentioned ("από €500") — Principle I forbids prices`
- [X] T037 [US3] Run `rules.check` inside `check` and at the start of `build` and `pictures` in `tools/reelkit/__main__.py`, before any network or rendering work (exit 2 on any problem)
- [X] T038 [US3] Extend `report.write_review` in `tools/reelkit/report.py` with a fixed pre-publish checklist taken from the constitution's quality gate: no prices or budget talk, no drawings, correct camera angle, every cut licensed and credited, AI shots labelled, Greek reviewed, no placeholders

**Checkpoint**: US1-US3 done: the tool refuses non-compliant plans and produces a review list.

---

## Phase 6: User Story 4 - Make the existing reels with the new pipeline (Priority: P4)

**Goal**: the reels made by one-off scripts become plans and build with `reelkit`.

**Independent Test**: building `inonda-youtube-videos/reels/tiles-black-marble-90s.yaml` gives
the same 19 lines, subtitles and order as `build_tiles_photo.py`, at 90 s ± 1 s.

- [X] T039 [P] [US4] Convert the `LINES` list of `inonda-youtube-videos/free-build/build_tiles_photo.py` to `inonda-youtube-videos/reels/tiles-black-marble-90s.yaml`: 19 lines with the same speech, Greek, labels and moves (zoom from/to, slide x/y), `format: reel`, `target_seconds: 90`, pictures as `file:` paths into a stills folder the owner supplies (document the folder in a comment) or `generate:` descriptions where no still exists
- [X] T040 [P] [US4] Convert `inonda-youtube-videos/free-build/build_reel_v01_george.py` (v01 reel with Greek subtitles) to `inonda-youtube-videos/reels/v01-bathroom-reel.yaml`; replace any Pollinations-only pictures with `generate:` lines (AI Horde)
- [ ] T041 [P] [US4] Convert `inonda-youtube-videos/free-build/build_v01.py` (Video 01, landscape) to `inonda-youtube-videos/reels/v01-bathroom-video.yaml` with `format: video`; lines that need real footage of the owner, jobs or clients are `file:` pictures pointing at a `real-footage/` folder, never generated (Principle V)
- [X] T042 [US4] Run `bin/reelkit check` on all three plans and fix any rule problems they reveal; build the tile reel and compare line order, subtitles and length with the old output (90 s ± 1 s)

**Checkpoint**: all stories done; old scripts are no longer needed.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T043 [P] Write `tools/reelkit/README.md`: what it does, install, `setup`, the four commands with examples, plan format summary linking to the schema, free sources and why paid ones are excluded
- [X] T044 [P] Update `inonda-youtube-videos/README.md`: new reels are made with `reelkit` from plans in `reels/`; link to `tools/reelkit/README.md`
- [X] T045 Move the four old builders from `inonda-youtube-videos/free-build/` to `inonda-youtube-videos/free-build/archive/` with a one-line note that `reelkit` replaces them (only after T042 passes)
- [X] T046 Run every step of `specs/001-free-reel-builder/quickstart.md` and record results in `specs/001-free-reel-builder/checklists/quickstart-run.md`
- [X] T047 Measure SC-002: edit one line of the tile-reel plan and time the rebuild (must be < 2 min); note it in the quickstart run file

---

## Dependencies & Execution Order

### Phase dependencies

- Setup (Phase 1) → Foundational (Phase 2) → user stories.
- US1 (P1) depends only on Phase 2.
- US2 (P2) depends on Phase 2 and extends the picture layer from US1 (T021); it can start once T021 exists.
- US3 (P3) depends only on Phase 2 (T007, T009); it can run in parallel with US1/US2.
- US4 (P4) needs US1 (build) and, for `generate:` lines, US2; its checks need US3.
- Polish after the stories it documents.

### Within each story

Tests and fixtures first, then modules, then CLI wiring, then the run/verify task.

### Parallel opportunities

- Phase 1: T002-T005 together.
- Phase 2: T008, T010, T011, T012 together after T007.
- US1: T013, T014 together; T016, T017, T018, T019, T021, T022 together (different files); then T020 → T023 → T024.
- US2: T025-T027 together; T028 and T029 together; then T030 → T031 → T032.
- US3: T033-T035 together; then T036 → T037; T038 independent.
- US4: T039-T041 together; then T042.

### Parallel example: User Story 1

```text
Task: "T016 [US1] voice.py (Kokoro, Edge, Stub engines + clip cache)"
Task: "T018 [US1] motion.py (port handheld frame + shake)"
Task: "T019 [US1] endcard.py (port Inonda bilingual end card)"
Task: "T022 [US1] report.py (credits, review, log)"
```

## Implementation Strategy

### MVP first (User Story 1 only)

1. Phases 1-2.
2. Phase 3 (US1): a reel from own photos, with voice, Greek subtitles, handheld moves, end card.
3. Stop and validate with quickstart step 3; the owner can already make reels from real job photos.

### Incremental delivery

1. + US2: free stock and AI Horde pictures with review.
2. + US3: automatic house-rule refusal (can be pulled before US2 if rule safety is wanted first).
3. + US4: old reels converted, old scripts archived.

## Notes

- [P] tasks touch different files and have no unfinished dependency.
- Commit after each task or logical group.
- Never add a paid source, an API key for a paid service, or a drawn/animated scene generator.
