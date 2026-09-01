"""Read-only Lemonade HTTP client."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx

from governor.config import LEMONADE_API_KEY, LEMONADE_MODEL, LEMONADE_URL


@dataclass
class LemonadeStatus:
    online: bool
    authenticated: bool
    health_status: str | None = None
    models: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None
    model_loaded: str | None = None


def _headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if LEMONADE_API_KEY:
        headers["Authorization"] = f"Bearer {LEMONADE_API_KEY}"
    return headers


def check_lemonade(timeout: float = 5.0) -> LemonadeStatus:
    status = LemonadeStatus(online=False, authenticated=bool(LEMONADE_API_KEY))
    if not LEMONADE_API_KEY:
        status.error = "LEMONADE_API_KEY not set"
        return status

    try:
        with httpx.Client(timeout=timeout) as client:
            health = client.get(f"{LEMONADE_URL}/health", headers=_headers())
            status.online = health.status_code == 200
            if health.status_code == 200:
                try:
                    body = health.json()
                    status.health_status = str(body.get("status", body))
                except Exception:
                    status.health_status = health.text[:200]
            elif health.status_code in {401, 403}:
                status.error = "authentication failed"
                return status
            else:
                status.error = f"health HTTP {health.status_code}"
                return status

            models_resp = client.get(f"{LEMONADE_URL}/v1/models", headers=_headers())
            if models_resp.status_code == 200:
                data = models_resp.json()
                status.models = data.get("data", [])
                for m in status.models:
                    if m.get("id") == LEMONADE_MODEL:
                        status.model_loaded = LEMONADE_MODEL
                        break
                if not status.model_loaded and status.models:
                    status.model_loaded = status.models[0].get("id")
            else:
                status.error = f"models HTTP {models_resp.status_code}"
    except httpx.RequestError as exc:
        status.error = str(exc)

    return status


def chat_completion_stream(
    messages: list[dict[str, str]],
    *,
    model: str | None = None,
    max_tokens: int = 128,
    temperature: float = 0.7,
    timeout: float = 300.0,
) -> tuple[httpx.Response | None, str | None]:
    """Return (response, error). Caller iterates response for SSE."""
    if not LEMONADE_API_KEY:
        return None, "LEMONADE_API_KEY not set"

    payload = {
        "model": model or LEMONADE_MODEL,
        "messages": messages,
        "stream": True,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    try:
        client = httpx.Client(timeout=timeout)
        resp = client.build_request(
            "POST",
            f"{LEMONADE_URL}/v1/chat/completions",
            headers=_headers(),
            json=payload,
        )
        sent = client.send(resp, stream=True)
        return sent, None
    except httpx.RequestError as exc:
        return None, str(exc)


def chat_completion(
    messages: list[dict[str, str]],
    *,
    model: str | None = None,
    max_tokens: int = 128,
    temperature: float = 0.7,
    timeout: float = 300.0,
) -> tuple[dict[str, Any] | None, str | None]:
    if not LEMONADE_API_KEY:
        return None, "LEMONADE_API_KEY not set"

    payload = {
        "model": model or LEMONADE_MODEL,
        "messages": messages,
        "stream": False,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.post(
                f"{LEMONADE_URL}/v1/chat/completions",
                headers=_headers(),
                json=payload,
            )
            if resp.status_code != 200:
                return None, f"HTTP {resp.status_code}: {resp.text[:300]}"
            return resp.json(), None
    except httpx.RequestError as exc:
        return None, str(exc)
