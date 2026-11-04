"""End-to-end build with the silent stub voice: no network, no voice model (quickstart step 3)."""
import json
import os
import shutil
import subprocess

from reelkit.__main__ import main


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate",
                          "-show_entries", "format=duration", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def test_build_two_lines(plans_dir, tmp_path, capsys):
    plan = os.path.join(plans_dir, "two-lines-own-photos.yaml")
    out = tmp_path / "build"
    assert main(["build", plan, "--out", str(out), "--stub-voice", "--offline"]) == 0
    video = out / "two-lines-own-photos.mp4"
    info = probe(str(video))
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    assert (v["width"], v["height"]) == (1080, 1920)
    assert v["r_frame_rate"] == "30/1"
    assert any(s["codec_type"] == "audio" for s in info["streams"])
    # stub voice: 0.35 s/word -> 4 and 12 words; lead 0.4 + (1.4+0.35) + (4.2+0.35) + end card 2
    expected = 0.4 + 1.4 + 0.35 + 4.2 + 0.35 + 2
    assert abs(float(info["format"]["duration"]) - expected) < 0.15
    credits = (out / "credits.md").read_text()
    assert credits.count("| own |") == 2
    review = (out / "review.md").read_text()
    assert "Greek native review" in review
    assert "wide" not in review or "centre-cropped" in review

    # second run: everything cached
    assert main(["build", plan, "--out", str(out), "--stub-voice", "--offline"]) == 0
    log = (out / "build.log").read_text()
    assert log.count("voice line") == 2 and "new clip" not in log and "rendered" not in log


def test_one_line_edit_revoices_one_clip(plans_dir, tmp_path):
    src = os.path.join(plans_dir, "two-lines-own-photos.yaml")
    plan = tmp_path / "plan.yaml"
    text = open(src, encoding="utf-8").read().replace("../stills/", os.path.join(plans_dir, "..", "stills") + "/")
    plan.write_text(text, encoding="utf-8")
    out = tmp_path / "build"
    assert main(["build", str(plan), "--out", str(out), "--stub-voice", "--offline"]) == 0
    plan.write_text(text.replace("give a clear written quote", "give you a clear written quote"), encoding="utf-8")
    assert main(["build", str(plan), "--out", str(out), "--stub-voice", "--offline"]) == 0
    log = (out / "build.log").read_text()
    assert log.count("new clip") == 1 and log.count("voice line 1: cache hit") == 1
    assert "segment line 1: cache hit" in log and "segment line 2: rendered" in log
    assert "segment end card: cache hit" in log


def test_missing_own_file_exits_4(write_plan, tmp_path):
    plan = write_plan("""
slug: missing-file
title: Missing file
format: reel
lines:
  - speech: Hello.
    greek: Γεια σας.
    picture: {file: does-not-exist.jpg}
""")
    assert main(["build", plan, "--out", str(tmp_path / "b"), "--stub-voice", "--offline"]) == 4


def test_new_writes_passing_starter(tmp_path, monkeypatch):
    from reelkit import cache
    monkeypatch.setattr(cache, "REPO_ROOT", str(tmp_path))
    os.makedirs(tmp_path / "inonda-youtube-videos" / "reels")
    assert main(["new", "my-reel"]) == 0
    path = tmp_path / "inonda-youtube-videos" / "reels" / "my-reel.yaml"
    assert main(["check", str(path)]) == 0
    assert main(["new", "my-reel"]) == 2  # never overwrites
    shutil.rmtree(tmp_path / "inonda-youtube-videos")
