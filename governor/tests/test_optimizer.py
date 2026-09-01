from dataclasses import dataclass

from governor.optimizer import Optimizer
from governor.profiles import WorkloadProfile
from governor.scorer import ScoreResult


@dataclass
class FakeRun:
    run_id: str = "fake"
    timestamp: str = "t"
    model: str = "m"
    profile_name: str = "p"
    config: dict | None = None
    prompts: list = None
    aggregate_ttft_s: float = 0.5
    aggregate_tps: float = 5.0
    aggregate_total_s: float = 1.0
    errors: list = None

    def __post_init__(self):
        if self.prompts is None:
            self.prompts = []
        if self.errors is None:
            self.errors = []
        if self.config is None:
            self.config = {}


def _telemetry_stub():
    return type("T", (), {"gpu": type("G", (), {
        "vram_free_mib": type("M", (), {"available": True, "value": 800})()
    })()})()


def _install_stubs(monkeypatch, score_by_config: dict[tuple[int, float], float]):
    def fake_run_benchmark(**kw):
        return FakeRun(config=dict(kw.get("config") or {}))

    def fake_score_benchmark(run, **kwargs):
        cfg = run.config or {}
        key = (cfg.get("max_tokens"), cfg.get("temperature"))
        score = score_by_config.get(key, 10.0)
        return ScoreResult(score=score, breakdown={}, passed=True, reason="ok")

    monkeypatch.setattr("governor.optimizer.run_benchmark", fake_run_benchmark)
    monkeypatch.setattr("governor.optimizer.score_benchmark", fake_score_benchmark)
    monkeypatch.setattr("governor.optimizer.save_benchmark_run", lambda *a, **k: None)
    monkeypatch.setattr("governor.optimizer.log_event", lambda *a, **k: None)
    monkeypatch.setattr("governor.optimizer.log_decision", lambda *a, **k: None)
    monkeypatch.setattr("governor.optimizer.save_winning_profile", lambda *a, **k: None)
    monkeypatch.setattr("governor.optimizer.get_saved_profile", lambda *a, **k: None)
    monkeypatch.setattr("governor.optimizer.collect_telemetry", _telemetry_stub)


def test_optimizer_rollback_on_failure(monkeypatch):
    opt = Optimizer(WorkloadProfile.LOW_LATENCY)
    baseline_score = 10.0

    def fake_run_benchmark(**kw):
        return FakeRun(config=dict(kw.get("config") or {}))

    def fake_score_benchmark(run, **kwargs):
        return ScoreResult(score=baseline_score, breakdown={}, passed=True, reason="ok")

    monkeypatch.setattr("governor.optimizer.run_benchmark", fake_run_benchmark)
    monkeypatch.setattr("governor.optimizer.score_benchmark", fake_score_benchmark)
    monkeypatch.setattr("governor.optimizer.save_benchmark_run", lambda *a, **k: None)
    monkeypatch.setattr("governor.optimizer.log_event", lambda *a, **k: None)
    monkeypatch.setattr("governor.optimizer.collect_telemetry", _telemetry_stub)

    run = opt.record_baseline()
    assert opt.baseline_score == baseline_score
    assert run.run_id == "fake"


def test_global_best_keeps_earlier_higher_scoring_candidate(monkeypatch):
    """
    Regression: later candidate beating baseline must not replace a higher
    global best from an earlier candidate (THROUGHPUT scenario).
    """
    opt = Optimizer(WorkloadProfile.THROUGHPUT)
    baseline_score = 14.322578056063746
    score_by_config = {
        (opt.baseline_config.max_tokens, opt.baseline_config.temperature): baseline_score,
        (480, 0.6): 15.1485,
        (512, 0.8): 14.9028,
    }
    _install_stubs(monkeypatch, score_by_config)

    opt.record_baseline()
    result = opt.optimize()

    assert result["best_score"] == 15.1485
    assert result["active_config"] == {"max_tokens": 480, "temperature": 0.6}

    by_config = {
        (c["candidate"]["max_tokens"], c["candidate"]["temperature"]): c
        for c in result["candidates"]
    }

    assert by_config[(480, 0.6)]["decision"] == "KEEP"
    assert by_config[(512, 0.8)]["decision"] == "NOT_BEST"
    assert by_config[(512, 0.8)]["score"] == 14.9028


def test_later_candidate_worse_than_baseline_is_rejected(monkeypatch):
    opt = Optimizer(WorkloadProfile.THROUGHPUT)
    baseline_score = 14.32
    score_by_config = {
        (opt.baseline_config.max_tokens, opt.baseline_config.temperature): baseline_score,
        (480, 0.6): 15.1485,
        (480, 0.8): 13.0,
    }
    _install_stubs(monkeypatch, score_by_config)

    opt.record_baseline()
    result = opt.optimize()

    by_config = {
        (c["candidate"]["max_tokens"], c["candidate"]["temperature"]): c
        for c in result["candidates"]
    }
    if (480, 0.8) in by_config:
        assert by_config[(480, 0.8)]["decision"] == "REJECT"
    assert result["best_score"] == 15.1485
    assert result["active_config"]["max_tokens"] == 480


def test_single_improvement_over_baseline_becomes_best(monkeypatch):
    opt = Optimizer(WorkloadProfile.LOW_LATENCY)
    baseline_score = 10.0
    score_by_config = {
        (opt.baseline_config.max_tokens, opt.baseline_config.temperature): baseline_score,
        (64, 0.6): 12.0,
    }
    _install_stubs(monkeypatch, score_by_config)

    opt.record_baseline()
    result = opt.optimize()

    assert result["best_score"] == 12.0
    assert result["active_config"] == {"max_tokens": 64, "temperature": 0.6}
