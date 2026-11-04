import pytest

from reelkit.plan import PlanInvalid, load_plan

GOOD = """
slug: good-plan
title: Good plan
format: reel
lines:
  - speech: Hello there.
    greek: Γεια σας.
    picture: {file: STILLS/portrait.jpg}
"""


def errors_of(path):
    with pytest.raises(PlanInvalid) as e:
        load_plan(path)
    return {(err.line, err.field): err.message for err in e.value.errors}


def test_minimal_plan_gets_defaults(write_plan):
    p = load_plan(write_plan(GOOD))
    assert p.size == (1080, 1920)
    assert (p.voice.engine, p.voice.name, p.voice.speed) == ("kokoro", "am_michael", 0.9)
    assert p.end_card_seconds == 6
    mv = p.lines[0].move
    assert (mv.zoom_from, mv.zoom_to, mv.slide_x, mv.slide_y, mv.shake) == (1.0, 1.07, 0, 0, "normal")


def test_video_format_size(write_plan):
    assert load_plan(write_plan(GOOD.replace("format: reel", "format: video"))).size == (1920, 1080)


def test_missing_greek(write_plan):
    errs = errors_of(write_plan(GOOD.replace("    greek: Γεια σας.\n", "")))
    assert (1, "greek") in errs


def test_bad_slug(write_plan):
    assert (None, "slug") in errors_of(write_plan(GOOD.replace("good-plan", "Good Plan")))


def test_unknown_licence(write_plan):
    text = GOOD.replace("{file: STILLS/portrait.jpg}", "{stock: 'https://x.org/a.jpg', licence: shutterstock}")
    errs = errors_of(write_plan(text))
    assert "licence must be one of" in errs[(1, "picture")]


def test_cc_by_needs_credit(write_plan):
    text = GOOD.replace("{file: STILLS/portrait.jpg}", "{stock: 'https://x.org/a.jpg', licence: cc-by}")
    assert errors_of(write_plan(text))[(1, "picture")] == "cc-by licence needs a credit"


def test_reuse_must_point_backwards(write_plan):
    text = GOOD.replace("{file: STILLS/portrait.jpg}", "{reuse: 1}")
    assert (1, "picture.reuse") in errors_of(write_plan(text))


def test_unknown_key(write_plan):
    errs = errors_of(write_plan(GOOD + "colour: red\n"))
    assert errs[(None, "plan")] == "unknown field 'colour'"


def test_empty_lines(write_plan):
    assert (None, "lines") in errors_of(write_plan(GOOD.split("lines:")[0] + "lines: []\n"))
