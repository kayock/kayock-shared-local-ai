from unittest.mock import patch

from governor.handoff import HandoffState, observe_handoff
from governor.telemetry import GpuTelemetry, MetricValue, SystemTelemetry, TelemetrySnapshot


def _snapshot(vram_free=2000, util=0):
    return TelemetrySnapshot(
        gpu=GpuTelemetry(
            vram_free_mib=MetricValue(float(vram_free), True),
            vram_used_mib=MetricValue(2000.0, True),
            utilization_percent=MetricValue(float(util), True),
        ),
        system=SystemTelemetry(
            cpu_percent=MetricValue(10.0, True),
            ram_used_mib=MetricValue(4000.0, True),
            ram_total_mib=MetricValue(16000.0, True),
            ram_percent=MetricValue(25.0, True),
        ),
    )


@patch("governor.handoff.check_lemonade")
def test_handoff_memory_pressure(mock_lemonade):
    from governor.lemonade import LemonadeStatus
    mock_lemonade.return_value = LemonadeStatus(
        online=True, authenticated=True, model_loaded="gpt-oss-20b-MXFP4"
    )
    obs = observe_handoff(telemetry=_snapshot(vram_free=300))
    assert obs.state == HandoffState.GPU_MEMORY_PRESSURE


@patch("governor.handoff.check_lemonade")
def test_handoff_idle(mock_lemonade):
    from governor.lemonade import LemonadeStatus
    mock_lemonade.return_value = LemonadeStatus(
        online=True, authenticated=True, model_loaded="gpt-oss-20b-MXFP4"
    )
    obs = observe_handoff(telemetry=_snapshot(vram_free=2000, util=0))
    assert obs.state == HandoffState.AI_INFERENCE_IDLE
