# Research: Free Reel and Video Builder Pipeline

Phase 0 for [plan.md](plan.md). Findings come from reading the four existing build scripts in
`inonda-youtube-videos/free-build/` and probing this cloud environment on 2026-11-04.

## 1. Language and runtime

- **Decision**: Python 3.13 package, run as `python3 -m reelkit`.
- **Rationale**: all four existing builders are Python; the frame-by-frame handheld renderer in
  `build_tiles_photo.py` (Pillow + numpy piped into ffmpeg) already produces the approved look and
  can be lifted almost unchanged. Python 3.13.18 is installed here.
- **Alternatives considered**: Remotion/HyperFrames (JS, heavier toolchain, motion-graphics
  oriented, not needed for stills with camera moves); pure ffmpeg `zoompan` filter graphs (used in
  `build_v01.py`, but cannot do the smooth low-pass hand shake and tiny roll the owner approved).

## 2. Reel plan format

- **Decision**: one YAML file per reel, validated against a JSON Schema
  ([contracts/reel-plan.schema.json](contracts/reel-plan.schema.json)).
- **Rationale**: the content maker must edit plans without touching code (FR-001). YAML is
  readable, takes Greek text without escaping, and PyYAML is already installed. JSON Schema gives
  precise error messages for a non-developer.
- **Alternatives considered**: Markdown scripts (`scripts/vNN.md`) as the plan itself: too loose to
  validate timings and pictures; Python tuples (today's approach): requires code edits.

## 3. Voice

- **Decision**: Kokoro (`kokoro-onnx` 0.6.x, ONNX model `kokoro-v1.0`), voice `am_michael`, speed
  0.90, one clip per line. Voice and speed are plan fields with these defaults.
- **Rationale**: free, open-source, runs locally; it is the voice the constitution and
  `build_reel_v01_george.py` name. `kokoro-onnx` and `soundfile` install with pip here; the model
  files download from Hugging Face (`onnx-community/Kokoro-82M-v1.0-ONNX`, reachable; GitHub
  release assets are blocked here, 403).
- **Alternatives considered**: Edge TTS (free but a Microsoft online service; kept as an optional
  fallback engine, as in `build_reel_v01_george.py`); reusing the "Emma" mp3s by cutting lines out
  (`build_reel_v01.py`): rejected as the default because per-line clips are required for exact
  subtitle sync and partial rebuilds (FR-003, FR-011).
- **Open**: the owner has not confirmed `am_michael` vs "Emma" (see constitution follow-up). The
  plan field makes this a one-line change, so it does not block planning.

## 4. Picture sources (FR-006)

Source order per line: supplied file → stock clip/photo named in the plan → free generation.

- **Own footage/photos**: a path in the plan. Always first.
- **Free stock**: the plan gives the stock page URL plus licence; the pipeline downloads the file
  once and records it. Mixkit pages are reachable here, but its listing pages load clips with
  JavaScript, so automated *searching* of stock is out of scope for v1; the content maker (or
  Claude) picks the clip. Pexels is blocked from this environment (403); Pixabay and Wikimedia were
  blocked earlier (README, 2026-10-29).
- **Free generation**: **AI Horde** (anonymous key `0000000000`, community GPUs, photoreal SDXL,
  max 768x1344, queue up to ~10 min). Heartbeat reachable here. Several requests run in parallel;
  first good result wins. Pollinations is reachable but returned 402 (payment required) on
  2026-10-29, so it is not used; a source that answers with a payment demand is treated as failed.
- **Rationale**: matches the house rules' "free sources only" and the tools that worked in
  practice.
- **Alternatives considered**: Higgsfield, Artlist, vidIQ (paid; `tools/higgsfield` exists but
  spends credits and is excluded by Principle IV).

## 5. Generated-picture checks (FR-007, edge case "face/text/cartoon")

- **Decision**: prompt hygiene plus a human gate. Every generation prompt appends the shared
  Inonda style and a negative prompt (faces, people, text, logos, cartoon, illustration, drawing,
  overhead, top-down, aerial). The build writes a contact sheet of all generated stills, and a
  still is only used once accepted (`accepted: true` written back to the picture record), or after
  the content maker re-runs with `--accept-all`.
- **Rationale**: automatic face/text/style detection would need extra models; a contact sheet takes
  seconds to review and keeps a person in the loop, as Principle V expects.
- **Alternatives considered**: OpenCV face detection + OCR (extra dependencies, false
  positives on hands/tiles); fully automatic acceptance (risks a non-compliant shot).

## 6. Handheld motion (FR-004)

- **Decision**: port `frame()` and `shake()` from `build_tiles_photo.py`: still scaled to 118 %,
  per-line zoom/slide, low-pass-filtered hand shake (±9 px x, ±7 px y), tiny roll (±0.35°), level
  horizon. Move parameters become optional plan fields with sensible defaults (gentle push-in).
- **Rationale**: this is the motion the owner approved on the 90 s tile reel.

## 7. Caching and partial rebuilds (FR-011, SC-002)

- **Decision**: content-addressed cache in the build's work folder. Voice clip key = hash(text,
  voice, speed, engine version); picture key = hash(source spec). Pictures and voice clips are
  reused when keys match; the final video is always re-composed (fast compared with generation).
- **Rationale**: a one-line edit then only re-voices one line; rendering 90 s at 1080x1920 is
  well under 2 minutes on this machine class.

## 8. House-rule checker (FR-009, FR-010)

- **Decision**: pure-Python rule set run before any network or rendering work:
  - money: currency symbols and words (€, EUR, euro, $, £), "from/under/only + number", number
    followed by "per m²/sqm", Greek equivalents (ευρώ, τιμή, κόστος, από €);
  - budget talk: budget, afford, cheap, cost(s), price(s), save/spend, fortune, and Greek
    προϋπολογισμός, φτηνό, κόστος, τιμή;
  - placeholders: `[ADD`, `TODO`, `[...]`;
  - forbidden shots: drawing, cartoon, animation, illustrated, top-down, overhead, aerial, drone,
    crane, ceiling view, bird's-eye, floor-level, worm's-eye.
- Each rule has a clear message naming the line. Rules live in one data file so a new owner rule
  is a one-line addition.
- **Rationale**: deterministic and testable (SC-004 needs 100 % refusal on the test set).

## 9. Output and storage

- **Decision**: plans in `inonda-youtube-videos/reels/<slug>.yaml` (committed); builds in
  `media/reels/<slug>/` (git-ignored: video, voice, pictures, credits, review list).
- **Rationale**: licensed media is not ours to redistribute and is large; the constitution keeps
  it out of git. Plans are small and reviewable.

## 10. Testing

- **Decision**: pytest. Unit tests for plan validation, rule checker, timing/subtitle maths and
  cache keys. Integration test builds a 2-line, 5-second reel from bundled test stills with a stub
  voice engine (no network, no model download), and checks duration, frame size and the presence of
  credits and review files with ffprobe. A slow, opt-in test uses real Kokoro.
- **Rationale**: keeps CI-style runs offline and free.
