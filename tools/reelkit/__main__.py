"""reelkit: build Inonda reels and videos from a written plan, free sources only.

Commands (contracts/cli.md): check, pictures, build, new, setup. Run via bin/reelkit.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import urllib.request

from . import cache, pictures, plan as planmod, render, report, rules, voice

OK, RULES, PENDING, MISSING, NO_VOICE = 0, 2, 3, 4, 5
HF_BASE = "https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX/resolve/main"
HF_FILES = {"kokoro-v1.0.onnx": "onnx/model.onnx", "voices-v1.0.bin": None}
KOKORO_RELEASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"


def _load_checked(path: str):
    """Load the plan and run the house rules. Returns (plan, exit_code)."""
    try:
        p = planmod.load_plan(path)
    except planmod.PlanInvalid as e:
        for err in e.errors:
            print(err)
        return None, RULES
    problems = rules.check(p)
    for err in problems:
        print(err)
    return p, (RULES if problems else OK)


def cmd_check(args) -> int:
    p, code = _load_checked(args.plan)
    if code == OK:
        print(f"OK: {len(p.lines)} lines, {p.format}")
    return code


def _pictures(p, args, log):
    bdir = cache.build_dir(p.slug, getattr(args, "out", None))
    try:
        recs = pictures.obtain(p, bdir, accept=set(getattr(args, "accept", None) or []),
                               accept_all=getattr(args, "accept_all", False),
                               retry=set(getattr(args, "retry", None) or []),
                               allow_network=not getattr(args, "offline", False), log=log)
        return bdir, recs, OK
    except pictures.PicturesMissing as e:
        print("Pictures missing after trying every free source:")
        print(e)
        return bdir, None, MISSING
    except pictures.PicturesPending as e:
        print(f"{e}. Look at {os.path.join(bdir, 'contact-sheet.jpg')}, then run:")
        print(f"  bin/reelkit pictures {args.plan} --accept {' '.join(map(str, e.lines))}   (or --retry N)")
        return bdir, None, PENDING


def cmd_pictures(args) -> int:
    p, code = _load_checked(args.plan)
    if code:
        return code
    log = []
    bdir, recs, code = _pictures(p, args, log)
    report.write_log(os.path.join(bdir, "pictures.log"), log)
    if code == OK:
        print(f"OK: {len(recs)} pictures ready in {os.path.join(bdir, 'pictures')}")
    return code


def cmd_build(args) -> int:
    p, code = _load_checked(args.plan)
    if code:
        return code
    log = [f"plan {os.path.abspath(args.plan)}"]
    bdir, recs, code = _pictures(p, args, log)
    if code:
        report.write_log(os.path.join(bdir, "build.log"), log)
        return code
    try:
        engine = voice.make_engine(p.voice, stub=args.stub_voice)
    except voice.VoiceUnavailable as e:
        print(e)
        return NO_VOICE
    clips = voice.voice_lines(p, bdir, engine, log)
    warnings: list[str] = []
    out, tl = render.render(p, bdir, pictures.picture_files(recs), clips, warnings)
    w = report.length_warning(p, tl["total"])
    if w:
        warnings.append(w)
    report.write_credits(p, recs, os.path.join(bdir, "credits.md"))
    report.write_review(p, recs, warnings, tl["total"], os.path.join(bdir, "review.md"))
    log += [f"warning: {x}" for x in warnings] + [f"wrote {out} {tl['total']:.1f}s"]
    report.write_log(os.path.join(bdir, "build.log"), log)
    print(f"wrote {out} {tl['total']:.1f}s")
    for x in warnings:
        print(f"warning: {x}")
    return OK


STARTER = """# Reel plan for reelkit. Format: specs/001-free-reel-builder/contracts/reel-plan.schema.json
# Rules (constitution): no prices or budget talk; real-looking pictures only; camera at chest height;
# free sources only; every line needs a Greek subtitle; no [ADD ...] placeholders.
slug: {slug}
title: "{title}"
format: {fmt}            # reel = 1080x1920 vertical, video = 1920x1080 landscape
target_seconds: 30       # optional: warns if the finished video is more than 2 s off
voice:                   # optional; these are the defaults
  engine: kokoro
  name: am_michael
  speed: 0.90
