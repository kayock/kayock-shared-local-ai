# Roadmap

## Completed — Demonstrated in This Repository

- [x] Lemonade chat completions for `Model Only` (`gpt-oss-20b-MXFP4`)
- [x] `POST /v1/unload` before special RVC voices
- [x] VRAM release confirmed in runtime journal (2026-09-01)
- [x] Return to Lemonade on next request (runtime journal 00:20:15)
- [x] Reference integration examples + contest documentation
- [x] Kayock AI Resource Governor telemetry and benchmark harness
- [x] Corrected THROUGHPUT optimizer with live evidence
- [x] Trophy Room local observability dashboard
- [x] Automated Governor + Trophy Room test suites

## Contest Submission Evidence

- [x] Runtime journal evidence in `evidence/verified-tests/`
- [x] Live Governor benchmark evidence in `governor/evidence/`
- [x] Corrected THROUGHPUT optimization evidence
- [x] Demo scripts and recording runbook in `demo/`
- [x] Verified-results index for judges
- [x] Public claims distinguish verified work from future work

The corrected optimizer result is a **~+4.22% improvement in the composite THROUGHPUT score**, not a claim that raw tokens/second alone improved by 4.22%.

## Implemented but Experimental

### Kayock AI Resource Governor

- [x] Telemetry CLI (`python -m governor status`)
- [x] Benchmark harness (requires API key + live Lemonade)
- [x] Deterministic optimizer (per-request params only)
- [x] Handoff state observer
- [x] Local dashboard
- [ ] Load-time ctx-size auto-apply (PLANNED)
- [ ] Father Fox opt-in integration (PLANNED)

### Trophy Room

- [x] Read-only local dashboard on port 8771
- [x] Five judge-facing views
- [x] Evidence Vault backed by committed sanitized evidence
- [x] Live service/GPU observability when dependencies are available

## Planned / Future — Not Demonstrated in Contest Evidence

### Whispeer Integration

Social-agent client intended to use Lemonade as a shared local inference layer. Not demonstrated in this contest repository.

### NOMAD as Additional Client

Legacy/local RAG backend for named collections; separate from the verified Lemonade contest path.

### Comic Reader

Future local-AI client/workload. Not part of the submitted contest evidence.

### Audio Notebook

Future local speech/transcription workflow. Not part of the submitted contest evidence.

### Resource Governor Integration

- [ ] Optional safe profile application to Father Fox
- [ ] Load-time context-size coordination with explicit approval
- [ ] Broader workload-profile validation

## Future Evidence Work

- [ ] Separate LOW_LATENCY live optimization report
- [ ] Additional hardware comparisons
- [ ] More repeated benchmark runs for confidence intervals / variance reporting
- [ ] Public demo screenshots and/or hosted video links near the repository entry point

## Non-Goals

- Modifying live deployed applications from this repository without explicit opt-in
- Shipping model weights or private RAG data
- Cloud inference fallback in the verified local path
- Hardware overclocking, voltage changes, or disabling thermal protections
