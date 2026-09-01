"""Governor configuration and paths."""

from __future__ import annotations

import os
from pathlib import Path

GOVERNOR_ROOT = Path(__file__).resolve().parent
REPO_ROOT = GOVERNOR_ROOT.parent
DATA_DIR = GOVERNOR_ROOT / "data"
PROMPTS_PATH = GOVERNOR_ROOT / "prompts" / "benchmark_prompts.json"
DB_PATH = DATA_DIR / "governor.sqlite"

LEMONADE_URL = os.getenv("LEMONADE_URL", "http://127.0.0.1:13305").rstrip("/")
LEMONADE_API_KEY = os.getenv("LEMONADE_API_KEY", "").strip()
LEMONADE_MODEL = os.getenv("LEMONADE_MODEL", "gpt-oss-20b-MXFP4").strip()

# VRAM pressure threshold (MiB free) for handoff awareness
VRAM_PRESSURE_FREE_MIB = int(os.getenv("GOVERNOR_VRAM_PRESSURE_MIB", "512"))

# Scoring weights (configurable via env)
SCORE_WEIGHT_TPS = float(os.getenv("GOVERNOR_WEIGHT_TPS", "1.0"))
SCORE_WEIGHT_TTFT = float(os.getenv("GOVERNOR_WEIGHT_TTFT", "1.0"))
SCORE_WEIGHT_LATENCY = float(os.getenv("GOVERNOR_WEIGHT_LATENCY", "0.5"))
SCORE_WEIGHT_VRAM = float(os.getenv("GOVERNOR_WEIGHT_VRAM", "0.3"))
SCORE_PENALTY_TEMP = float(os.getenv("GOVERNOR_PENALTY_TEMP", "0.5"))
SCORE_PENALTY_THROTTLE = float(os.getenv("GOVERNOR_PENALTY_THROTTLE", "2.0"))
SCORE_PENALTY_ERROR = float(os.getenv("GOVERNOR_PENALTY_ERROR", "10.0"))

# Profile parameter bounds (per-request, safe without model reload)
MAX_TOKENS_MIN = 16
MAX_TOKENS_MAX = 1024
TEMPERATURE_MIN = 0.0
TEMPERATURE_MAX = 1.5

# Load-time settings (documented only; require explicit --allow-reload to apply)
CTX_SIZE_MIN = 2048
CTX_SIZE_MAX = 8192
CTX_SIZE_ALLOWED = {2048, 4096, 6144, 8192}

DASHBOARD_HOST = os.getenv("GOVERNOR_DASHBOARD_HOST", "127.0.0.1")
DASHBOARD_PORT = int(os.getenv("GOVERNOR_DASHBOARD_PORT", "8770"))


def ensure_data_dir() -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR
