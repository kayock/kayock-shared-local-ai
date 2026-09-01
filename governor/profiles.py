"""Safe configuration profiles and bounds."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from governor.config import (
    CTX_SIZE_ALLOWED,
    CTX_SIZE_MAX,
    CTX_SIZE_MIN,
    MAX_TOKENS_MAX,
    MAX_TOKENS_MIN,
    SCORE_PENALTY_ERROR,
    SCORE_PENALTY_TEMP,
    SCORE_PENALTY_THROTTLE,
    SCORE_WEIGHT_LATENCY,
    SCORE_WEIGHT_TPS,
    SCORE_WEIGHT_TTFT,
    SCORE_WEIGHT_VRAM,
    TEMPERATURE_MAX,
    TEMPERATURE_MIN,
)


class WorkloadProfile(str, Enum):
    LOW_LATENCY = "LOW_LATENCY"
    THROUGHPUT = "THROUGHPUT"
    BACKGROUND = "BACKGROUND"
    GPU_HANDOFF = "GPU_HANDOFF"


@dataclass
class RequestConfig:
    """Per-request settings safe without model reload."""

    max_tokens: int = 128
    temperature: float = 0.7

    def validate(self) -> None:
        if not (MAX_TOKENS_MIN <= self.max_tokens <= MAX_TOKENS_MAX):
            raise ValueError(
                f"max_tokens must be {MAX_TOKENS_MIN}..{MAX_TOKENS_MAX}"
            )
        if not (TEMPERATURE_MIN <= self.temperature <= TEMPERATURE_MAX):
            raise ValueError(
                f"temperature must be {TEMPERATURE_MIN}..{TEMPERATURE_MAX}"
            )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class LoadTimeConfig:
    """Load-time settings — require explicit reload to apply."""

    ctx_size: int | None = None
    llamacpp_backend: str | None = None
    note: str = "Not applied automatically; documentation / future reload path"

    def validate(self) -> None:
        if self.ctx_size is not None:
            if self.ctx_size not in CTX_SIZE_ALLOWED:
                raise ValueError(
                    f"ctx_size must be one of {sorted(CTX_SIZE_ALLOWED)}"
                )
            if not (CTX_SIZE_MIN <= self.ctx_size <= CTX_SIZE_MAX):
                raise ValueError(
                    f"ctx_size must be {CTX_SIZE_MIN}..{CTX_SIZE_MAX}"
                )


@dataclass
class ScoringWeights:
    tps: float = SCORE_WEIGHT_TPS
    ttft: float = SCORE_WEIGHT_TTFT
    latency: float = SCORE_WEIGHT_LATENCY
    vram_headroom: float = SCORE_WEIGHT_VRAM
    penalty_temperature: float = SCORE_PENALTY_TEMP
    penalty_throttle: float = SCORE_PENALTY_THROTTLE
    penalty_error: float = SCORE_PENALTY_ERROR


@dataclass
class ProfileDefinition:
    name: WorkloadProfile
    description: str
    request: RequestConfig
    weights: ScoringWeights = field(default_factory=ScoringWeights)
    load_time: LoadTimeConfig = field(default_factory=LoadTimeConfig)
    prioritize: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name.value,
            "description": self.description,
            "prioritize": self.prioritize,
            "request": self.request.to_dict(),
            "weights": asdict(self.weights),
            "load_time": asdict(self.load_time),
        }


PROFILES: dict[WorkloadProfile, ProfileDefinition] = {
    WorkloadProfile.LOW_LATENCY: ProfileDefinition(
        name=WorkloadProfile.LOW_LATENCY,
        description="Minimize TTFT for interactive voice (Father Fox use case)",
        request=RequestConfig(max_tokens=96, temperature=0.7),
        weights=ScoringWeights(tps=0.5, ttft=2.0, latency=1.5),
        prioritize="TTFT",
    ),
    WorkloadProfile.THROUGHPUT: ProfileDefinition(
        name=WorkloadProfile.THROUGHPUT,
        description="Maximize tokens/sec for longer generation",
        request=RequestConfig(max_tokens=512, temperature=0.7),
        weights=ScoringWeights(tps=2.0, ttft=0.5, latency=0.5),
        prioritize="TPS",
    ),
    WorkloadProfile.BACKGROUND: ProfileDefinition(
        name=WorkloadProfile.BACKGROUND,
        description="Resource-efficient defaults for future background workloads",
        request=RequestConfig(max_tokens=256, temperature=0.5),
        weights=ScoringWeights(tps=0.8, ttft=0.3, vram_headroom=1.0),
        prioritize="efficiency",
    ),
    WorkloadProfile.GPU_HANDOFF: ProfileDefinition(
        name=WorkloadProfile.GPU_HANDOFF,
        description="Favor freeing VRAM for RVC or other GPU workloads",
        request=RequestConfig(max_tokens=64, temperature=0.7),
        weights=ScoringWeights(vram_headroom=2.0, tps=0.3, ttft=0.5),
        load_time=LoadTimeConfig(ctx_size=4096),
        prioritize="VRAM release",
    ),
}


def get_profile(name: WorkloadProfile | str) -> ProfileDefinition:
    if isinstance(name, str):
        name = WorkloadProfile(name)
    return PROFILES[name]


def generate_candidates(
    baseline: RequestConfig,
    profile: ProfileDefinition,
) -> list[RequestConfig]:
    """Small bounded set of safe candidate configurations."""
    baseline.validate()
    candidates: list[RequestConfig] = [baseline]

    token_steps = sorted(
        {
            max(MAX_TOKENS_MIN, baseline.max_tokens - 32),
            baseline.max_tokens,
            min(MAX_TOKENS_MAX, baseline.max_tokens + 32),
            profile.request.max_tokens,
        }
    )
    temp_steps = sorted(
        {
            round(max(TEMPERATURE_MIN, baseline.temperature - 0.1), 2),
            baseline.temperature,
            round(min(TEMPERATURE_MAX, baseline.temperature + 0.1), 2),
            profile.request.temperature,
        }
    )

    seen: set[tuple[int, float]] = set()
    for mt in token_steps:
        for temp in temp_steps:
            key = (mt, temp)
            if key in seen:
                continue
            seen.add(key)
            cfg = RequestConfig(max_tokens=mt, temperature=temp)
            try:
                cfg.validate()
            except ValueError:
                continue
            if cfg.to_dict() != baseline.to_dict():
                candidates.append(cfg)

    return candidates[:6]  # hard cap
