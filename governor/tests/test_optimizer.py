from governor.optimizer import Optimizer
from governor.profiles import WorkloadProfile


def test_optimizer_rollback_on_failure(monkeypatch):
    opt = Optimizer(WorkloadProfile.LOW_LATENCY)

    class FakeRun:
        run_id = "fake"
        timestamp = "t"
        model = "m"
        profile_name = "p"
        config = {}
        prompts = []
        aggregate_ttft_s = 0.5
        aggregate_tps = 5.0
        aggregate_total_s = 1.0
        errors = []

    monkeypatch.setattr("governor.optimizer.run_benchmark", lambda **kw: FakeRun())
    monkeypatch.setattr("governor.optimizer.save_benchmark_run", lambda *a, **k: None)
    monkeypatch.setattr("governor.optimizer.log_event", lambda *a, **k: None)
    monkeypatch.setattr(
        "governor.optimizer.collect_telemetry",
        lambda: type("T", (), {"gpu": type("G", (), {
            "vram_free_mib": type("M", (), {"available": True, "value": 800})()
        })()})(),
    )
    run = opt.record_baseline()
    assert opt.baseline_score is not None
    assert run.run_id == "fake"
