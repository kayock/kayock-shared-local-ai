from governor.telemetry import _parse_nvidia_smi_csv, _parse_float


def test_parse_nvidia_smi_csv():
    stdout = """name, utilization.gpu [%], memory.used [MiB]
Quadro P2000, 10 %, 3191 MiB"""
    row = _parse_nvidia_smi_csv(stdout)
    assert row["name"] == "Quadro P2000"
    assert _parse_float(row["utilization.gpu [%]"]) == 10.0


def test_parse_float_na():
    assert _parse_float("[N/A]") is None
    assert _parse_float("43") == 43.0
