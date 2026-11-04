# Quickstart: validate the reel builder end to end

Run from the repository root. Command details: [contracts/cli.md](contracts/cli.md).

## Prerequisites

```bash
python3 --version          # 3.13+
ffmpeg -version | head -1  # any recent ffmpeg
pip install -r tools/reelkit/requirements.txt   # kokoro-onnx, soundfile, jsonschema, pytest
python3 -m reelkit setup   # downloads the free Kokoro model from Hugging Face once
```

## 1. Offline tests (no network, no model)

```bash
python3 -m pytest tools/reelkit/tests -q
```

Expected: all pass, including the rule-checker set (every price/budget/placeholder/forbidden-angle
sample refused, SC-004) and the 2-line stub-voice build (5 s video at 1080x1920 with
`credits.md` and `review.md`).

## 2. House-rule refusal (User Story 3)

```bash
python3 -m reelkit check tools/reelkit/tests/plans/bad-price-and-angle.yaml; echo "exit $?"
```

Expected: exit 2, two problems named: the `€` amount in a subtitle and the "overhead view" shot.

## 3. Build from supplied pictures (User Story 1)

```bash
python3 -m reelkit build tools/reelkit/tests/plans/two-lines-own-photos.yaml
ffprobe -v error -show_entries stream=width,height -show_entries format=duration \
  media/reels/two-lines-own-photos/two-lines-own-photos.mp4
```

Expected: 1080x1920, duration = speech + gaps + end card; subtitles appear while each line is
spoken; `review.md` lists "Greek native review".

Re-run the same command: it finishes faster and `build.log` shows voice and picture cache hits.
Edit one line's `speech`, re-run: only that line is re-voiced (SC-002, under 2 minutes).

## 4. Free generation (User Story 2, needs internet)

```bash
python3 -m reelkit pictures tools/reelkit/tests/plans/one-generated-line.yaml; echo "exit $?"
```

Expected: exit 3 with the line listed for review; `contact-sheet.jpg` shows a realistic still
with no faces or text. Then:

```bash
python3 -m reelkit pictures tools/reelkit/tests/plans/one-generated-line.yaml --accept 1
python3 -m reelkit build tools/reelkit/tests/plans/one-generated-line.yaml
```

Expected: video built; `credits.md` lists the picture as `ai-horde`, `ai-generated`; `review.md`
reminds to add an "illustration" label if it could pass as a real Inonda job.

## 5. Existing reel as a plan (User Story 4)

```bash
python3 -m reelkit build inonda-youtube-videos/reels/tiles-black-marble-90s.yaml
```

Expected: same 19 lines, subtitles and order as `free-build/archive/build_tiles_photo.py`, length
90 s ± 1 s.
