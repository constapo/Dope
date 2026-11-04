import os

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
PLANS = os.path.join(HERE, "plans")


@pytest.fixture
def plans_dir():
    return PLANS


@pytest.fixture
def write_plan(tmp_path):
    """Write a plan YAML into tmp_path (stills resolve through an absolute path)."""
    def _write(text: str, name: str = "plan.yaml") -> str:
        p = tmp_path / name
        p.write_text(text.replace("STILLS", os.path.join(HERE, "stills")), encoding="utf-8")
        return str(p)
    return _write
