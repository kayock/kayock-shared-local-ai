import tempfile
from pathlib import Path

from governor.persistence import (
    init_db,
    log_decision,
    log_event,
    get_recent_events,
    get_saved_profile,
    save_winning_profile,
)
from governor import config


def test_persistence_roundtrip(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "test.sqlite"
        monkeypatch.setattr(config, "DB_PATH", db)
        monkeypatch.setattr(config, "DATA_DIR", Path(tmp))
        init_db()
        save_winning_profile("LOW_LATENCY", {"max_tokens": 96}, 1.5)
        prof = get_saved_profile("LOW_LATENCY")
        assert prof is not None
        assert prof["config"]["max_tokens"] == 96
        log_event("test", "hello")
        log_decision(
            workload_profile="LOW_LATENCY",
            original_config={"max_tokens": 128},
            candidate_config={"max_tokens": 96},
            ttft=0.5,
            tps=10.0,
            peak_vram=3000,
            peak_temperature=45,
            score=1.2,
            decision="KEEP",
            reason="test",
        )
        events = get_recent_events(5)
        assert any(e["message"] == "hello" for e in events)
