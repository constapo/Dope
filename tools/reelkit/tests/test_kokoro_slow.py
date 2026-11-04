"""Opt-in: real Kokoro voice (python3 -m pytest -m slow). Needs `bin/reelkit setup` first."""
import os

import pytest

from reelkit import voice


@pytest.mark.slow
def test_kokoro_speaks():
    if not all(os.path.exists(os.path.join(voice.KOKORO_DIR, f)) for f in voice.KOKORO_FILES):
        pytest.skip("Kokoro model not downloaded; run bin/reelkit setup")
    samples, sr = voice.KokoroEngine().speak("Every job is different.")
    assert sr == 24000 and 0.8 < len(samples) / sr < 4
