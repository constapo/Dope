# Dope Constitution
<!-- Dope is the workspace for Inonda Ltd marketing content: YouTube videos, reels, social posts,
     and the tools that build them. -->

## Core Principles

### I. No Prices, No Budget Talk (NON-NEGOTIABLE)
Inonda does not work with fixed prices.
- No content MAY show, say or caption a price, price range, cost figure, "from €…", "under €…"
  or price placeholder. This covers videos, reels, shorts, posts, thumbnails, titles,
  descriptions and subtitles.
- No content MAY talk about clients' budgets ("on a budget", "what it costs", "save here /
  spend here", "without spending a fortune").
- The approved message instead: every job is different; we visit, look at the job properly and
  give a clear written quote (free inspection).

Rationale: owner rule (2026-10-29); quoted prices mislead because every job differs.

### II. Real-Looking Footage Only
Every video, preview included, MUST use real-looking footage. Drawings, cartoons, animations
and illustrated scenes MUST NOT appear. Text overlays, end cards and simple graphics made in
the editor are allowed.

Rationale: owner rule (2026-10-29): "never-ever drawings or cartoon on videos".

### III. Handheld Phone Camera
Every shot MUST look like a person filming with a phone: camera at chest/hand height, horizon
level, slight natural hand movement. Ceiling, top-down/overhead, drone, crane and low
floor-level angles MUST NOT be used, whether filmed, stock or generated. Generated clips that
break this are rejected, not fixed in the edit.

Rationale: owner rule (2026-10-29); the brand look is a tradesperson showing real work.

### IV. Free and Licensed Sources Only
- Footage generation MUST use free tools, free tiers or open models. Money or paid credits
  MUST NOT be spent on generation.
- Every cut MUST come from a source whose licence allows commercial reuse: free stock (Mixkit,
  Pexels, Pixabay, Coverr), CC0 or CC-BY clips (credited), free-generated clips, or Inonda's
  own footage. Other people's published videos MUST NOT be reused without a licence.
- A video MAY combine many cuts and MAY mix licensed stock with generated shots.

Rationale: owner rules (2026-10-29); unlicensed clips cause copyright and Content-ID claims.

### V. Honest Footage
AI-generated footage of interior work (tiling, floors, walls, kitchens, bathrooms) is allowed
and expected, but it MUST NOT pass as a specific real Inonda job, client or person.
- Generated shots show hands and tools only; no faces, and no one who could be taken for Inonda
  staff or clients.
- Owner on camera, real jobs, real clients and real before/after MUST be filmed for real.
- An AI shot that could be mistaken for a real Inonda job MUST carry an on-screen
  "illustration" label.
- Generated shots MUST NOT contain on-screen text, logos or brand names.

Rationale: shot-list rules; faked "real job" footage would mislead customers.

### VI. Bilingual and Reviewed Before Publishing
Videos are narrated in English with Greek subtitles and a silent bilingual end card. Nothing is
published while it contains `[ADD …]` placeholders, unreviewed Greek text, or a breach of
Principles I-V. Greek text MUST be reviewed by a native speaker before publishing.

Rationale: the audience is in Cyprus; placeholders and machine Greek look unprofessional.

## Production Standards

- **Narration:** Kokoro voice `am_michael` at speed 0.90 (free, open-source). Sentences with
  `[ADD …]` placeholders are not voiced.
- **Format:** YouTube videos are 16:9; reels and stories use the platform's vertical format.
- **Free toolchain known to work from the cloud (2026-10-29):** AI Horde (anonymous photoreal
  SDXL stills, max 768x1344), Kokoro (voice), ffmpeg (handheld moves, editing), Mixkit (stock).
  Run several generation jobs in parallel and keep the first good result.
- **Shared AI style:** photorealistic, handheld documentary look, natural Mediterranean
  daylight, warm slightly desaturated tones, typical Cyprus home, no faces, no text, no logos.
- **Repository:** scripts live in `inonda-youtube-videos/scripts/`, build tools next to the
  content they build. Large or licensed media that is not ours to redistribute stays out of git
  (see `.gitignore`).

## Workflow and Quality Gates

1. **Plan:** each video or post starts from its script and shot list; every shot is tagged as
   filmed, AI-generated, graphic or reused.
2. **Source:** generated and stock shots are checked against Principles II-V as they arrive;
   rejected shots are regenerated or replaced, never kept.
3. **Pre-publish review:** before anything is published, check it against every principle:
   no prices or budget talk, no drawings, correct camera angle, every cut licensed and credited
   where required, AI shots labelled, Greek reviewed, no placeholders left.
4. **Owner decisions:** new owner rules are recorded with their date in the project README and
   added to this constitution by amendment.

## Governance

This constitution overrides other project notes, scripts and prompts; where they conflict,
this document wins and the other file is updated.

- **Amendments:** any change requires the owner's approval, is made through
  `/speckit-constitution`, and states the reason and date. Owner rules given in conversation
  count as approval once recorded.
- **Versioning:** semantic versioning. MAJOR: a principle removed or redefined. MINOR: a new
  principle or section, or materially expanded guidance. PATCH: wording and clarifications.
- **Compliance:** every Spec Kit plan runs a Constitution Check against these principles, and
  every piece of content passes the pre-publish review before release. Any exception must be
  written down with the owner's approval.

**Version**: 1.0.0 | **Ratified**: 2026-11-03 | **Last Amended**: 2026-11-03
