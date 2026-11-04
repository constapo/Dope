"""Free photorealistic stills from AI Horde (anonymous, community GPUs). research.md §4-5.

Prompts always add the shared Inonda style and a negative prompt that excludes faces, text, logos,
drawn styles and overhead/aerial angles (constitution, Principles II, III, V). A payment demand
counts as failure and is never worked around (Principle IV).
"""
from __future__ import annotations

import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor

from .. import cache
from .net import PaymentRequired, http_get, http_json

API = "https://aihorde.net/api/v2"
ANON_KEY = "0000000000"
CLIENT = "reelkit:1.0:inonda"
STYLE = ("photorealistic phone photo, handheld documentary look, eye-level view from chest height, natural "
         "Mediterranean daylight, warm slightly desaturated tones, shallow depth of field, typical Cyprus home, "
         "white render, 1990s ceramic tiles, aluminium windows, no faces, no on-screen text, no logos")
NEGATIVE = ("people, person, face, faces, text, letters, words, logo, watermark, signature, cartoon, illustration, "
            "drawing, painting, sketch, anime, 3d render, cgi, overhead, top-down, aerial, drone, bird's-eye, "
            "ceiling view, fisheye, distorted")
MODELS = ["AlbedoBase XL (SDXL)", "Juggernaut XL"]
SIZES = {"reel": (768, 1344), "video": (1344, 768)}
PARALLEL = 2
MAX_ATTEMPTS = 3
TIMEOUT = 15 * 60


class HordeFailed(Exception):
    pass


def prompt_for(describe: str) -> str:
    return f"{describe}, {STYLE} ### {NEGATIVE}"


def _payload(describe: str, fmt: str, seed: int) -> dict:
    w, h = SIZES[fmt]
    return {"prompt": prompt_for(describe), "nsfw": False, "censor_nsfw": True, "r2": True,
            "models": MODELS, "params": {"width": w, "height": h, "steps": 25, "cfg_scale": 6.0,
                                         "sampler_name": "k_dpmpp_2m", "karras": True, "n": 1,
                                         "seed": str(seed)}}


def _one(describe, fmt, seed, http, get, sleep, clock):
    headers = {"apikey": ANON_KEY, "Client-Agent": CLIENT}
    job = http("POST", f"{API}/generate/async", _payload(describe, fmt, seed), headers)
    if "id" not in job:
        raise HordeFailed(f"request refused: {job.get('message', job)}")
    start = clock()
    while True:
        st = http("GET", f"{API}/generate/check/{job['id']}", None, headers)
        if st.get("faulted"):
            raise HordeFailed("generation faulted")
        if st.get("done"):
            break
        if clock() - start > TIMEOUT:
            raise HordeFailed("timed out waiting in the queue")
        sleep(min(30, max(5, st.get("wait_time", 10))))
    res = http("GET", f"{API}/generate/status/{job['id']}", None, headers)
    gens = res.get("generations") or []
    if not gens or not gens[0].get("img"):
        raise HordeFailed("no image returned")
    img = gens[0]["img"]
    return get(img) if img.startswith("http") else __import__("base64").b64decode(img)


def obtain(line, fmt: str, build_dir: str, attempts_done: int = 0, http=http_json, get=http_get,
           sleep=time.sleep, clock=time.monotonic, log: list | None = None):
    """Generate one still for a line. Returns a picture record (accepted=False) or raises HordeFailed."""
    log = log if log is not None else []
    describe = line.picture.spec["generate"]
    k = cache.picture_key({**line.picture.spec, "format": fmt, "attempt": attempts_done})
    out = os.path.join(build_dir, "pictures", f"{k}.webp")
    attempts = attempts_done
    last_err = "unknown error"
    while attempts < MAX_ATTEMPTS:
        attempts += 1
        seeds = [attempts * 1000 + i for i in range(PARALLEL)]
        data = None
        with ThreadPoolExecutor(PARALLEL) as pool:
            futures = [pool.submit(_one, describe, fmt, s, http, get, sleep, clock) for s in seeds]
            for f in futures:
                try:
                    data = f.result()
                    break  # first good result wins
                except PaymentRequired as e:
                    raise HordeFailed(f"AI Horde asked for payment/kudos ({e}); paid generation is not allowed") from e
                except Exception as e:  # noqa: BLE001 - keep trying the free source
                    last_err = str(e)
        if data:
            with open(out + ".part", "wb") as f:
                f.write(data)
            shutil.move(out + ".part", out)
            log.append(f"picture line {line.number}: generated on attempt {attempts}")
            return {"line": line.number, "key": k, "file": out, "source": "ai-horde", "licence": "ai-generated",
                    "credit": "", "ai_generated": True, "accepted": False, "attempts": attempts}
        log.append(f"picture line {line.number}: attempt {attempts} failed: {last_err}")
    raise HordeFailed(f"no picture after {attempts} attempts: {last_err}")
