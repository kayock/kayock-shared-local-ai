# Roadmap

## Completed — Demonstrated in This Repository

- [x] Lemonade chat completions for `Model Only` (`gpt-oss-20b-MXFP4`)
- [x] `POST /v1/unload` before special RVC voices
- [x] VRAM release confirmed in runtime journal (2026-09-01)
- [x] Return to Lemonade on next request (runtime journal 00:20:15)
- [x] Reference integration examples + contest documentation

## Contest Submission Ready

- [x] Runtime journal evidence in `evidence/verified-tests/`
- [x] Demo script in `docs/demo-script.md`
- [x] Public-facing claims scoped to Father Fox + RVC only

## PLANNED / FUTURE

### Whispeer Integration

Social-agent client — source at `/home/kayock/kayock-social-agent` not present on this machine.

### NOMAD as Additional Client

Legacy RAG backend for named collections; separate from Lemonade demo path.

### Kayock AI Resource Governor

**IMPLEMENTED BUT EXPERIMENTAL** on branch `governor-v0.1`:

- [x] Telemetry CLI (`python -m governor status`)
- [x] Benchmark harness (requires API key + live Lemonade)
- [x] Deterministic optimizer (per-request params only)
- [x] Handoff state observer
- [x] Local dashboard
- [ ] Load-time ctx-size auto-apply (PLANNED)
- [ ] Father Fox opt-in integration (PLANNED)

### Formal Benchmarks

TTFT, TPS, and VRAM measurements — not captured in recovered journal evidence.

## Non-Goals

- Modifying live deployed applications from this repository
- Shipping model weights or private RAG data
- Cloud inference fallback
