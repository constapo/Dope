"""House-rule checker (FR-009, FR-010). Pure text matching, no network: runs before any work."""
from __future__ import annotations

import os
import re
import unicodedata

import yaml

from .plan import PlanError

RULES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules.yaml")
_COMPILED = None


def normalise(s: str) -> str:
    """Lower case, Greek accents and diaeresis removed, so ΤΙΜΗ, τιμή and Τιμή all match."""
    s = unicodedata.normalize("NFD", s.casefold())
    return unicodedata.normalize("NFC", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def _rules():
    global _COMPILED
    if _COMPILED is None:
        with open(RULES_PATH, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        _COMPILED = [(name, g, [re.compile(normalise(p)) for p in g["patterns"]])
                     for name, g in data["groups"].items()]
    return _COMPILED


def find(text: str, kind: str) -> list[tuple[str, str]]:
    """Problems in one piece of text: [(message, matched text)]. kind is 'text' or 'shot'."""
    norm = normalise(text)
    found = []
    for _, g, patterns in _rules():
        if kind not in g["applies_to"]:
            continue
        for p in patterns:
            m = p.search(norm)
            if m:
                found.append((f'{g["message"]} ("{_context(text, norm, m)}") - constitution Principle '
                              f'{g["principle"]}', m.group(0)))
                break
    return found


def _context(text: str, norm: str, m) -> str:
    """The match with the word before it and the rest of its word, from the original text."""
    src = text if len(norm) == len(text) else norm
    start, end = m.start(), m.end()
    while end < len(src) and not src[end].isspace():
        end += 1
    left = src.rfind(" ", 0, max(0, start - 1))
    start = left + 1 if left >= 0 and start - left <= 25 else start
    return src[start:end].strip(" ,.;:")


def check(plan) -> list[PlanError]:
    errors = [PlanError(None, "title", msg) for msg, _ in find(plan.title, "text")]
    for line in plan.lines:
        for field in ("speech", "greek", "label"):
            for msg, _ in find(getattr(line, field) or "", "text"):
                errors.append(PlanError(line.number, field, msg))
        if line.picture.kind == "generate":
            for msg, _ in find(line.picture.spec["generate"], "shot"):
                errors.append(PlanError(line.number, "picture.generate", msg))
    return errors
