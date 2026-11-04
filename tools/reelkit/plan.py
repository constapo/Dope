"""Load and validate reel plans (format: reel-plan.schema.json, entities: data-model.md)."""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field

import yaml
from jsonschema import Draft202012Validator

SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reel-plan.schema.json")
SIZES = {"reel": (1080, 1920), "video": (1920, 1080)}
LICENCES = ("mixkit-free", "pexels", "pixabay", "coverr", "cc0", "cc-by")
PICTURE_KINDS = ("file", "stock", "generate", "reuse")


@dataclass
class PlanError:
    line: int | None  # 1-based line number, None for plan-level problems
    field: str
    message: str

    def __str__(self) -> str:
        where = f"line {self.line}" if self.line else "plan"
        return f"{where}: {self.field}: {self.message}"


@dataclass
class Move:
    zoom_from: float = 1.00
    zoom_to: float = 1.07
    slide_x: float = 0.0
    slide_y: float = 0.0
    shake: str = "normal"


@dataclass
class Picture:
    kind: str  # file | stock | generate | reuse
    spec: dict

    @property
    def ai_generated(self) -> bool:
        return self.kind == "generate" or bool(self.spec.get("ai_generated"))


@dataclass
class Line:
    number: int
    speech: str
    greek: str
    picture: Picture
    label: str = ""
    move: Move = field(default_factory=Move)
    min_seconds: float = 0.0


@dataclass
class Voice:
    engine: str = "kokoro"
    name: str = "am_michael"
    speed: float = 0.90


@dataclass
class ReelPlan:
    path: str
    slug: str
    title: str
    format: str
    lines: list[Line]
    voice: Voice = field(default_factory=Voice)
    end_card_seconds: float = 6.0
    end_card_variant: str = "inonda-bilingual"
    target_seconds: float | None = None

    @property
    def size(self) -> tuple[int, int]:
        return SIZES[self.format]

    @property
    def base_dir(self) -> str:
        return os.path.dirname(os.path.abspath(self.path))


class PlanInvalid(Exception):
    def __init__(self, errors: list[PlanError]):
        super().__init__("\n".join(str(e) for e in errors))
        self.errors = errors


def _schema() -> dict:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def _schema_error(err) -> PlanError:
    path = list(err.absolute_path)
    line = path[1] + 1 if len(path) >= 2 and path[0] == "lines" and isinstance(path[1], int) else None
    rest = [str(p) for p in path[2:]] if line else [str(p) for p in path]
    msg = err.message
    if err.validator == "required":
        m = re.match(r"'([^']+)' is a required property", msg)
        if m:
            rest.append(m.group(1))
            msg = "is required"
    elif err.validator == "oneOf" and rest and rest[-1] == "picture":
        msg = ("must be exactly one of: file (own photo), stock (url + licence), "
               "generate (shot description), reuse (earlier line number)")
        sub = err.instance if isinstance(err.instance, dict) else {}
        if "stock" in sub and sub.get("licence") not in LICENCES:
            msg = f"licence must be one of {', '.join(LICENCES)}"
        elif "stock" in sub and sub.get("licence") == "cc-by" and not sub.get("credit"):
            msg = "cc-by licence needs a credit"
    elif err.validator == "additionalProperties":
        m = re.search(r"\('([^']+)' was unexpected", msg)
        if m:
            msg = f"unknown field '{m.group(1)}'"
    return PlanError(line, ".".join(rest) or "plan", msg)


def load_plan(path: str) -> ReelPlan:
    """Read a YAML plan, validate it and fill defaults. Raises PlanInvalid with every problem."""
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        raise PlanInvalid([PlanError(None, "file", f"not found: {path}")]) from None
    except yaml.YAMLError as e:
        raise PlanInvalid([PlanError(None, "yaml", str(e).replace("\n", " "))]) from None
    if not isinstance(data, dict):
        raise PlanInvalid([PlanError(None, "plan", "must be a YAML mapping")])

    errors = [_schema_error(e) for e in
              sorted(Draft202012Validator(_schema()).iter_errors(data), key=lambda e: list(map(str, e.path)))]
    # one message per (line, field)
    seen, unique = set(), []
    for e in errors:
        if (e.line, e.field) not in seen:
            seen.add((e.line, e.field))
            unique.append(e)
    errors = unique

    lines: list[Line] = []
    for i, raw in enumerate(data.get("lines") or [], start=1):
        if not isinstance(raw, dict):
            continue
        pic_raw = raw.get("picture") or {}
        kinds = [k for k in PICTURE_KINDS if k in pic_raw]
        kind = kinds[0] if len(kinds) == 1 else ""
        if kind == "reuse":
            target = pic_raw.get("reuse")
            if not isinstance(target, int) or not 1 <= target < i:
                errors.append(PlanError(i, "picture.reuse", "must point to an earlier line number"))
        for key in ("speech", "greek"):
            if isinstance(raw.get(key), str) and not raw[key].strip():
                errors.append(PlanError(i, key, "must not be empty"))
        mv = raw.get("move") or {}
        lines.append(Line(
            number=i,
            speech=str(raw.get("speech", "")).strip(),
            greek=str(raw.get("greek", "")).strip(),
            picture=Picture(kind, dict(pic_raw)),
            label=str(raw.get("label", "") or "").strip(),
            move=Move(**{k: mv[k] for k in ("zoom_from", "zoom_to", "slide_x", "slide_y", "shake") if k in mv}),
            min_seconds=float(raw.get("min_seconds", 0) or 0),
        ))

    if errors:
        raise PlanInvalid(errors)

    v = data.get("voice") or {}
    ec = data.get("end_card") or {}
    return ReelPlan(
        path=path,
        slug=data["slug"],
        title=str(data["title"]).strip(),
        format=data["format"],
        lines=lines,
        voice=Voice(engine=v.get("engine", "kokoro"), name=v.get("name", "am_michael"),
                    speed=float(v.get("speed", 0.90))),
        end_card_seconds=float(ec.get("seconds", 6)),
        end_card_variant=ec.get("variant", "inonda-bilingual"),
        target_seconds=data.get("target_seconds"),
    )
