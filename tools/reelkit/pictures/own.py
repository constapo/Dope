"""Own footage and photos named in the plan (always the first source)."""
from __future__ import annotations

import os

from .. import cache


def resolve(spec: dict, plan_dir: str) -> str | None:
    path = os.path.expanduser(spec["file"])
    for base in ("", plan_dir, cache.REPO_ROOT):
        candidate = path if os.path.isabs(path) else os.path.join(base or os.getcwd(), path)
        if os.path.exists(candidate):
            return os.path.abspath(candidate)
    return None


def obtain(line, plan_dir: str):
    spec = line.picture.spec
    path = resolve(spec, plan_dir)
    if path is None:
        return None
    return {"line": line.number, "key": cache.picture_key(line.picture.spec), "file": path,
            "source": spec.get("source", "own"),
            "licence": "ai-generated" if line.picture.ai_generated else "own",
            "credit": spec.get("credit", ""), "ai_generated": line.picture.ai_generated,
            "accepted": True, "attempts": 0}
