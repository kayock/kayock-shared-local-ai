"""GPU/system telemetry — reuses Governor collector."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from governor.telemetry import collect_telemetry, format_metric, telemetry_to_dict  # noqa: E402


def get_gpu_summary() -> dict[str, Any]:
    snap = collect_telemetry()
    gpu = snap.gpu
    return {
        "name": format_metric(gpu.name),
        "utilization_percent": format_metric(gpu.utilization_percent),
        "vram_used_mib": format_metric(gpu.vram_used_mib),
        "vram_free_mib": format_metric(gpu.vram_free_mib),
        "temperature_c": format_metric(gpu.temperature_c),
        "clock_mhz": format_metric(gpu.clock_graphics_mhz),
        "throttle": format_metric(gpu.throttle_reasons),
        "cpu_percent": format_metric(snap.system.cpu_percent),
        "ram_percent": format_metric(snap.system.ram_percent),
        "raw": telemetry_to_dict(snap),
    }
