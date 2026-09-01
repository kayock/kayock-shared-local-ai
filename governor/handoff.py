"""GPU handoff state awareness (observe only — does not modify Father Fox)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from governor.config import LEMONADE_MODEL, VRAM_PRESSURE_FREE_MIB
from governor.lemonade import check_lemonade
from governor.telemetry import TelemetrySnapshot, collect_telemetry


class HandoffState(str, Enum):
    AI_INFERENCE_ACTIVE = "AI_INFERENCE_ACTIVE"
    AI_INFERENCE_IDLE = "AI_INFERENCE_IDLE"
    GPU_MEMORY_PRESSURE = "GPU_MEMORY_PRESSURE"
    SPECIAL_WORKLOAD_REQUESTING_GPU = "SPECIAL_WORKLOAD_REQUESTING_GPU"
    MODEL_UNLOAD_REQUIRED = "MODEL_UNLOAD_REQUIRED"
    GPU_RELEASED = "GPU_RELEASED"
    AI_SERVICE_RESTORATION = "AI_SERVICE_RESTORATION"
    UNKNOWN = "UNKNOWN"


@dataclass
class HandoffObservation:
    state: HandoffState
    vram_used_mib: float | None
    vram_free_mib: float | None
    lemonade_model: str | None
    lemonade_online: bool
    notes: list[str]


# Design evidence from Father Fox lifecycle (source + runtime journal):
# 1. Model Only -> Lemonade chat
# 2. Special RVC voice -> POST /v1/unload
# 3. VRAM released -> RVC /speak
# 4. Next request -> Lemonade reloads automatically

HANDOFF_LIFECYCLE = [
    HandoffState.AI_INFERENCE_ACTIVE,
    HandoffState.MODEL_UNLOAD_REQUIRED,
    HandoffState.GPU_RELEASED,
    HandoffState.SPECIAL_WORKLOAD_REQUESTING_GPU,
    HandoffState.AI_SERVICE_RESTORATION,
    HandoffState.AI_INFERENCE_ACTIVE,
]


def observe_handoff(
    *,
    telemetry: TelemetrySnapshot | None = None,
    expect_rvc_handoff: bool = False,
    model_recently_unloaded: bool = False,
) -> HandoffObservation:
    """
    Infer handoff-related state from telemetry and Lemonade status.

    This does NOT call unload or modify any service. It provides a reusable
    interface for monitoring documented Father Fox behavior.
    """
    telemetry = telemetry or collect_telemetry()
    lemonade = check_lemonade()
    notes: list[str] = []

    vram_used = (
        float(telemetry.gpu.vram_used_mib.value)
        if telemetry.gpu.vram_used_mib.available
        else None
    )
    vram_free = (
        float(telemetry.gpu.vram_free_mib.value)
        if telemetry.gpu.vram_free_mib.available
        else None
    )

    state = HandoffState.UNKNOWN

    if model_recently_unloaded:
        state = HandoffState.GPU_RELEASED
        notes.append("External signal: model unload completed")
    elif expect_rvc_handoff:
        state = HandoffState.SPECIAL_WORKLOAD_REQUESTING_GPU
        notes.append("External signal: RVC workload expected")
    elif vram_free is not None and vram_free < VRAM_PRESSURE_FREE_MIB:
        state = HandoffState.GPU_MEMORY_PRESSURE
        notes.append(f"VRAM free {vram_free:.0f} MiB < threshold {VRAM_PRESSURE_FREE_MIB}")
    elif lemonade.model_loaded == LEMONADE_MODEL:
        util = telemetry.gpu.utilization_percent.value
        if util is not None and float(util) > 5:
            state = HandoffState.AI_INFERENCE_ACTIVE
        else:
            state = HandoffState.AI_INFERENCE_IDLE
    elif lemonade.online and not lemonade.model_loaded:
        state = HandoffState.AI_SERVICE_RESTORATION
        notes.append("Lemonade online but target model not listed")
    elif not lemonade.online:
        state = HandoffState.UNKNOWN
        notes.append(lemonade.error or "Lemonade offline")

    return HandoffObservation(
        state=state,
        vram_used_mib=vram_used,
        vram_free_mib=vram_free,
        lemonade_model=lemonade.model_loaded,
        lemonade_online=lemonade.online,
        notes=notes,
    )


def describe_lifecycle() -> list[dict[str, str]]:
    return [
        {
            "state": s.value,
            "description": _state_description(s),
        }
        for s in HANDOFF_LIFECYCLE
    ]


def _state_description(state: HandoffState) -> str:
    descriptions = {
        HandoffState.AI_INFERENCE_ACTIVE: "Lemonade model resident; inference in progress or ready",
        HandoffState.MODEL_UNLOAD_REQUIRED: "RVC/special workload needs GPU; unload API should be called",
        HandoffState.GPU_RELEASED: "VRAM freed after unload; grace period may apply",
        HandoffState.SPECIAL_WORKLOAD_REQUESTING_GPU: "RVC or other GPU workload loading",
        HandoffState.AI_SERVICE_RESTORATION: "Next chat request reloads Lemonade model",
        HandoffState.AI_INFERENCE_IDLE: "Model loaded but GPU mostly idle",
        HandoffState.GPU_MEMORY_PRESSURE: "Low free VRAM; handoff may be needed",
    }
    return descriptions.get(state, "Unknown state")
