from reelkit.plan import Line, Picture, ReelPlan
from reelkit.render import GAP, LEAD, SUB_TAIL, timeline


def make_plan(min_seconds=(0, 0), end=6):
    lines = [Line(i + 1, f"line {i}", f"γραμμή {i}", Picture("file", {"file": "x"}), min_seconds=m)
             for i, m in enumerate(min_seconds)]
    return ReelPlan("p.yaml", "t", "T", "reel", lines, end_card_seconds=end)


F = 1 / 30  # timings are whole frames, rounded up


def test_spans_follow_speech():
    tl = timeline(make_plan(), [2.0, 3.0])
    a, b = tl["spans"]
    assert abs(a["start"] - LEAD) < F
    assert 0 <= a["end"] - a["start"] - (2.0 + GAP) < F
    assert b["start"] == a["end"]
    assert 0 <= b["end"] - b["start"] - (3.0 + GAP) < F
    assert 0 <= a["sub_end"] - a["start"] - (2.0 + SUB_TAIL) < F
    assert abs(tl["total"] - (b["end"] + 6)) < 1e-9


def test_whole_frames_and_independent_lines():
    a = timeline(make_plan(), [2.0, 3.0])
    b = timeline(make_plan(), [2.5, 3.0])  # change only line 1's length
    assert a["spans"][1]["frames"] == b["spans"][1]["frames"]
    for s in a["spans"]:
        assert abs(s["start"] * 30 - round(s["start"] * 30)) < 1e-6


def test_min_seconds_extends_line():
    tl = timeline(make_plan(min_seconds=(5, 0)), [2.0, 1.0])
    a = tl["spans"][0]
    assert abs(a["end"] - a["start"] - 5) < 1e-9
    assert 0 <= a["sub_end"] - a["start"] - (2.0 + SUB_TAIL) < F


def test_subtitle_never_outlasts_line():
    tl = timeline(make_plan(), [1.0, 1.0])
    for s in tl["spans"]:
        assert s["sub_end"] <= s["end"]
