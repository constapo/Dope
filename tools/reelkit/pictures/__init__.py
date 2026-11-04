"""Obtain a picture for every line: own file → free stock → free generation (FR-006).

Records are kept in build_dir/pictures/index.json. Generated pictures need human acceptance on the
contact sheet before they are used (constitution, Principle V).
"""
from __future__ import annotations

import json
import os

from PIL import Image, ImageDraw, ImageFont

from .. import cache
from . import horde, own, stock


class PicturesPending(Exception):
    def __init__(self, lines):
        super().__init__(f"generated pictures awaiting review: lines {', '.join(map(str, lines))}")
        self.lines = lines


class PicturesMissing(Exception):
    def __init__(self, problems):
        super().__init__("\n".join(f"line {n}: {msg}" for n, msg in problems))
        self.problems = problems


def _index_path(build_dir):
    return os.path.join(build_dir, "pictures", "index.json")


def load_index(build_dir) -> dict:
    try:
        with open(_index_path(build_dir), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_index(build_dir, index: dict):
    with open(_index_path(build_dir), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def obtain(plan, build_dir: str, *, accept=(), accept_all=False, retry=(), allow_network=True,
           log: list | None = None, horde_kwargs: dict | None = None) -> dict:
    """Return {line number: record}. Raises PicturesMissing or PicturesPending when not ready."""
    log = log if log is not None else []
    index = load_index(build_dir)
    records, problems = {}, []
    for line in plan.lines:
        kind, spec = line.picture.kind, line.picture.spec
        if kind == "reuse":
            continue
        spec_key = cache.picture_key(spec)
        rec = index.get(spec_key)
        if rec and line.number in retry and rec.get("ai_generated") and kind == "generate":
            if os.path.exists(rec["file"]):
                os.remove(rec["file"])
            log.append(f"picture line {line.number}: retry requested, old still removed")
            index[spec_key] = rec = {**rec, "file": "", "retry": True}
        if rec and rec.get("file") and os.path.exists(rec["file"]) and not rec.get("retry"):
            log.append(f"picture line {line.number}: cache hit ({rec['source']})")
        else:
            try:
                if kind == "file":
                    rec = own.obtain(line, plan.base_dir)
                    if rec is None:
                        problems.append((line.number, f"file not found: {spec['file']}"))
                        continue
                elif kind == "stock":
                    if not allow_network:
                        problems.append((line.number, "stock picture not downloaded yet (network disabled)"))
                        continue
                    rec = stock.obtain(line, build_dir)
                elif kind == "generate":
                    if not allow_network:
                        problems.append((line.number, "picture not generated yet (network disabled)"))
                        continue
                    done = (rec or {}).get("attempts", 0) if (rec or {}).get("retry") else 0
                    rec = horde.obtain(line, plan.format, build_dir, attempts_done=done, log=log,
                                       **(horde_kwargs or {}))
                log.append(f"picture line {line.number}: obtained from {rec['source']}")
            except (stock.StockError, horde.HordeFailed, OSError) as e:
                problems.append((line.number, str(e)))
                continue
        rec = {**rec, "line": line.number}
        rec.pop("retry", None)
        if rec.get("ai_generated") and kind == "generate" and (accept_all or line.number in accept):
            rec["accepted"] = True
        index[spec_key] = rec
        records[line.number] = rec
    save_index(build_dir, index)

    for line in plan.lines:  # reuse points at an earlier line's picture
        if line.picture.kind == "reuse" and line.picture.spec["reuse"] in records:
            records[line.number] = {**records[line.picture.spec["reuse"]], "line": line.number,
                                    "reused_from": line.picture.spec["reuse"]}

    if any(r.get("ai_generated") and r.get("source") == "ai-horde" for r in records.values()):
        contact_sheet(records, os.path.join(build_dir, "contact-sheet.jpg"))
    if problems:
        raise PicturesMissing(problems)
    pending = sorted(n for n, r in records.items() if not r.get("accepted") and "reused_from" not in r)
    if pending:
        raise PicturesPending(pending)
    return records


def contact_sheet(records: dict, out: str, thumb=320):
    gen = [(n, r) for n, r in sorted(records.items()) if r.get("source") == "ai-horde" and "reused_from" not in r]
    cols = min(4, len(gen))
    rows = (len(gen) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb + 20) + 20, rows * (thumb + 70) + 20), (30, 30, 30))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    for i, (n, r) in enumerate(gen):
        x, y = 20 + (i % cols) * (thumb + 20), 20 + (i // cols) * (thumb + 70)
        im = Image.open(r["file"]).convert("RGB")
        im.thumbnail((thumb, thumb))
        sheet.paste(im, (x, y))
        state = "accepted" if r.get("accepted") else "TO REVIEW"
        d.text((x, y + thumb + 10), f"line {n}: {state}", font=font,
               fill=(120, 220, 120) if r.get("accepted") else (255, 200, 80))
    sheet.save(out, quality=88)


def picture_files(records: dict) -> dict:
    return {n: r["file"] for n, r in records.items()}
