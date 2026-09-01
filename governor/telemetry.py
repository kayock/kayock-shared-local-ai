"""Read-only system and GPU telemetry."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass, field
from typing import Any

import psutil


@dataclass
class MetricValue:
    value: Any
    available: bool = True
    note: str = ""


@dataclass
class GpuTelemetry:
    name: MetricValue = field(default_factory=lambda: MetricValue(None, False))
    utilization_percent: MetricValue = field(default_factory=lambda: MetricValue(None, False))
    vram_used_mib: MetricValue = field(default_factory=lambda: MetricValue(None, False))
    vram_free_mib: MetricValue = field(default_factory=lambda: MetricValue(None, False))
    vram_total_mib: MetricValue = field(default_factory=lambda: MetricValue(None, False))
    temperature_c: MetricValue = field(default_factory=lambda: MetricValue(None, False))
    clock_graphics_mhz: MetricValue = field(default_factory=lambda: MetricValue(None, False))
    power_draw_w: MetricValue = field(default_factory=lambda: MetricValue(None, False))
    power_limit_w: MetricValue = field(default_factory=lambda: MetricValue(None, False))
    throttle_reasons: MetricValue = field(default_factory=lambda: MetricValue(None, False))


@dataclass
class SystemTelemetry:
    cpu_percent: MetricValue
    ram_used_mib: MetricValue
    ram_total_mib: MetricValue
    ram_percent: MetricValue


@dataclass
class TelemetrySnapshot:
    gpu: GpuTelemetry
    system: SystemTelemetry
    source: str = "nvidia-smi+psutil"


def _parse_nvidia_smi_csv(stdout: str) -> dict[str, str]:
    lines = [ln.strip() for ln in stdout.strip().splitlines() if ln.strip()]
    if len(lines) < 2:
        return {}
    headers = [h.strip() for h in lines[0].split(",")]
    values = [v.strip() for v in lines[1].split(",")]
    if len(headers) != len(values):
        # Handle commas inside [N/A]
        values = re.split(r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", lines[1])
        values = [v.strip() for v in values]
    return dict(zip(headers, values))


def _parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if not value or value in {"[N/A]", "N/A", ""}:
        return None
    value = value.replace(" %", "").replace(" MiB", "").replace(" MHz", "").replace(" W", "")
    try:
        return float(value)
    except ValueError:
        return None


def collect_gpu_telemetry() -> GpuTelemetry:
    gpu = GpuTelemetry()
    if not shutil.which("nvidia-smi"):
        note = "nvidia-smi not found"
        for attr in gpu.__dataclass_fields__:
            setattr(gpu, attr, MetricValue(None, False, note))
        return gpu

    query = (
        "name,utilization.gpu,memory.used,memory.free,memory.total,"
        "temperature.gpu,clocks.current.graphics,power.draw,power.limit"
    )
    try:
        result = subprocess.run(
            ["nvidia-smi", f"--query-gpu={query}", "--format=csv"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        note = str(exc)
        for attr in gpu.__dataclass_fields__:
            setattr(gpu, attr, MetricValue(None, False, note))
        return gpu

    if result.returncode != 0:
        note = result.stderr.strip() or "nvidia-smi failed"
        for attr in gpu.__dataclass_fields__:
            setattr(gpu, attr, MetricValue(None, False, note))
        return gpu

    row = _parse_nvidia_smi_csv(result.stdout)
    gpu.name = MetricValue(row.get("name"), bool(row.get("name")))
    gpu.utilization_percent = MetricValue(
        _parse_float(row.get("utilization.gpu [%]")), row.get("utilization.gpu [%]") is not None
    )
    gpu.vram_used_mib = MetricValue(
        _parse_float(row.get("memory.used [MiB]")), row.get("memory.used [MiB]") is not None
    )
    gpu.vram_free_mib = MetricValue(
        _parse_float(row.get("memory.free [MiB]")), row.get("memory.free [MiB]") is not None
    )
    gpu.vram_total_mib = MetricValue(
        _parse_float(row.get("memory.total [MiB]")), row.get("memory.total [MiB]") is not None
    )
    gpu.temperature_c = MetricValue(
        _parse_float(row.get("temperature.gpu")), row.get("temperature.gpu") is not None
    )
    gpu.clock_graphics_mhz = MetricValue(
        _parse_float(row.get("clocks.current.graphics [MHz]")),
        row.get("clocks.current.graphics [MHz]") not in {None, "[N/A]", "N/A"},
    )
    pd = row.get("power.draw [W]")
    gpu.power_draw_w = MetricValue(_parse_float(pd), pd not in {None, "[N/A]", "N/A"})
    pl = row.get("power.limit [W]")
    gpu.power_limit_w = MetricValue(_parse_float(pl), pl not in {None, "[N/A]", "N/A"})

    throttle = _collect_throttle_reasons()
    gpu.throttle_reasons = throttle
    return gpu


def _collect_throttle_reasons() -> MetricValue:
    try:
        result = subprocess.run(
            ["nvidia-smi", "-q", "-d", "PERFORMANCE"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return MetricValue(None, False, str(exc))

    if result.returncode != 0:
        return MetricValue(None, False, "PERFORMANCE query failed")

    active: list[str] = []
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if stripped.endswith(": Active") and "Not Active" not in stripped:
            name = stripped.split(":")[0].strip()
            if name and name != "Performance State":
                active.append(name)
    return MetricValue(active or ["none"], True)


def collect_system_telemetry() -> SystemTelemetry:
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    return SystemTelemetry(
        cpu_percent=MetricValue(cpu, True),
        ram_used_mib=MetricValue(mem.used / (1024 * 1024), True),
        ram_total_mib=MetricValue(mem.total / (1024 * 1024), True),
        ram_percent=MetricValue(mem.percent, True),
    )


def collect_telemetry() -> TelemetrySnapshot:
    return TelemetrySnapshot(
        gpu=collect_gpu_telemetry(),
        system=collect_system_telemetry(),
    )


def telemetry_to_dict(snapshot: TelemetrySnapshot) -> dict[str, Any]:
    return json.loads(json.dumps(asdict(snapshot), default=str))


def format_metric(mv: MetricValue) -> str:
    if not mv.available:
        suffix = f" ({mv.note})" if mv.note else " (unavailable)"
        return f"unavailable{suffix}"
    if mv.value is None:
        return "unavailable"
    if isinstance(mv.value, list):
        return ", ".join(str(v) for v in mv.value) if mv.value else "none"
    if isinstance(mv.value, float) and mv.value == int(mv.value):
        return str(int(mv.value))
    return str(mv.value)
