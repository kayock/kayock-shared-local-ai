"""Load sanitized repository evidence for display."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config import EVIDENCE_PATHS, REPO_ROOT


def _read_safe(path: Path) -> str | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    return _sanitize_display(text)


def _sanitize_display(text: str) -> str:
    """Strip patterns that should never appear in browser output."""
    import re
    text = re.sub(r"\b10\.\d+\.\d+\.\d+\b", "<redacted-host>", text)
    text = re.sub(
        r"(?i)(api[_-]?key|bearer|authorization)\s*[:=]\s*\S+",
        r"\1: <redacted>",
        text,
    )
    text = text.replace("LEMONADE_API_KEY", "<api-key-env-var>")
    return text


def load_evidence_vault() -> list[dict[str, Any]]:
    items = []
    catalog = [
        ("father_fox_journal", "Father Fox Runtime Journal", "VERIFIED", "GPU handoff lifecycle"),
        ("throughput", "THROUGHPUT Optimization (corrected)", "VERIFIED", "+4.22% Governor result"),
        ("benchmark", "Governor Benchmark Harness", "VERIFIED", "TTFT/TPS baseline run"),
        ("gpu_handoff", "GPU Handoff Documentation", "VERIFIED", "Architecture + sequence"),
        ("status_sample", "Governor Telemetry Sample", "VERIFIED", "Quadro P2000 snapshot"),
    ]
    for key, title, badge, summary in catalog:
        path = EVIDENCE_PATHS.get(key)
        if path is None:
            continue
        content = _read_safe(path)
        items.append({
            "id": key,
            "title": title,
            "badge": badge,
            "summary": summary,
            "path": str(path.relative_to(REPO_ROOT)) if path.is_relative_to(REPO_ROOT) else str(path),
            "content": content,
            "available": content is not None,
        })
    return items


def load_milestones() -> list[dict[str, Any]]:
    return [
        {"title": "Father Fox → Lemonade", "badge": "VERIFIED", "ref": "evidence/verified-tests/2026-09-01-father-fox-journal.md"},
        {"title": "gpt-oss-20b-MXFP4 inference", "badge": "VERIFIED", "ref": "integrations/father-fox/"},
        {"title": "Dynamic Lemonade unload", "badge": "VERIFIED", "ref": "integrations/rvc-handoff/"},
        {"title": "VRAM release for RVC", "badge": "VERIFIED", "ref": "evidence/verified-tests/2026-09-01-father-fox-journal.md"},
        {"title": "RVC GPU handoff", "badge": "VERIFIED", "ref": "docs/gpu-handoff.md"},
        {"title": "Return to Lemonade", "badge": "VERIFIED", "ref": "evidence/verified-tests/2026-09-01-father-fox-journal.md"},
        {"title": "Kayock AI Resource Governor", "badge": "VERIFIED EXPERIMENTAL", "ref": "governor/README.md"},
        {"title": "THROUGHPUT optimization +4.22%", "badge": "VERIFIED", "ref": "governor/evidence/throughput-optimization-2026-09-01.md"},
        {"title": "Global-best optimizer bug fix", "badge": "VERIFIED", "ref": "governor/evidence/throughput-optimization-2026-09-01.md", "note": "Fixed d682462"},
        {"title": "NOMAD integration", "badge": "PLANNED", "ref": "docs/integrations.md"},
        {"title": "Whispeer client", "badge": "PLANNED", "ref": "integrations/whispeer/README.md"},
        {"title": "Comic Reader", "badge": "PLANNED", "ref": None, "note": "Local source only"},
        {"title": "Audio Notebook", "badge": "PLANNED", "ref": None, "note": "Local source only"},
    ]
