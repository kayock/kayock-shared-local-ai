"""Read-only local service detection."""

from __future__ import annotations

import ssl
from dataclasses import dataclass, field
from typing import Any

import httpx

from config import (
    FATHER_FOX_HEALTH,
    GOVERNOR_DASHBOARD_URL,
    LEMONADE_API_KEY,
    LEMONADE_URL,
    RVC_URL,
)


@dataclass
class ServiceStatus:
    id: str
    name: str
    status: str  # online | offline | planned
    badge: str  # VERIFIED | EXPERIMENTAL | PLANNED
    purpose: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    evidence_ref: str = ""


def _probe(url: str, *, verify: bool = True, timeout: float = 2.0) -> tuple[bool, str | None]:
    try:
        ctx = ssl.create_default_context()
        if not verify:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        with httpx.Client(timeout=timeout, verify=ctx if url.startswith("https") else True) as client:
            resp = client.get(url)
            if resp.status_code < 500:
                return True, f"HTTP {resp.status_code}"
            return False, f"HTTP {resp.status_code}"
    except Exception as exc:
        return False, str(exc)[:120]


def probe_lemonade() -> dict[str, Any]:
    online, note = _probe(f"{LEMONADE_URL}/health", verify=True)
    result: dict[str, Any] = {"online": online, "note": note, "authenticated": bool(LEMONADE_API_KEY)}
    if LEMONADE_API_KEY and online:
        try:
            with httpx.Client(timeout=3.0) as client:
                resp = client.get(
                    f"{LEMONADE_URL}/v1/models",
                    headers={"Authorization": f"Bearer {LEMONADE_API_KEY}"},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    models = [m.get("id") for m in data.get("data", [])]
                    result["models"] = models
                    result["model_loaded"] = models[0] if models else None
                else:
                    result["models_error"] = f"HTTP {resp.status_code}"
        except Exception as exc:
            result["models_error"] = str(exc)[:120]
    return result


def probe_all_services() -> list[ServiceStatus]:
    services: list[ServiceStatus] = []

    ff_online, ff_note = _probe(FATHER_FOX_HEALTH, verify=False)
    services.append(ServiceStatus(
        id="father_fox",
        name="Father Fox Voice Hub",
        status="online" if ff_online else "offline",
        badge="VERIFIED",
        purpose="Speech → Whisper → Lemonade LLM → TTS/RVC",
        details={"health": ff_note, "port": 8765},
        evidence_ref="evidence/verified-tests/2026-09-01-father-fox-journal.md",
    ))

    lemon = probe_lemonade()
    services.append(ServiceStatus(
        id="lemonade",
        name="AMD Lemonade Server",
        status="online" if lemon["online"] else "offline",
        badge="VERIFIED",
        purpose="OpenAI-compatible local LLM runtime",
        details=lemon,
        evidence_ref="integrations/father-fox/",
    ))

    gov_online, gov_note = _probe(GOVERNOR_DASHBOARD_URL, verify=True)
    services.append(ServiceStatus(
        id="governor",
        name="Kayock AI Resource Governor",
        status="online" if gov_online else "offline",
        badge="VERIFIED EXPERIMENTAL",
        purpose="Telemetry, benchmark, optimizer (observe-only)",
        details={"health": gov_note, "port": 8770},
        evidence_ref="governor/evidence/throughput-optimization-2026-09-01.md",
    ))

    rvc_online, rvc_note = _probe(RVC_URL, verify=False)
    services.append(ServiceStatus(
        id="rvc",
        name="Kayock Voice (RVC)",
        status="online" if rvc_online else "offline",
        badge="VERIFIED",
        purpose="Character voice synthesis after Lemonade unload",
        details={"health": rvc_note, "port": 8766},
        evidence_ref="docs/gpu-handoff.md",
    ))

    services.append(ServiceStatus(
        id="whispeer",
        name="Whispeer",
        status="planned",
        badge="PLANNED",
        purpose="Social agent — source not found on this machine",
        evidence_ref="integrations/whispeer/README.md",
    ))

    services.append(ServiceStatus(
        id="nomad",
        name="NOMAD RAG",
        status="planned",
        badge="PLANNED",
        purpose="Legacy RAG backend — not part of Lemonade demo",
        evidence_ref="docs/integrations.md",
    ))

    services.append(ServiceStatus(
        id="comic_reader",
        name="Comic Reader",
        status="offline",
        badge="PLANNED",
        purpose="Source at ~/ocr-lab — not running, not Lemonade-integrated",
        details={"local_path": "~/ocr-lab/comic-reader"},
    ))

    services.append(ServiceStatus(
        id="audio_notebook",
        name="Audio Notebook",
        status="offline",
        badge="PLANNED",
        purpose="Source at ~/erics-notebook-portable-deploy — not running",
        details={"local_path": "~/erics-notebook-portable-deploy"},
    ))

    return services


def services_to_dict(services: list[ServiceStatus]) -> list[dict[str, Any]]:
    return [
        {
            "id": s.id,
            "name": s.name,
            "status": s.status,
            "badge": s.badge,
            "purpose": s.purpose,
            "details": s.details,
            "evidence_ref": s.evidence_ref,
        }
        for s in services
    ]
