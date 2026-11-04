from reelkit.plan import Line, Picture, ReelPlan
from reelkit.render import GAP, LEAD, SUB_TAIL, timeline


def make_plan(min_seconds=(0, 0), end=6):
    lines = [Line(i + 1, f"line {i}", f"γραμμή {i}", Picture("file", {"file": "x"}), min_seconds=m)
             for i, m in enumerate(min_seconds)]
    return ReelPlan("p.yaml", "t", "T", "reel", lines, end_card_seconds=end)


def test_spans_follow_speech():
    tl = timeline(make_plan(), [2.0, 3.0])
    a, b = tl["spans"]
    assert a["start"] == LEAD
    assert a["end"] == LEAD + 2.0 + GAP
    assert b["start"] == a["end"]
    assert b["end"] == b["start"] + 3.0 + GAP
    assert a["sub_end"] == a["start"] + 2.0 + SUB_TAIL
    assert tl["total"] == b["end"] + 6


def test_min_seconds_extends_line():
    tl = timeline(make_plan(min_seconds=(5, 0)), [2.0, 1.0])
    a = tl["spans"][0]
    assert a["end"] - a["start"] == 5
    assert a["sub_end"] == a["start"] + 2.0 + SUB_TAIL


def test_subtitle_never_outlasts_line():
    tl = timeline(make_plan(), [1.0, 1.0])
    for s in tl["spans"]:
        assert s["sub_end"] <= s["end"]
