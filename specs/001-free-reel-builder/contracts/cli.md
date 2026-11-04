# Command-line contract: `reelkit`

Run from the repository root. All commands take a reel plan path
(`inonda-youtube-videos/reels/<slug>.yaml`, format in [reel-plan.schema.json](reel-plan.schema.json)).

## `python3 -m reelkit check <plan>`

Validates the plan's structure and runs the house-rule checker. No network, no rendering.

- Exit 0: prints `OK: <n> lines, <format>`.
- Exit 2: prints one problem per line as `line <i>: <field>: <message>` (or `plan: ...`), e.g.
  `line 3: greek: price mentioned ("από €500") — Principle I forbids prices`.

## `python3 -m reelkit pictures <plan> [--accept LINE...] [--accept-all] [--retry LINE...]`

Obtains every picture (own file → stock download → AI Horde generation) without rendering.
Writes `media/reels/<slug>/contact-sheet.jpg` and `pictures/index.json`.

- `--accept`/`--accept-all` marks generated pictures as reviewed and usable.
- `--retry` throws away a generated picture and asks for a new one.
- Exit 0: all pictures present and accepted.
- Exit 3: some generated pictures await review (listed with their line numbers).
- Exit 4: some lines have no picture after trying every free source (listed); work done is kept.

## `python3 -m reelkit build <plan> [--out DIR]`

Runs `check`, then `pictures` (stopping on exit 3/4), then voices the lines and renders.

- Output in `media/reels/<slug>/` (or `--out`): `<slug>.mp4`, `credits.md`, `review.md`,
  `build.log`.
- Prints `wrote <path> <seconds>s` and any warnings (length vs target, crops, long subtitles).
- Exit codes: 0 built; 2 rule/structure problems; 3 pictures awaiting review; 4 pictures missing;
  5 voice engine unavailable (message says how to install the free model).
- Never contacts a paid service. A source answering 402/payment-required counts as failed.

## `python3 -m reelkit new <slug> [--format reel|video]`

Writes a starter plan with two example lines to `inonda-youtube-videos/reels/<slug>.yaml`.