lines:
  - speech: "Cracked, tired floor tiles?"
    greek: "Σπασμένα, κουρασμένα πλακάκια δαπέδου;"
    label: "BEFORE · ΠΡΙΝ"          # optional on-screen tag
    picture:
      file: photos/old-floor.jpg    # your own photo, path relative to this plan
    move: {{zoom_from: 1.00, zoom_to: 1.08}}
  - speech: "We look at the job properly and give you a clear written quote."
    greek: "Ελέγχουμε τη δουλειά σωστά και σας δίνουμε σαφή γραπτή προσφορά."
    picture:
      generate: "close-up of hands measuring a bathroom floor with a tape measure, Cyprus apartment"
"""


def cmd_new(args) -> int:
    path = os.path.join(cache.REPO_ROOT, "inonda-youtube-videos", "reels", f"{args.slug}.yaml")
    if os.path.exists(path):
        print(f"already exists: {path}")
        return RULES
    with open(path, "w", encoding="utf-8") as f:
        f.write(STARTER.format(slug=args.slug, title=args.slug.replace("-", " ").capitalize(), fmt=args.format))
    print(f"wrote {path}")
    return OK


def _download(url: str, dest: str):
    from .pictures.net import _context
    req = urllib.request.Request(url, headers={"User-Agent": "reelkit/1.0"})
    with urllib.request.urlopen(req, timeout=600, context=_context()) as r, open(dest + ".part", "wb") as f:
        shutil.copyfileobj(r, f)
    shutil.move(dest + ".part", dest)


def cmd_setup(args) -> int:
    os.makedirs(voice.KOKORO_DIR, exist_ok=True)
    for name in voice.KOKORO_FILES:
        dest = os.path.join(voice.KOKORO_DIR, name)
        if os.path.exists(dest):
            print(f"present: {dest}")
            continue
        urls = [f"{KOKORO_RELEASE}/{name}"]
        if HF_FILES.get(name):
            urls.insert(0, f"{HF_BASE}/{HF_FILES[name]}")
        for url in urls:
            try:
                print(f"downloading {url}")
                _download(url, dest)
                break
            except Exception as e:  # noqa: BLE001
                print(f"  failed: {e}")
        if not os.path.exists(dest):
            print(f"Could not download {name}. Download it by hand from {KOKORO_RELEASE} into {voice.KOKORO_DIR}")
            return NO_VOICE
    print(f"Kokoro voice ready in {voice.KOKORO_DIR}")
    return OK


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="reelkit", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="validate a plan and run the house rules (no network)")
    c.add_argument("plan")
    c.set_defaults(fn=cmd_check)
    pi = sub.add_parser("pictures", help="obtain pictures from free sources and make the contact sheet")
    pi.add_argument("plan")
    pi.add_argument("--accept", type=int, nargs="+", metavar="LINE")
    pi.add_argument("--accept-all", action="store_true")
    pi.add_argument("--retry", type=int, nargs="+", metavar="LINE")
    pi.add_argument("--offline", action="store_true", help="never download or generate")
    pi.add_argument("--out")
    pi.set_defaults(fn=cmd_pictures)
    b = sub.add_parser("build", help="check, get pictures, voice and render the video")
    b.add_argument("plan")
    b.add_argument("--out")
    b.add_argument("--offline", action="store_true")
    b.add_argument("--stub-voice", action="store_true", help="silent placeholder voice (for tests)")
    b.set_defaults(fn=cmd_build)
    n = sub.add_parser("new", help="write a starter plan")
    n.add_argument("slug")
    n.add_argument("--format", choices=["reel", "video"], default="reel")
    n.set_defaults(fn=cmd_new)
    s = sub.add_parser("setup", help="download the free Kokoro voice model once")
    s.set_defaults(fn=cmd_setup)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
