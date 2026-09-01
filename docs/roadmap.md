# Roadmap

## Completed (Verified in Father Fox Source)

- [x] Lemonade chat completions for `Model Only` conversations
- [x] Default model `gpt-oss-20b-MXFP4`
- [x] `POST /v1/unload` before special RVC voices
- [x] Legacy Ollama GPU cleanup alongside Lemonade unload
- [x] 1-second VRAM grace period after unload

## In Progress / Documented Here

- [x] Contest documentation repository (this repo)
- [x] Reference integration examples extracted from Father Fox
- [x] Architecture and GPU handoff diagrams

## Blocked / Not Found Locally

- [ ] Whispeer Lemonade integration — source at `/home/kayock/kayock-social-agent` not present
- [ ] `AMD_Lemonade_Contest_Evidence_Log.md` — file not found; cannot attach formal test results
- [ ] Runtime benchmarks (TTFT, TPS, VRAM measurements) — awaiting evidence log

## Future Work

### Kayock AI Resource Governor

A planned self-optimizer for multi-app GPU sharing. See [`governor/README.md`](../governor/README.md).

Planned capabilities:

| Area | Goal |
|------|------|
| TTFT | Minimize time-to-first-token across apps |
| TPS | Track and optimize tokens per second |
| VRAM | Monitor and enforce memory budgets |
| Temperature | Tune per-app inference parameters |
| Utilization | Balance GPU load across workloads |
| Context | Right-size context windows per request type |
| Batch | Coordinate batching where safe |
| Threads | Tune CPU/GPU thread allocation |
| App priority | Prefer interactive voice over background tasks |
| Unload/reload | Centralized handoff policy vs. per-app calls |
| Safe benchmarking | Non-destructive perf probes with rollback |
| Scoring | Rank configuration changes by measured improvement |
| Rollback | Revert failed optimizations automatically |

**Status:** Design only. No implementation exists in this repository.

### Whispeer Integration

When `kayock-social-agent` source becomes available, extract a Lemonade client reference mirroring the Father Fox pattern and update [`integrations/whispeer/`](../integrations/whispeer/).

### Centralized Evidence Collection

Formal test harness that writes to `evidence/verified-tests/` with sanitized output, replacing ad-hoc log collection.

### Multi-GPU Support

Current documentation assumes a single Quadro P2000. Governor design should extend to multiple AMD/NVIDIA devices when hardware allows.

## Non-Goals

- Replacing or modifying existing deployed applications
- Shipping model weights or private RAG data
- Cloud inference fallback
