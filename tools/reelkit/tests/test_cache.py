from reelkit import cache


def test_voice_key_stable_and_sensitive():
    base = cache.voice_key("Hello", "kokoro", "am_michael", 0.9)
    assert base == cache.voice_key("Hello", "kokoro", "am_michael", 0.9)
    assert base != cache.voice_key("Hello!", "kokoro", "am_michael", 0.9)
    assert base != cache.voice_key("Hello", "edge", "am_michael", 0.9)
    assert base != cache.voice_key("Hello", "kokoro", "af_heart", 0.9)
    assert base != cache.voice_key("Hello", "kokoro", "am_michael", 1.0)


def test_picture_key():
    a = cache.picture_key({"generate": "tiles"})
    assert a == cache.picture_key({"generate": "tiles"})
    assert a != cache.picture_key({"generate": "grout"})


def test_build_dir(tmp_path):
    d = cache.build_dir("x", str(tmp_path / "out"))
    assert (tmp_path / "out" / "voice").is_dir() and (tmp_path / "out" / "pictures").is_dir()
    assert d.endswith("out")
