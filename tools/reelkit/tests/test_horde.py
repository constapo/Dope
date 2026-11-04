"""AI Horde generation with a fake HTTP layer: no network (research.md §4-5)."""
import io

import pytest
from PIL import Image

from reelkit.pictures import horde
from reelkit.pictures.net import PaymentRequired
from reelkit.plan import Line, Picture


def png_bytes():
    b = io.BytesIO()
    Image.new("RGB", (64, 112), (120, 110, 100)).save(b, "PNG")
    return b.getvalue()


def line():
    return Line(1, "Cracked tiles.", "Ραγισμένα πλακάκια.", Picture("generate", {"generate": "cracked beige floor tiles"}))


class FakeHorde:
    def __init__(self, fail_first=0, payment=False):
        self.fail_first, self.payment, self.posts, self.payloads = fail_first, payment, 0, []

    def http(self, method, url, payload=None, headers=None):
        assert headers["apikey"] == horde.ANON_KEY  # anonymous, never a paid key
        if method == "POST":
            if self.payment:
                raise PaymentRequired("HTTP 403: KudosUpfront")
            self.posts += 1
            self.payloads.append(payload)
            return {"id": f"job{self.posts}"}
        job = url.rsplit("/", 1)[1]
        n = int(job[3:])
        if "/check/" in url:
            return {"done": True, "faulted": n <= self.fail_first}
        return {"generations": [{"img": f"https://img.example/{job}.webp"}]}

    def get(self, url):
        return png_bytes()


def obtain(fake, tmp_path, **kw):
    (tmp_path / "pictures").mkdir(exist_ok=True)
    return horde.obtain(line(), "reel", str(tmp_path), http=fake.http, get=fake.get,
                        sleep=lambda s: None, clock=lambda: 0, **kw)


def test_prompt_has_style_and_negative():
    p = horde.prompt_for("cracked tiles")
    assert p.startswith("cracked tiles, photorealistic")
    pos, neg = p.split(" ### ")
    for word in ("faces", "text", "logo", "cartoon", "illustration", "overhead", "aerial", "drone"):
        assert word in neg
    assert "chest height" in pos


def test_generates_record_needing_review(tmp_path):
    fake = FakeHorde()
    rec = obtain(fake, tmp_path)
    assert rec["source"] == "ai-horde" and rec["ai_generated"] and rec["accepted"] is False
    assert rec["licence"] == "ai-generated" and rec["attempts"] == 1
    w, h = fake.payloads[0]["params"]["width"], fake.payloads[0]["params"]["height"]
    assert (w, h) == horde.SIZES["reel"] and w % 64 == 0 and h % 64 == 0
    assert fake.posts == horde.PARALLEL  # parallel requests, first good one wins


def test_payment_demand_is_failure(tmp_path):
    with pytest.raises(horde.HordeFailed, match="payment"):
        obtain(FakeHorde(payment=True), tmp_path)


def test_gives_up_after_max_attempts(tmp_path):
    fake = FakeHorde(fail_first=10**6)
    with pytest.raises(horde.HordeFailed, match="no picture after 3 attempts"):
        obtain(fake, tmp_path)
    assert fake.posts == horde.MAX_ATTEMPTS * horde.PARALLEL


def test_one_faulted_request_still_succeeds(tmp_path):
    rec = obtain(FakeHorde(fail_first=1), tmp_path)
    assert rec["attempts"] == 1
