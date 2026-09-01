"""Trophy Room configuration."""

from __future__ import annotations

import os
from pathlib import Path

TROPHY_ROOM_ROOT = Path(__file__).resolve().parent
REPO_ROOT = TROPHY_ROOM_ROOT.parent

HOST = os.getenv("TROPHY_ROOM_HOST", "127.0.0.1")
PORT = int(os.getenv("TROPHY_ROOM_PORT", "8771"))

LEMONADE_URL = os.getenv("LEMONADE_URL", "http://127.0.0.1:13305").rstrip("/")
LEMONADE_API_KEY = os.getenv("LEMONADE_API_KEY", "").strip()
LEMONADE_MODEL = os.getenv("LEMONADE_MODEL", "gpt-oss-20b-MXFP4").strip()

FATHER_FOX_HEALTH = os.getenv(
    "FATHER_FOX_HEALTH_URL", "https://127.0.0.1:8765/health"
)
RVC_URL = os.getenv("RVC_URL", "https://127.0.0.1:8766/")
GOVERNOR_DASHBOARD_URL = os.getenv("GOVERNOR_DASHBOARD_URL", "http://127.0.0.1:8770/")

POLL_INTERVAL_MS = int(os.getenv("TROPHY_ROOM_POLL_MS", "4000"))

EVIDENCE_PATHS = {
    "father_fox_journal": REPO_ROOT / "evidence/verified-tests/2026-09-01-father-fox-journal.md",
    "benchmark": REPO_ROOT / "governor/evidence/benchmark-results-2026-09-01.md",
    "throughput": REPO_ROOT / "governor/evidence/throughput-optimization-2026-09-01.md",
    "gpu_handoff": REPO_ROOT / "docs/gpu-handoff.md",
    "status_sample": REPO_ROOT / "governor/evidence/status-sample-2026-09-01.txt",
}

GOVERNOR_SQLITE = REPO_ROOT / "governor/data/governor.sqlite"

# Verified optimization (from committed evidence — not live-computed)
VERIFIED_THROUGHPUT = {
    "baseline_score": 14.639872171624882,
    "best_score": 15.25802453529699,
    "improvement_pct": 4.22,
    "winner": {"max_tokens": 480, "temperature": 0.7},
    "winner_ttft": 6.740860408664351,
    "winner_tps": 7.438428107041268,
    "candidates": [
        {"max_tokens": 480, "temperature": 0.6, "score": 14.3498, "decision": "REJECT"},
        {"max_tokens": 480, "temperature": 0.7, "score": 15.2580, "decision": "KEEP"},
        {"max_tokens": 480, "temperature": 0.8, "score": 15.1551, "decision": "NOT_BEST"},
        {"max_tokens": 512, "temperature": 0.6, "score": 14.1270, "decision": "REJECT"},
        {"max_tokens": 512, "temperature": 0.8, "score": 15.0987, "decision": "NOT_BEST"},
    ],
}

HANDOFF_TIMELINE = [
    {"time": "00:17:39", "event": "Father Fox → Lemonade (gpt-oss-20b-MXFP4)", "verified": True},
    {"time": "00:18:08", "event": "Lemonade model unload", "verified": True},
    {"time": "00:18:12", "event": "VRAM released for RVC", "verified": True},
    {"time": "00:18:28", "event": "POST /api/talk 200 OK (RVC complete)", "verified": True},
    {"time": "00:20:15", "event": "Return to Lemonade inference", "verified": True},
    {"time": "00:20:46", "event": "POST /api/talk 200 OK", "verified": True},
]

VERIFIED_BENCHMARK = {
    "avg_ttft_s": 7.15,
    "avg_tps": 7.01,
    "peak_vram_mib": 3191,
    "peak_temp_c": 57,
    "config": {"max_tokens": 128, "temperature": 0.7},
}
