"""Small HTTP helpers on the standard library. Uses the system proxy settings and CA bundle."""
from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.request

USER_AGENT = "reelkit/1.0 (Inonda free reel builder)"


class PaymentRequired(Exception):
    """A source asked for money or paid credits. Constitution, Principle IV: treat as failure."""


def _context():
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if not cafile and os.path.exists("/root/.ccr/ca-bundle.crt"):
        cafile = "/root/.ccr/ca-bundle.crt"
    return ssl.create_default_context(cafile=cafile) if cafile else ssl.create_default_context()


def _open(req, timeout):
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_context()) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        if e.code == 402 or "kudosupfront" in body.lower().replace(" ", ""):
            raise PaymentRequired(f"HTTP {e.code}: {body}") from e
        raise


def http_get(url: str, headers: dict | None = None, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    return _open(req, timeout)


def http_json(method: str, url: str, payload=None, headers: dict | None = None, timeout: int = 60):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"User-Agent": USER_AGENT, "Content-Type": "application/json",
                                          **(headers or {})})
    return json.loads(_open(req, timeout) or b"{}")
