"""House-rule test set (SC-004): every refuse case refused, no pass case refused."""
import pytest

from reelkit.__main__ import main
from reelkit.rules import find

REFUSE_TEXT = [
    "from €300", "under 500 euros", "€45 per m²", "only 99 EUR", "$200", "£150", "a budget kitchen",
    "on a budget", "what it costs", "save here, spend there", "without spending a fortune", "cheap tiles",
    "affordable renovation", "great prices", "45 per m2", "starting at 900", "big discount",
    "προϋπολογισμός", "τιμή", "ΤΙΜΗ", "κόστος", "ευρώ", "φθηνά", "Νέα πλακάκια από €500",
    "[ADD job details]", "TODO", "[...]",
]
REFUSE_SHOT = [
    "top-down view of a floor", "overhead shot of a kitchen", "aerial view of a house", "drone shot of a roof",
    "view from the ceiling", "bird's-eye view of tiles", "floor-level view of grout", "cartoon bathroom",
    "drawing of a kitchen", "illustration of tiles", "animated tile laying", "low angle of a wall",
]
PASS_TEXT = [
    "We give a clear written quote", "free inspection", "every job is different", "two days of work",
    "3 coats of sealant", "1990s tiles", "Δωρεάν αυτοψία και γραπτή προσφορά", "Κάθε δουλειά είναι διαφορετική.",
    "A smooth, easy-to-clean finish.", "We protect doors and furniture from dust.", "Feel the difference.",
    "Precise work on every row.", "Accurate measuring first.",
]
PASS_SHOT = [
    "close-up of cracked beige 1990s floor tiles, natural daylight",
    "hands spreading adhesive with a notched trowel, eye-level view",
    "new black marble-look tiles in a Cyprus living room",
]


@pytest.mark.parametrize("text", REFUSE_TEXT)
def test_refuse_text(text):
    assert find(text, "text"), text


@pytest.mark.parametrize("text", REFUSE_SHOT)
def test_refuse_shot(text):
    assert find(text, "shot"), text


@pytest.mark.parametrize("text", PASS_TEXT)
def test_pass_text(text):
    assert not find(text, "text"), find(text, "text")


@pytest.mark.parametrize("text", PASS_SHOT)
def test_pass_shot(text):
    assert not find(text, "shot"), find(text, "shot")


def test_shot_rules_do_not_apply_to_speech():
    # "drawing" in speech is about the job, not a picture style
    assert not find("We start by drawing the layout on the floor.", "text")


def test_check_command_names_both_problems(plans_dir, capsys):
    code = main(["check", f"{plans_dir}/bad-price-and-angle.yaml"])
    out = capsys.readouterr().out
    assert code == 2
    assert "line 1: greek: price mentioned" in out and "€500" in out
    assert "line 2: picture.generate: forbidden shot" in out and "overhead" in out


def test_build_refuses_before_any_work(plans_dir, tmp_path):
    assert main(["build", f"{plans_dir}/bad-price-and-angle.yaml", "--out", str(tmp_path / "b"),
                 "--stub-voice"]) == 2
    assert not (tmp_path / "b").exists()
