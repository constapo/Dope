# Feature Specification: Free Reel and Video Builder Pipeline

**Feature Branch**: `001-free-reel-builder`

**Created**: 2026-11-03

**Status**: Draft

**Input**: User description: "a free reel / video generator builder pipeline"

## User Scenarios & Testing *(mandatory)*

Today every Inonda reel or video is built by its own one-off script (bathroom video 01, the v01
reel, the tile reel, the tile preview). Each copies the same steps: get pictures, add a handheld
camera move, voice the lines, burn in Greek subtitles, add the end card. Changing a reel or making
a new one means editing code. This feature replaces that with one repeatable pipeline: the
content maker writes down what the reel says and shows, and the pipeline produces a finished,
house-rule-compliant video using free sources only.

The main user is the person producing Inonda content (the owner, or an assistant acting for
them). They are not expected to write code.

### User Story 1 - Build a reel from a written reel plan (Priority: P1)

The content maker writes a reel plan: the format (vertical reel or landscape video), and for each
line what is said in English, its Greek subtitle, an optional on-screen label, and the picture to
show. They run the pipeline once and get a finished video file: pictures with a handheld camera
move, English voice-over, Greek subtitles, and the bilingual end card.

**Why this priority**: this is the whole point. On its own it already replaces the four one-off
build scripts and makes every new reel a writing job instead of a coding job.

**Independent Test**: write a plan for a short reel whose pictures are all supplied (no
generation), run the pipeline, and check the output plays with voice, subtitles, camera moves and
end card in the right order.

**Acceptance Scenarios**:

1. **Given** a complete reel plan whose pictures are all available, **When** the content maker
   runs the pipeline, **Then** one finished video is produced in the plan's format with every
   line voiced, its Greek subtitle on screen while it is spoken, and the end card last.
2. **Given** the same plan run twice, **When** nothing in the plan or its pictures changed,
   **Then** the second run produces the same video and does not fetch or generate anything again.
3. **Given** a plan with one line edited, **When** the pipeline runs again, **Then** only that
   line's voice and subtitle change, and the other lines and pictures are reused.

---

### User Story 2 - Get missing pictures from free sources (Priority: P2)

When a line's picture does not exist yet, the plan describes it instead (what the shot shows).
The pipeline gets it for free: from the content maker's own footage or photos if provided, from
free licensed stock, or by generating a photorealistic picture with a free generator. Each
picture's source and licence is recorded.

**Why this priority**: most reels lack real footage for every line; without this the content
maker still has to find or generate every picture by hand.

**Independent Test**: write a plan with two described (not supplied) pictures, run it, and check
both pictures appear in the video and both are listed with source and licence in the credits
record. Confirm nothing was paid for.

**Acceptance Scenarios**:

1. **Given** a line with a described picture and no supplied file, **When** the pipeline runs,
   **Then** it obtains a matching realistic picture from a free source and records where it came
   from and under what licence.
2. **Given** a free generator is slow or unavailable, **When** the pipeline needs a picture,
   **Then** it tries the next free source, and if all fail it stops with a clear message naming
   the line whose picture is missing, never switching to a paid service.
3. **Given** the plan names the content maker's own photo for a line, **When** the pipeline runs,
   **Then** that photo is used and no picture is generated for that line.

---

### User Story 3 - House-rule check before the video is built (Priority: P3)

Before building, the pipeline checks the plan against the constitution and stops if anything
breaks a rule: prices or budget talk in any spoken line, subtitle, label or title; `[ADD …]`
placeholders left in; described shots asking for drawings, cartoons, top-down, drone, ceiling or
floor-level angles, faces, logos or on-screen text in generated shots. It also reminds the
content maker which items need a human check (Greek native review, AI shots that could pass as a
real Inonda job need an "illustration" label).

**Why this priority**: the rules are non-negotiable and easy to break by accident; catching them
before a 10-minute build saves time and stops a non-compliant video being published.

**Independent Test**: run the check on a plan containing "from €500" in a subtitle and a shot
described as "overhead view", and confirm the build is refused with both problems named.

**Acceptance Scenarios**:

1. **Given** a plan whose text mentions a price or a client's budget, **When** the pipeline runs,
   **Then** it refuses to build and names the line and the offending words.
2. **Given** a plan with a shot described as top-down, drone, from the ceiling, drawn or cartoon,
   **When** the pipeline runs, **Then** it refuses to build and names the shot.
3. **Given** a plan that passes, **When** the video is built, **Then** a short review list is
   produced with the human checks still needed before publishing.

---

### User Story 4 - Make the existing reels with the new pipeline (Priority: P4)

The reels already made by one-off scripts (video 01, the v01 reel, the 90 s tile reel) are
rewritten as reel plans, so they can be rebuilt and edited the new way.

**Why this priority**: proves the pipeline covers real needs and lets the old scripts be retired;
not needed for new reels to work.

**Independent Test**: build the 90 s tile reel from its plan and compare length, line order,
subtitles and end card with the existing version.

**Acceptance Scenarios**:

1. **Given** the tile reel converted to a plan, **When** it is built, **Then** the result has
   the same lines, subtitles, order and end card as the existing tile reel, and is 90 s ± 1 s.

### Edge Cases

- A spoken line is longer than the time its picture is planned for: the picture stays on screen
  until the line ends; the plan's timings are treated as minimums.
