# reelkit

Builds Inonda reels and videos from a written plan, using free sources only. You write what each
line says (English) and shows (Greek subtitle + picture); reelkit checks it against the house rules,
gets the pictures, voices the lines, adds the handheld camera move, subtitles and end card, and
writes the video with a credits list and a review list.

Spec, plan and design: `specs/001-free-reel-builder/`. Rules: `.specify/memory/constitution.md`.

## Install (once)

```bash
pip install -r tools/reelkit/requirements.txt   # free, open-source packages
bin/reelkit setup                               # downloads the free Kokoro voice (~350 MB)
```

Needs Python 3.13+ and ffmpeg.

## Make a reel

```bash
bin/reelkit new my-reel            # starter plan: inonda-youtube-videos/reels/my-reel.yaml
bin/reelkit check  inonda-youtube-videos/reels/my-reel.yaml   # house rules, no network
bin/reelkit pictures inonda-youtube-videos/reels/my-reel.yaml # get/generate pictures
#   look at media/reels/my-reel/contact-sheet.jpg, then accept good stills or retry bad ones:
bin/reelkit pictures inonda-youtube-videos/reels/my-reel.yaml --accept 1 3   # or --accept-all
bin/reelkit pictures inonda-youtube-videos/reels/my-reel.yaml --retry 2
bin/reelkit build  inonda-youtube-videos/reels/my-reel.yaml   # writes media/reels/my-reel/my-reel.mp4
```

Outputs in `media/reels/<slug>/` (not committed): the video, `credits.md` (source and licence of
every picture), `review.md` (what a person must still check before publishing), `build.log`,
`contact-sheet.jpg`. Voice clips and pictures are cached, so changing one line only re-voices
that line.

Exit codes: 0 done, 2 house-rule or plan problem (each one listed), 3 generated pictures waiting
for review, 4 no picture after trying every free source, 5 voice model missing (run `setup`).

## Plan format

Full format: `specs/001-free-reel-builder/contracts/reel-plan.schema.json`. Short version:

```yaml
slug: my-reel                 # lowercase-with-hyphens
title: "New floor tiles"
format: reel                  # reel = 1080x1920, video = 1920x1080
target_seconds: 30            # optional, warns when off by more than 2 s
lines:
  - speech: "Cracked, tired floor tiles?"          # English, voiced
    greek: "Σπασμένα, κουρασμένα πλακάκια δαπέδου;"  # subtitle while it is spoken
    label: "BEFORE · ΠΡΙΝ"                           # optional tag
    picture: {file: photos/old-floor.jpg}           # own photo (path relative to the plan)
    # or {stock: https://.../clip.mp4, licence: mixkit-free}   # direct file link + licence
    # or {generate: "close-up of cracked beige floor tiles"}   # free AI Horde still
    # or {reuse: 1}                                            # same picture as line 1
    move: {zoom_from: 1.0, zoom_to: 1.08, slide_x: 0.3, shake: normal}   # optional
    min_seconds: 4                                  # optional minimum time on screen
```

## Free sources only

Pictures come from, in order: your own photos and footage, free stock with a commercial licence
(Mixkit, Pexels, Pixabay, Coverr, CC0, CC-BY with credit), then AI Horde (free community GPUs,
no account). Any service that asks for payment or credits counts as failed; paid tools
(Higgsfield, Artlist, ...) are never used. The voice is Kokoro `am_michael`, a free local model.

Generated pictures never show faces, text or logos, are always eye-level, and must be accepted
on the contact sheet before use. Real jobs, real clients and the owner on camera are always real
footage (`file:`), never generated.

## Tests

```bash
python3 -m pytest          # offline: no network, no voice model, silent stub voice
python3 -m pytest -m slow  # opt-in: real Kokoro voice
```
