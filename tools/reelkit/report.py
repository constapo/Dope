"""credits.md, review.md and build.log written next to every video (FR-008, FR-013, FR-014)."""
from __future__ import annotations

import datetime

PRE_PUBLISH = [  # constitution, Workflow and Quality Gates, step 3
    "No prices, price ranges or budget talk in the video, title, description or thumbnail",
    "No drawings, cartoons or animated scenes",
    "Every shot looks handheld at chest height with a level horizon (no overhead, drone or floor-level)",
    "Every cut is licensed for commercial use and credited where required (see credits.md)",
    "AI shots that could pass as a real Inonda job carry an on-screen 'illustration' label",
    "Greek subtitles reviewed by a native speaker",
    "No [ADD ...] placeholders left anywhere",
]


def write_credits(plan, records: dict, path: str):
    rows = ["# Credits: " + plan.title, "", "| Line | Source | Licence | Credit | File |", "|---|---|---|---|---|"]
    for n in sorted(records):
        r = records[n]
        src = r["source"] + (f" (same as line {r['reused_from']})" if "reused_from" in r else "")
        lic = r["licence"] + (", ai-generated" if r.get("ai_generated") and r["licence"] != "ai-generated" else "")
        rows.append(f"| {n} | {src} | {lic} | {r.get('credit', '')} | {r['file']} |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")


def write_review(plan, records: dict, warnings: list, seconds: float, path: str):
    out = [f"# Review before publishing: {plan.title}", "",
           f"Length: {seconds:.1f} s" + (f" (target {plan.target_seconds} s)" if plan.target_seconds else ""), "",
           "## Still to check by a person", "", "- [ ] Greek native review before publishing"]
    ai = sorted(n for n, r in records.items() if r.get("ai_generated"))
    if ai:
        out.append(f"- [ ] Add an 'illustration' label to AI shots on lines {', '.join(map(str, ai))} "
                   "if they could pass as a real Inonda job")
    out += ["", "## Pre-publish checklist (constitution)", ""] + [f"- [ ] {item}" for item in PRE_PUBLISH]
    notes = [r["note"] for r in records.values() if r.get("note")]
    if warnings or notes:
        out += ["", "## Warnings", ""] + [f"- {w}" for w in warnings] + [f"- {n}" for n in sorted(set(notes))]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


def length_warning(plan, seconds: float) -> str | None:
    if plan.target_seconds and abs(seconds - plan.target_seconds) > 2:
        return f"video is {seconds:.1f} s, target is {plan.target_seconds} s"
    return None


def write_log(path: str, entries: list):
    stamp = datetime.datetime.now().isoformat(timespec="seconds")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# reelkit build {stamp}\n" + "\n".join(entries) + "\n")