- The total runs over the target length (e.g. 90 s for a reel): the pipeline warns with the
  actual length and does not cut speech mid-sentence.
- A generated picture comes back with a face, text, a cartoon look or an overhead angle: it is
  rejected, regenerated up to a set number of attempts, then the line is reported as needing a
  picture.
- A supplied picture is the wrong shape (landscape for a vertical reel): it is cropped to the
  frame centre, and the crop is noted in the review list.
- A Greek subtitle is too long for the screen: it wraps onto at most two lines; longer text is
  flagged for shortening.
- Internet access to free sources is blocked or rate-limited: the run stops cleanly, keeps
  everything already obtained, and resumes from there next time.
- A line has no Greek subtitle: the build is refused (every spoken line must have one).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The pipeline MUST build a finished video from a single written reel plan, without
  the content maker editing code.
- **FR-002**: A reel plan MUST define the format (vertical reel for Instagram/TikTok/Shorts, or
  landscape video for YouTube), a title, and an ordered list of lines; each line has English
  speech, a Greek subtitle, an optional on-screen label, and a picture (a supplied file or a
  description of the shot).
- **FR-003**: The pipeline MUST voice every line in English with the house narration voice and
  show each Greek subtitle exactly while its line is spoken.
- **FR-004**: Every picture MUST be shown with a slow handheld-phone camera move: level horizon,
  chest height, slight natural hand movement.
- **FR-005**: Every video MUST end with the silent bilingual Inonda end card.
- **FR-006**: The pipeline MUST obtain missing pictures only from free sources, in this order:
  the content maker's own footage or photos, free licensed stock, then free photorealistic
  generation. It MUST NOT use any paid service or spend credits.
- **FR-007**: Generated pictures MUST follow the shared Inonda style (photorealistic, handheld
  phone look, natural Mediterranean daylight, typical Cyprus home) and contain no faces, no
  on-screen text and no logos.
- **FR-008**: For every picture the pipeline MUST record its source, its licence and any credit
  required, and produce a credits list with the video.
- **FR-009**: Before building, the pipeline MUST check all text in the plan (speech, subtitles,
  labels, title) and refuse to build if it finds prices, price ranges, currency amounts, budget
  talk or `[ADD …]` placeholders, naming each problem and its line.
- **FR-010**: Before building, the pipeline MUST refuse shot descriptions that ask for drawings,
  cartoons, animation, top-down, overhead, ceiling, drone, crane or floor-level angles.
- **FR-011**: The pipeline MUST reuse voice clips and pictures from earlier runs when their
  inputs have not changed, so an edit to one line rebuilds only what changed.
- **FR-012**: If a free source fails, the pipeline MUST try the next free source; when none
  works it MUST stop with a message naming the lines still missing pictures, keeping all work done.
- **FR-013**: With each video the pipeline MUST produce a review list of human checks still
  required before publishing: Greek native review, "illustration" labels for AI shots that could
  pass as a real Inonda job, and any warnings (length, crops, wrapped subtitles).
- **FR-014**: The pipeline MUST report the finished video's length, and warn when it differs from
  the plan's target length by more than 2 seconds.
- **FR-015**: The existing reels (video 01, the v01 reel, the 90 s tile reel) MUST be expressible
  as reel plans and buildable by the pipeline.

### Key Entities

- **Reel plan**: one video's full description: title, format, target length, ordered lines,
  end card choice. The thing the content maker writes and edits.
- **Line**: one spoken sentence with its Greek subtitle, optional on-screen label, picture and
  camera move.
- **Picture**: a still or clip for a line; either supplied, stock or generated; carries source,
  licence, credit text and whether it was AI-generated.
- **Build output**: the finished video file, its credits list and its review list.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new 30-90 s reel can be made by writing a plan only, with no code changes; a
  content maker produces their first reel within 30 minutes of starting.
- **SC-002**: Changing one line of an existing plan and rebuilding takes under 2 minutes when no
  new picture is needed.
- **SC-003**: Zero money or paid credits are spent across all builds.
- **SC-004**: 100% of plans containing a price, budget talk or a placeholder are refused before
  building, in a test set covering each rule.
- **SC-005**: Every published video's credits list names a source and licence for 100% of its
  pictures.
- **SC-006**: The three existing reels are rebuilt from plans with the same lines, subtitles and
  order, and the one-off build scripts can be retired.
- **SC-007**: At least 9 of 10 generated pictures are accepted by the content maker without
  regeneration for being unrealistic, off-angle, or showing faces, text or logos.

## Assumptions

- The main user is the Inonda owner or an assistant producing content for them; plans are
  written by hand or with Claude's help.
- Builds run on a normal computer or a cloud session with internet access to free sources; no
  paid hosting is needed.
- The house narration voice is the free Kokoro `am_michael` voice at speed 0.90, per the
  constitution (the existing "Emma" recordings are not reused by default; this is pending the
  owner's confirmation noted in the constitution).
- Greek subtitles are written by the content maker or Claude and still need a native speaker's
  review; the pipeline does not translate or certify Greek.
- Real footage of the owner, real jobs and real clients is filmed separately and supplied as
  files; the pipeline never generates those.
- Music, publishing/uploading to platforms, thumbnails and video descriptions are out of scope
  for this feature.
- Free sources change availability often; which free services are used, and in what order within
  each source type, may change without changing this spec.
