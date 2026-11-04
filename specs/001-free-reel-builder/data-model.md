# Data Model: Free Reel and Video Builder Pipeline

Entities from the [spec](spec.md). The reel plan's exact file format is in
[contracts/reel-plan.schema.json](contracts/reel-plan.schema.json).

## ReelPlan

The file the content maker writes (`inonda-youtube-videos/reels/<slug>.yaml`).

| Field | Type | Required | Rules |
|---|---|---|---|
| `slug` | string | yes | lowercase, digits, hyphens; names the build folder |
| `title` | string | yes | checked by the house-rule checker |
| `format` | `reel` \| `video` | yes | `reel` = 1080x1920 9:16; `video` = 1920x1080 16:9 |
| `target_seconds` | number | no | warn when finished length differs by > 2 s (FR-014) |
| `voice` | object | no | `engine` (`kokoro` default, `edge` fallback), `name` (`am_michael`), `speed` (0.90) |
| `end_card` | object | no | `seconds` (default 6), `variant` (`inonda-bilingual` default) |
| `lines` | list of Line | yes | at least 1; order is playback order |

Validation: every rule from the house-rule checker (see research §8) runs on `title`, every
`speech`, `greek`, `label`, and every picture `describe` before anything else happens.

## Line

| Field | Type | Required | Rules |
|---|---|---|---|
| `speech` | string | yes | English, spoken by the voice; no prices/budget/placeholders |
| `greek` | string | yes | Greek subtitle shown while `speech` plays; > 2 wrapped lines flagged |
| `label` | string | no | short on-screen tag, e.g. `BEFORE · ΠΡΙΝ` |
| `picture` | Picture | yes | exactly one source |
| `move` | Move | no | defaults to a gentle push-in |
| `min_seconds` | number | no | minimum on-screen time; extended to fit speech |

## Picture (source spec in the plan)

Exactly one of:

| Kind | Fields | Notes |
|---|---|---|
| `file` | `path`, optional `ai_generated` (default false) | own footage/photo; real Inonda work |
| `stock` | `url`, `licence`, optional `credit` | downloaded once; licence must be in the allowed list |
| `generate` | `describe` | shot description; style + negative prompt added automatically |
| `reuse` | `line` (index) | same picture as an earlier line |

Allowed licences: `mixkit-free`, `pexels`, `pixabay`, `coverr`, `cc0`, `cc-by` (needs `credit`),
`own`. Anything else is refused.

## PictureRecord (written by the build)

`media/reels/<slug>/pictures/index.json`, one entry per obtained picture.

| Field | Meaning |
|---|---|
| `key` | content hash of the source spec |
| `file` | local file used in the render |
| `source` | `own`, `mixkit`, `ai-horde`, ... |
| `licence`, `credit` | as recorded; `ai-generated` for generated |
| `ai_generated` | true for generation; drives the "illustration" label reminder |
| `accepted` | generated pictures only; false until reviewed on the contact sheet |
| `attempts` | generation attempts used |

State of a generated picture: `requested → received → accepted` or `→ rejected → requested`
(up to the retry limit, default 3) `→ failed` (line reported as missing a picture, FR-012).

## Move

| Field | Default | Meaning |
|---|---|---|
| `zoom_from`, `zoom_to` | 1.00 → 1.07 | scale over the line; 1.0 shows the frame with 18 % spare |
| `slide_x`, `slide_y` | 0, 0 | −1..1 drift across the spare area |
| `shake` | `normal` | `still` \| `normal` \| `strong` hand-movement amplitude |

Angle is never a field: the pipeline only ever moves a level, chest-height frame (Principle III).

## BuildOutput

`media/reels/<slug>/`:

| File | Content |
|---|---|
| `<slug>.mp4` | finished video (H.264 + AAC, 30 fps) |
| `credits.md` | every picture: source, licence, credit text (FR-008) |
| `review.md` | human checks still needed + warnings (FR-013, FR-014) |
| `contact-sheet.jpg` | all generated stills with their line numbers |
| `voice/`, `pictures/` | cached clips and pictures for partial rebuilds (FR-011) |
| `build.log` | timings, cache hits, sources tried |
