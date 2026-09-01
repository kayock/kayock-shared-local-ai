"""Deterministic optimizer: measure → try safe change → measure → compare → keep or rollback."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from governor.benchmark import BenchmarkRun, run_benchmark
from governor.persistence import (
    get_saved_profile,
    log_decision,
    log_event,
    save_benchmark_run,
    save_winning_profile,
)
from governor.profiles import (
    ProfileDefinition,
    RequestConfig,
    WorkloadProfile,
    generate_candidates,
    get_profile,
)
from governor.scorer import compare_scores, score_benchmark
from governor.telemetry import collect_telemetry


class Optimizer:
    """
    Safe software-only optimizer.

    Only varies per-request parameters (max_tokens, temperature).
    Does not reload models or change hardware settings.
    """

    def __init__(self, workload: WorkloadProfile = WorkloadProfile.LOW_LATENCY):
        self.workload = workload
        self.profile_def: ProfileDefinition = get_profile(workload)
        self.baseline_config = RequestConfig(
            max_tokens=self.profile_def.request.max_tokens,
            temperature=self.profile_def.request.temperature,
        )
        self.baseline_run: BenchmarkRun | None = None
        self.baseline_score: float | None = None
        self.best_config = self.baseline_config
        self.best_score: float | None = None
        self.rollback_config = self.baseline_config

    def record_baseline(self) -> BenchmarkRun:
        self.baseline_config.validate()
        run = run_benchmark(
            profile_name=f"{self.workload.value}_baseline",
            config=self.baseline_config.to_dict(),
        )
        telem = collect_telemetry()
        vram_free = (
            float(telem.gpu.vram_free_mib.value)
            if telem.gpu.vram_free_mib.available
            else None
        )
        scored = score_benchmark(run, weights=self.profile_def.weights, vram_free_mib=vram_free)
        self.baseline_run = run
        self.baseline_score = scored.score
        self.best_config = self.baseline_config
        self.best_score = scored.score
        save_benchmark_run(run, scored.score)
        log_event(
            "baseline",
            f"Baseline recorded for {self.workload.value}",
            {"score": scored.score, "config": self.baseline_config.to_dict()},
        )
        return run

    def optimize(self) -> dict[str, Any]:
        if self.baseline_run is None:
            self.record_baseline()

        assert self.baseline_score is not None
        candidates = generate_candidates(self.baseline_config, self.profile_def)
        results: list[dict[str, Any]] = []

        for candidate in candidates:
            if candidate.to_dict() == self.baseline_config.to_dict():
                continue

            original = self.rollback_config.to_dict()
            candidate_dict = candidate.to_dict()

            try:
                candidate.validate()
            except ValueError as exc:
                log_decision(
                    workload_profile=self.workload.value,
                    original_config=original,
                    candidate_config=candidate_dict,
                    ttft=None,
                    tps=None,
                    peak_vram=None,
                    peak_temperature=None,
                    score=-999,
                    decision="REJECT",
                    reason=str(exc),
                )
                continue

            run = run_benchmark(
                profile_name=f"{self.workload.value}_candidate",
                config=candidate_dict,
            )
            telem = collect_telemetry()
            vram_free = (
                float(telem.gpu.vram_free_mib.value)
                if telem.gpu.vram_free_mib.available
                else None
            )
            scored = score_benchmark(
                run,
                weights=self.profile_def.weights,
                baseline=self.baseline_run,
                vram_free_mib=vram_free,
            )

            peak_vram = max(
                (p.peak_vram_mib for p in run.prompts if p.peak_vram_mib),
                default=None,
            )
            peak_temp = max(
                (p.peak_temperature_c for p in run.prompts if p.peak_temperature_c),
                default=None,
            )

            if run.errors:
                decision = "ROLLBACK"
                reason = run.errors[0]
            elif compare_scores(scored.score, self.best_score):
                decision = "KEEP"
                reason = (
                    f"Score {scored.score:.4f} is new global best "
                    f"(previous best {self.best_score:.4f})"
                )
                self.best_config = candidate
                self.best_score = scored.score
                save_winning_profile(self.workload.value, candidate_dict, scored.score)
            elif compare_scores(scored.score, self.baseline_score):
                decision = "NOT_BEST"
                reason = (
                    f"Score {scored.score:.4f} beats baseline {self.baseline_score:.4f} "
                    f"but not current best {self.best_score:.4f}"
                )
            else:
                decision = "REJECT"
                reason = (
                    f"Score {scored.score:.4f} does not beat baseline {self.baseline_score:.4f}"
                )

            log_decision(
                workload_profile=self.workload.value,
                original_config=original,
                candidate_config=candidate_dict,
                ttft=run.aggregate_ttft_s,
                tps=run.aggregate_tps,
                peak_vram=peak_vram,
                peak_temperature=peak_temp,
                score=scored.score,
                decision=decision,
                reason=reason,
            )
            save_benchmark_run(run, scored.score)

            results.append(
                {
                    "candidate": candidate_dict,
                    "score": scored.score,
                    "decision": decision,
                    "reason": reason,
                    "ttft": run.aggregate_ttft_s,
                    "tps": run.aggregate_tps,
                }
            )

        # Always restore to best known config (rollback if nothing improved)
        final_config = self.best_config.to_dict()
        log_event(
            "optimize_complete",
            f"Optimization complete for {self.workload.value}",
            {
                "baseline_score": self.baseline_score,
                "best_score": self.best_score,
                "active_config": final_config,
            },
        )

        return {
            "workload": self.workload.value,
            "baseline_score": self.baseline_score,
            "best_score": self.best_score,
            "active_config": final_config,
            "saved_profile": get_saved_profile(self.workload.value),
            "candidates": results,
        }
