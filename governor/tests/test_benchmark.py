import json

from governor.benchmark import _parse_sse_chunk, _estimate_tokens
from governor.profiles import RequestConfig, generate_candidates, get_profile, WorkloadProfile


def test_request_config_bounds():
    cfg = RequestConfig(max_tokens=128, temperature=0.7)
    cfg.validate()
    try:
        RequestConfig(max_tokens=8, temperature=0.7).validate()
        assert False, "should fail"
    except ValueError:
        pass


def test_generate_candidates_bounded():
    baseline = RequestConfig(max_tokens=128, temperature=0.7)
    profile = get_profile(WorkloadProfile.LOW_LATENCY)
    candidates = generate_candidates(baseline, profile)
    assert len(candidates) <= 6
    for c in candidates:
        c.validate()


def test_sse_parse():
    line = 'data: {"choices":[{"delta":{"content":"Hi"}}]}'
    assert _parse_sse_chunk(line) == "Hi"
    assert _parse_sse_chunk("data: [DONE]") is None


def test_token_estimate():
    assert _estimate_tokens("one two three") == 3
