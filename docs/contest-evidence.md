# Contest Evidence

Evidence is classified throughout this repository so judges can distinguish runtime proof, source verification, experimental measurements, and future work.

| Tier | Label | Meaning |
|------|-------|---------|
| 1 | **VERIFIED FROM RUNTIME LOG** | Captured from `journalctl` or equivalent system logs |
| 2 | **VERIFIED FROM SOURCE CODE** | Confirmed by reading committed application/reference source |
| 3 | **VERIFIED EXPERIMENTAL MEASUREMENT** | Captured from a live benchmark/optimization run and preserved as evidence |
| 4 | **PLANNED / FUTURE** | Design intent only; not demonstrated in this contest repository |

## Runtime Evidence Recovered

**VERIFIED FROM RUNTIME LOG** — journal entries from `father-fox-voice.service` on **2026-09-01 between 00:17:39 and 00:20:46** (local time).

Retrieval command:

```bash
journalctl -u father-fox-voice.service \
  --since "2026-09-01 00:10:00" \
  --until "2026-09-01 00:30:00" \
  --no-pager
```

Full sanitized excerpt: [`evidence/verified-tests/2026-09-01-father-fox-journal.md`](../evidence/verified-tests/2026-09-01-father-fox-journal.md)

### Key runtime log lines

```
[Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)
[RVC GPU handoff] Unloading Lemonade model: gpt-oss-20b-MXFP4
[RVC GPU handoff] Lemonade VRAM released for RVC.
[RVC GPU handoff] GPU already clear of Ollama models.
POST /api/talk HTTP/1.1" 200 OK
[Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)
POST /api/talk HTTP/1.1" 200 OK
```

The second `Model Only -> Lemonade` line at **00:20:15** confirms the full handoff cycle: unload → RVC → return to Lemonade inference.

## Verified from Source Code

The repository includes cleaned reference extracts of the live Father Fox integration:

| Capability | Reference |
|------------|-----------|
| Lemonade chat for `Model Only` | [`integrations/father-fox/lemonade_chat.py`](../integrations/father-fox/lemonade_chat.py) |
| `POST /v1/unload` with `model_name` | [`integrations/rvc-handoff/lemonade_unload.py`](../integrations/rvc-handoff/lemonade_unload.py) |
| RVC handoff for special voices | Same unload/handoff reference |
| 1-second VRAM grace period | `VRAM_GRACE_SECONDS = 1.0` |
| Return to Lemonade on later request | Corroborated by runtime journal at 00:20:15 |

## Verified Experimental Measurements — Governor

The Kayock AI Resource Governor is an **implemented experimental prototype** with committed source, automated tests, and live measurement evidence.

### Benchmark harness

[`governor/evidence/benchmark-results-2026-09-01.md`](../governor/evidence/benchmark-results-2026-09-01.md) records a live three-prompt run against `gpt-oss-20b-MXFP4` on the Quadro P2000:

- Avg TTFT: **7.15 s**
- Avg generation throughput: **7.01 tokens/s**
- Peak VRAM: **3191 MiB**
- Peak temperature: **57 °C**
- Errors: **0**

These are benchmark measurements, not values inferred from journal gaps.

### Corrected THROUGHPUT optimization

[`governor/evidence/throughput-optimization-2026-09-01.md`](../governor/evidence/throughput-optimization-2026-09-01.md) records the corrected live optimizer run after commit `d682462` fixed an order-dependent global-best bug.

| Field | Baseline | Winner |
|-------|----------|--------|
| `max_tokens` | 512 | 480 |
| `temperature` | 0.7 | 0.7 |
| Composite score | 14.639872171624882 | 15.25802453529699 |
| Composite-score improvement | — | **~+4.22%** |
| Winner TTFT | — | 6.7409 s |
| Winner TPS | — | 7.4384 |

The **+4.22% figure refers to the deterministic composite THROUGHPUT score**, not a claim that raw tokens/second alone increased by 4.22%.

The earlier pre-fix optimizer run is explicitly excluded from contest evidence.

## Trophy Room

The Trophy Room is a read-only local contest dashboard that surfaces committed evidence, verified constants, service state, and GPU telemetry. It runs locally on port `8771`; `127.0.0.1` is not a public hosted showcase URL.

See [`trophy-room/README.md`](../trophy-room/README.md).

## Not Demonstrated in This Contest Repository

| Item | Status |
|------|--------|
| Whispeer as a demonstrated Lemonade client | **PLANNED / FUTURE** |
| NOMAD as a demonstrated Lemonade client | **PLANNED / FUTURE** |
| Comic Reader integration | **PLANNED / not part of submitted contest evidence** |
| Audio Notebook integration | **PLANNED / not part of submitted contest evidence** |
| Automatic Governor → Father Fox config push | **PLANNED** |
| LOW_LATENCY live optimization evidence | **NOT DOCUMENTED AS CONTEST EVIDENCE** |

## Evidence Repository Policy

See [`evidence/README.md`](../evidence/README.md). Unsanitized logs, credentials, model weights, databases, and private data are excluded from the public repository.
