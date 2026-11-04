"""Picture sources, review gate, accept/retry, stock caching. No network."""
import io
import os

import pytest
from PIL import Image

from reelkit import pictures
from reelkit.pictures import horde, stock
from reelkit.plan import load_plan

from .test_horde import FakeHorde

GEN_PLAN = """
slug: gen
title: Gen
format: reel
lines:
  - speech: Cracked tiles.
    greek: Ραγισμένα πλακάκια.
    picture: {generate: "cracked beige floor tiles in a Cyprus apartment"}
  - speech: Same picture again.
    greek: Η ίδια εικόνα ξανά.
    picture: {reuse: 1}
"""


@pytest.fixture
def fake_horde(monkeypatch):
    fake = FakeHorde()
    real = horde.obtain

    def patched(*a, **kw):
        kw.update(http=fake.http, get=fake.get, sleep=lambda s: None, clock=lambda: 0)
        return real(*a, **kw)
    monkeypatch.setattr(horde, "obtain", patched)
    return fake


def test_generated_needs_review_then_accept(write_plan, tmp_path, fake_horde):
    plan = load_plan(write_plan(GEN_PLAN))
    bdir = str(tmp_path / "b")
    os.makedirs(os.path.join(bdir, "pictures"))
    with pytest.raises(pictures.PicturesPending) as e:
        pictures.obtain(plan, bdir)
    assert e.value.lines == [1]
    assert os.path.exists(os.path.join(bdir, "contact-sheet.jpg"))
    recs = pictures.obtain(plan, bdir, accept={1})
    assert recs[1]["accepted"] and recs[2]["reused_from"] == 1
    assert fake_horde.posts == horde.PARALLEL  # second call reused the cached still
    assert pictures.obtain(plan, bdir)[1]["accepted"]  # acceptance is remembered


def test_accept_all_and_retry(write_plan, tmp_path, fake_horde):
    plan = load_plan(write_plan(GEN_PLAN))
    bdir = str(tmp_path / "b")
    os.makedirs(os.path.join(bdir, "pictures"))
    first = pictures.obtain(plan, bdir, accept_all=True)[1]
    with pytest.raises(pictures.PicturesPending):
        pictures.obtain(plan, bdir, retry={1})
    assert not os.path.exists(first["file"])
    assert fake_horde.posts == 2 * horde.PARALLEL


def test_offline_generate_is_missing(write_plan, tmp_path):
    plan = load_plan(write_plan(GEN_PLAN))
    bdir = str(tmp_path / "b")
    os.makedirs(os.path.join(bdir, "pictures"))
    with pytest.raises(pictures.PicturesMissing):
        pictures.obtain(plan, bdir, allow_network=False)


def test_stock_download_cached_with_licence(write_plan, tmp_path, monkeypatch):
    calls = []

    def fake_get(url):
        calls.append(url)
        b = io.BytesIO()
        Image.new("RGB", (800, 600)).save(b, "JPEG")
        return b.getvalue()
    real = stock.obtain
    monkeypatch.setattr(stock, "obtain", lambda line, bdir: real(line, bdir, get=fake_get))
    plan = load_plan(write_plan("""
slug: st
title: Stock
format: reel
lines:
  - speech: Every job is different.
    greek: Κάθε δουλειά είναι διαφορετική.
    picture: {stock: "https://assets.mixkit.co/a/b.jpg", licence: cc-by, credit: "Photo by A. Person"}
"""))
    bdir = str(tmp_path / "b")
    os.makedirs(os.path.join(bdir, "pictures"))
    rec = pictures.obtain(plan, bdir)[1]
    assert (rec["source"], rec["licence"], rec["credit"]) == ("mixkit", "cc-by", "Photo by A. Person")
    pictures.obtain(plan, bdir)
    assert len(calls) == 1


def test_stock_page_url_refused(write_plan, tmp_path):
    plan = load_plan(write_plan("""
slug: st
title: Stock
format: reel
lines:
  - speech: Every job is different.
    greek: Κάθε δουλειά είναι διαφορετική.
    picture: {stock: "https://mixkit.co/free-stock-video/tiles/", licence: mixkit-free}
"""))
    bdir = str(tmp_path / "b")
    os.makedirs(os.path.join(bdir, "pictures"))
    with pytest.raises(pictures.PicturesMissing, match="direct file link"):
        pictures.obtain(plan, bdir)
