"""Governor panel data — static verified evidence + optional SQLite."""

from __future__ import annotations

import json
import sqlite3
from typing import Any

from config import GOVERNOR_SQLITE, VERIFIED_BENCHMARK, VERIFIED_THROUGHPUT


def get_governor_panel() -> dict[str, Any]:
    panel: dict[str, Any] = {
        "throughput": VERIFIED_THROUGHPUT,
        "benchmark": VERIFIED_BENCHMARK,
        "test_count": 16,
        "bug_fix_commit": "d682462",
        "sqlite_available": GOVERNOR_SQLITE.is_file(),
        "last_decisions": [],
        "saved_profile": VERIFIED_THROUGHPUT["winner"],
    }

    if GOVERNOR_SQLITE.is_file():
        try:
            conn = sqlite3.connect(f"file:{GOVERNOR_SQLITE}?mode=ro", uri=True)
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT decision, score, ttft, tps, candidate_config_json, reason
                FROM optimization_decisions
                WHERE workload_profile = 'THROUGHPUT' AND id >= 15
                ORDER BY id
                """
            ).fetchall()
            panel["last_decisions"] = [
                {
                    "decision": r["decision"],
                    "score": r["score"],
                    "ttft": r["ttft"],
                    "tps": r["tps"],
                    "config": json.loads(r["candidate_config_json"]),
                    "reason": r["reason"][:200],
                }
                for r in rows
            ]
            prof = conn.execute(
                "SELECT config_json, score, updated_at FROM saved_profiles WHERE name='THROUGHPUT'"
            ).fetchone()
            if prof:
                panel["saved_profile"] = json.loads(prof["config_json"])
                panel["saved_score"] = prof["score"]
                panel["saved_at"] = prof["updated_at"]
            conn.close()
        except Exception as exc:
            panel["sqlite_error"] = str(exc)[:120]

    return panel
