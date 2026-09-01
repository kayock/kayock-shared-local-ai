"""Deterministic scoring for benchmark results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from governor.benchmark import BenchmarkRun
from governor.profiles import ScoringWeights


@dataclass
class ScoreResult:
    score: float
    breakdown: dict[str, float]
    passed: bool
    reason: str


def score_benchmark(
    run: BenchmarkRun,
    *,
    weights: ScoringWeights | None = None,
    baseline: BenchmarkRun | None = None,
    vram_free_mib: float | None = None,
    throttled: bool = False,
    max_temp_c: float = 85.0,
) -> ScoreResult:
    weights = weights or ScoringWeights()
    breakdown: dict[str, float] = {}

    if run.errors:
        penalty = weights.penalty_error * len(run.errors)
        breakdown["error_penalty"] = -penalty
        return ScoreResult(
            score=-penalty,
            breakdown=breakdown,
            passed=False,
            reason=f"{len(run.errors)} error(s): {run.errors[0]}",
        )

    score = 0.0

    if run.aggregate_tps is not None:
        contrib = run.aggregate_tps * weights.tps
        breakdown["tps"] = contrib
        score += contrib

    if run.aggregate_ttft_s is not None and run.aggregate_ttft_s > 0:
        # Lower TTFT is better — invert
        contrib = (1.0 / run.aggregate_ttft_s) * weights.ttft
        breakdown["ttft"] = contrib
        score += contrib

    if run.aggregate_total_s is not None and run.aggregate_total_s > 0:
        contrib = (1.0 / run.aggregate_total_s) * weights.latency
        breakdown["latency"] = contrib
        score += contrib

    if vram_free_mib is not None:
        contrib = (vram_free_mib / 1024.0) * weights.vram_headroom
        breakdown["vram_headroom"] = contrib
        score += contrib

    peak_temps = [
        p.peak_temperature_c
        for p in run.prompts
        if p.peak_temperature_c is not None
    ]
    if peak_temps:
        peak = max(peak_temps)
        if peak > max_temp_c:
            penalty = (peak - max_temp_c) * weights.penalty_temperature
            breakdown["temp_penalty"] = -penalty
            score -= penalty

    if throttled:
        breakdown["throttle_penalty"] = -weights.penalty_throttle
        score -= weights.penalty_throttle

    if baseline and baseline.aggregate_tps and run.aggregate_tps:
        if run.aggregate_tps < baseline.aggregate_tps * 0.95:
            breakdown["regression_penalty"] = -1.0
            score -= 1.0

    passed = score > 0 and not run.errors
    reason = "acceptable" if passed else "below threshold or errors"
    return ScoreResult(score=score, breakdown=breakdown, passed=passed, reason=reason)


def compare_scores(candidate: float, baseline: float, min_improvement: float = 0.02) -> bool:
    """True if candidate beats baseline by at least min_improvement fraction."""
    if baseline <= 0:
        return candidate > baseline
    return candidate >= baseline * (1.0 + min_improvement)
