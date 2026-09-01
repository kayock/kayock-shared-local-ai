"""Benchmark harness for Lemonade inference."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from governor.config import LEMONADE_MODEL, PROMPTS_PATH, ensure_data_dir
from governor.lemonade import chat_completion_stream
from governor.telemetry import collect_gpu_telemetry, collect_telemetry


@dataclass
class PromptResult:
    prompt_id: str
    request_start: float
    time_to_first_token_s: float | None
    total_time_s: float | None
    completion_tokens: int
    tokens_per_sec: float | None
    peak_vram_mib: float | None
    peak_temperature_c: float | None
    peak_gpu_util: float | None
    error: str | None = None


@dataclass
class BenchmarkRun:
    run_id: str
    timestamp: str
    model: str
    profile_name: str
    config: dict[str, Any]
    prompts: list[PromptResult] = field(default_factory=list)
    model_reload_penalty_s: float | None = None
    aggregate_ttft_s: float | None = None
    aggregate_tps: float | None = None
    aggregate_total_s: float | None = None
    errors: list[str] = field(default_factory=list)


def load_prompts() -> list[dict[str, Any]]:
    return json.loads(PROMPTS_PATH.read_text())


def _estimate_tokens(text: str) -> int:
    # Rough heuristic when usage not returned in stream
    return max(1, len(text.split()))


def _parse_sse_chunk(line: str) -> str | None:
    if not line.startswith("data:"):
        return None
    data = line[5:].strip()
    if data == "[DONE]":
        return None
    try:
        payload = json.loads(data)
        delta = payload.get("choices", [{}])[0].get("delta", {})
        return delta.get("content")
    except json.JSONDecodeError:
        return None


def run_single_prompt(
    prompt: dict[str, Any],
    *,
    max_tokens: int = 128,
    temperature: float = 0.7,
) -> PromptResult:
    prompt_id = prompt["id"]
    messages = prompt["messages"]
    result = PromptResult(
        prompt_id=prompt_id,
        request_start=time.perf_counter(),
        time_to_first_token_s=None,
        total_time_s=None,
        completion_tokens=0,
        tokens_per_sec=None,
        peak_vram_mib=None,
        peak_temperature_c=None,
        peak_gpu_util=None,
    )

    peak_vram = 0.0
    peak_temp = 0.0
    peak_util = 0.0

    start = time.perf_counter()
    response, err = chat_completion_stream(
        messages, max_tokens=max_tokens, temperature=temperature
    )
    if err or response is None:
        result.error = err or "no response"
        result.total_time_s = time.perf_counter() - start
        return result

    if response.status_code != 200:
        result.error = f"HTTP {response.status_code}"
        result.total_time_s = time.perf_counter() - start
        response.close()
        return result

    first_token_time: float | None = None
    content_parts: list[str] = []

    try:
        for line in response.iter_lines():
            gpu = collect_gpu_telemetry()
            if gpu.vram_used_mib.available and gpu.vram_used_mib.value:
                peak_vram = max(peak_vram, float(gpu.vram_used_mib.value))
            if gpu.temperature_c.available and gpu.temperature_c.value:
                peak_temp = max(peak_temp, float(gpu.temperature_c.value))
            if gpu.utilization_percent.available and gpu.utilization_percent.value:
                peak_util = max(peak_util, float(gpu.utilization_percent.value))

            if isinstance(line, bytes):
                line = line.decode("utf-8", errors="replace")
            chunk = _parse_sse_chunk(line)
            if chunk:
                if first_token_time is None:
                    first_token_time = time.perf_counter() - start
                content_parts.append(chunk)
    finally:
        response.close()

    total = time.perf_counter() - start
    text = "".join(content_parts)
    tokens = _estimate_tokens(text)

    result.time_to_first_token_s = first_token_time
    result.total_time_s = total
    result.completion_tokens = tokens
    if tokens > 0 and total > 0:
        # TPS from first token to end (generation throughput)
        gen_time = total - (first_token_time or 0)
        result.tokens_per_sec = tokens / gen_time if gen_time > 0 else tokens / total
    result.peak_vram_mib = peak_vram or None
    result.peak_temperature_c = peak_temp or None
    result.peak_gpu_util = peak_util or None
    return result


def run_benchmark(
    *,
    profile_name: str = "default",
    config: dict[str, Any] | None = None,
    max_tokens: int = 128,
    temperature: float = 0.7,
) -> BenchmarkRun:
    config = config or {"max_tokens": max_tokens, "temperature": temperature}
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run = BenchmarkRun(
        run_id=run_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        model=LEMONADE_MODEL,
        profile_name=profile_name,
        config=config,
    )

    # Snapshot telemetry at start
    collect_telemetry()

    for prompt in load_prompts():
        pr = run_single_prompt(
            prompt,
            max_tokens=int(config.get("max_tokens", max_tokens)),
            temperature=float(config.get("temperature", temperature)),
        )
        run.prompts.append(pr)
        if pr.error:
            run.errors.append(f"{pr.prompt_id}: {pr.error}")

    ttfts = [p.time_to_first_token_s for p in run.prompts if p.time_to_first_token_s]
    tps_vals = [p.tokens_per_sec for p in run.prompts if p.tokens_per_sec]
    totals = [p.total_time_s for p in run.prompts if p.total_time_s]

    run.aggregate_ttft_s = sum(ttfts) / len(ttfts) if ttfts else None
    run.aggregate_tps = sum(tps_vals) / len(tps_vals) if tps_vals else None
    run.aggregate_total_s = sum(totals) / len(totals) if totals else None
    return run


def save_benchmark(run: BenchmarkRun, path: Path | None = None) -> Path:
    ensure_data_dir()
    out = path or (ensure_data_dir() / f"benchmark_{run.run_id}.json")
    out.write_text(json.dumps(asdict(run), indent=2))
    return out
