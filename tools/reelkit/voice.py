"""Voice engines and the per-line voice clip cache.

Default engine: Kokoro (free, open-source, local), voice am_michael at speed 0.90 (constitution,
Production Standards). Edge TTS is an optional free fallback. StubEngine makes silent clips for tests.
"""
from __future__ import annotations

import os

import numpy as np
import soundfile

from . import cache

KOKORO_DIR = os.path.expanduser(os.environ.get("REELKIT_KOKORO_DIR", "~/.cache/kokoro"))
KOKORO_FILES = ("kokoro-v1.0.onnx", "voices-v1.0.bin")


class VoiceUnavailable(Exception):
    """The chosen voice engine cannot run (model missing or package not installed)."""


class StubEngine:
    """Silent clips, 0.35 s per word: lets tests build videos without the voice model."""
    name = "stub"
    sample_rate = 24000

    def speak(self, text: str):
        n = int(self.sample_rate * max(0.6, 0.35 * len(text.split())))
        return np.zeros(n, dtype=np.float32), self.sample_rate


class KokoroEngine:
    def __init__(self, voice: str = "am_michael", speed: float = 0.90):
        missing = [f for f in KOKORO_FILES if not os.path.exists(os.path.join(KOKORO_DIR, f))]
        if missing:
            raise VoiceUnavailable(f"Kokoro model files missing in {KOKORO_DIR}: {', '.join(missing)}. "
                                   "Run `bin/reelkit setup` once to download them (free).")
        try:
            from kokoro_onnx import Kokoro
        except ImportError as e:
            raise VoiceUnavailable("kokoro-onnx is not installed: pip install -r tools/reelkit/requirements.txt") from e
        self._k = Kokoro(*(os.path.join(KOKORO_DIR, f) for f in KOKORO_FILES))
        self.voice, self.speed, self.name = voice, speed, "kokoro"

    def speak(self, text: str):
        samples, sr = self._k.create(text, voice=self.voice, speed=self.speed, lang="en-us")
        return np.asarray(samples, dtype=np.float32), sr


class EdgeEngine:
    """Optional fallback: free Microsoft Edge online voice (needs `pip install edge-tts`)."""
    name = "edge"

    def __init__(self, voice: str = "en-GB-ThomasNeural", speed: float = 0.97):
        try:
            import edge_tts  # noqa: F401
        except ImportError as e:
            raise VoiceUnavailable("edge-tts is not installed: pip install edge-tts") from e
        self.voice = voice if "Neural" in voice else "en-GB-ThomasNeural"
        self.rate = f"{round((speed - 1) * 100):+d}%"

    def speak(self, text: str):
        import asyncio
        import io
        import subprocess

        import edge_tts

        async def run():
            chunks = []
            async for c in edge_tts.Communicate(text, self.voice, rate=self.rate, pitch="-14Hz").stream():
                if c["type"] == "audio":
                    chunks.append(c["data"])
            return b"".join(chunks)

        mp3 = asyncio.run(run())
        wav = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "pipe:0", "-f", "wav", "-ac", "1",
                              "-ar", "24000", "pipe:1"], input=mp3, capture_output=True, check=True).stdout
        samples, sr = soundfile.read(io.BytesIO(wav), dtype="float32")
        return samples, sr


def make_engine(voice_cfg, stub: bool = False):
    if stub or os.environ.get("REELKIT_STUB_VOICE") == "1":
        return StubEngine()
    if voice_cfg.engine == "edge":
        return EdgeEngine(speed=voice_cfg.speed)
    return KokoroEngine(voice_cfg.name, voice_cfg.speed)


def voice_lines(plan, build_dir: str, engine, log: list) -> list[str]:
    """One WAV per line in build_dir/voice/, reused when text and voice settings are unchanged."""
    paths = []
    for line in plan.lines:
        k = cache.voice_key(line.speech, engine.name, plan.voice.name, plan.voice.speed)
        path = os.path.join(build_dir, "voice", f"{k}.wav")
        if os.path.exists(path):
            log.append(f"voice line {line.number}: cache hit")
        else:
            samples, sr = engine.speak(line.speech)
            soundfile.write(path, samples, sr)
            log.append(f"voice line {line.number}: new clip ({len(samples) / sr:.2f}s)")
        paths.append(path)
    return paths
