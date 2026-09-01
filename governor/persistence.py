"""SQLite persistence for benchmarks, decisions, and profiles."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Iterator

from governor.benchmark import BenchmarkRun
from governor.config import DB_PATH, ensure_data_dir


def _connect() -> sqlite3.Connection:
    ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS benchmark_runs (
                run_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                profile_name TEXT NOT NULL,
                model TEXT NOT NULL,
                config_json TEXT NOT NULL,
                results_json TEXT NOT NULL,
                score REAL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS optimization_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                workload_profile TEXT NOT NULL,
                original_config_json TEXT NOT NULL,
                candidate_config_json TEXT NOT NULL,
                ttft REAL,
                tps REAL,
                peak_vram REAL,
                peak_temperature REAL,
                score REAL,
                decision TEXT NOT NULL,
                reason TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS saved_profiles (
                name TEXT PRIMARY KEY,
                config_json TEXT NOT NULL,
                score REAL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                message TEXT NOT NULL,
                details_json TEXT
            );
            """
        )
        conn.commit()


@contextmanager
def db_session() -> Iterator[sqlite3.Connection]:
    init_db()
    conn = _connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def save_benchmark_run(run: BenchmarkRun, score: float | None = None) -> None:
    with db_session() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO benchmark_runs
            (run_id, timestamp, profile_name, model, config_json, results_json, score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run.run_id,
                run.timestamp,
                run.profile_name,
                run.model,
                json.dumps(run.config),
                json.dumps(asdict(run)),
                score,
                datetime.now(timezone.utc).isoformat(),
            ),
        )


def log_decision(
    *,
    workload_profile: str,
    original_config: dict[str, Any],
    candidate_config: dict[str, Any],
    ttft: float | None,
    tps: float | None,
    peak_vram: float | None,
    peak_temperature: float | None,
    score: float,
    decision: str,
    reason: str,
) -> None:
    with db_session() as conn:
        conn.execute(
            """
            INSERT INTO optimization_decisions
            (timestamp, workload_profile, original_config_json, candidate_config_json,
             ttft, tps, peak_vram, peak_temperature, score, decision, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                workload_profile,
                json.dumps(original_config),
                json.dumps(candidate_config),
                ttft,
                tps,
                peak_vram,
                peak_temperature,
                score,
                decision,
                reason,
            ),
        )


def log_event(event_type: str, message: str, details: dict[str, Any] | None = None) -> None:
    with db_session() as conn:
        conn.execute(
            """
            INSERT INTO events (timestamp, event_type, message, details_json)
            VALUES (?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                event_type,
                message,
                json.dumps(details) if details else None,
            ),
        )


def save_winning_profile(name: str, config: dict[str, Any], score: float) -> None:
    with db_session() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO saved_profiles (name, config_json, score, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (name, json.dumps(config), score, datetime.now(timezone.utc).isoformat()),
        )


def get_saved_profile(name: str) -> dict[str, Any] | None:
    with db_session() as conn:
        row = conn.execute(
            "SELECT config_json, score, updated_at FROM saved_profiles WHERE name = ?",
            (name,),
        ).fetchone()
        if not row:
            return None
        return {
            "config": json.loads(row["config_json"]),
            "score": row["score"],
            "updated_at": row["updated_at"],
        }


def get_latest_benchmark() -> dict[str, Any] | None:
    with db_session() as conn:
        row = conn.execute(
            """
            SELECT run_id, timestamp, profile_name, score, results_json
            FROM benchmark_runs ORDER BY created_at DESC LIMIT 1
            """
        ).fetchone()
        if not row:
            return None
        return {
            "run_id": row["run_id"],
            "timestamp": row["timestamp"],
            "profile_name": row["profile_name"],
            "score": row["score"],
            "results": json.loads(row["results_json"]),
        }


def get_recent_events(limit: int = 20) -> list[dict[str, Any]]:
    with db_session() as conn:
        rows = conn.execute(
            "SELECT timestamp, event_type, message, details_json FROM events "
            "ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [
            {
                "timestamp": r["timestamp"],
                "event_type": r["event_type"],
                "message": r["message"],
                "details": json.loads(r["details_json"]) if r["details_json"] else None,
            }
            for r in rows
        ]


def get_recent_decisions(limit: int = 20) -> list[dict[str, Any]]:
    with db_session() as conn:
        rows = conn.execute(
            """
            SELECT timestamp, workload_profile, decision, reason, score, ttft, tps
            FROM optimization_decisions ORDER BY id DESC LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
