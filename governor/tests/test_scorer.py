from governor.benchmark import BenchmarkRun, PromptResult
from governor.profiles import ScoringWeights
from governor.scorer import compare_scores, score_benchmark


def _make_run(ttft=0.5, tps=10.0, total=2.0, errors=None):
    pr = PromptResult(
        prompt_id="t",
        request_start=0,
        time_to_first_token_s=ttft,
        total_time_s=total,
        completion_tokens=20,
        tokens_per_sec=tps,
        peak_vram_mib=3000,
        peak_temperature_c=50,
        peak_gpu_util=80,
        error=None,
    )
    return BenchmarkRun(
        run_id="test",
        timestamp="2026-01-01T00:00:00Z",
        model="test-model",
        profile_name="test",
        config={},
        prompts=[pr],
        aggregate_ttft_s=ttft,
        aggregate_tps=tps,
        aggregate_total_s=total,
        errors=errors or [],
    )


def test_score_benchmark_positive():
    run = _make_run()
    result = score_benchmark(run, vram_free_mib=800)
    assert result.score > 0
    assert result.passed


def test_score_benchmark_errors():
    run = _make_run(errors=["fail"])
    result = score_benchmark(run)
    assert result.score < 0
    assert not result.passed


def test_compare_scores():
    assert compare_scores(1.1, 1.0)
    assert not compare_scores(1.01, 1.0, min_improvement=0.02)
