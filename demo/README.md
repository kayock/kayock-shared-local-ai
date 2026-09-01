# Kayock Shared Local AI — Contest Demo

**One Lemonade server. Multiple local-AI workloads.**  
**Shared hardware. No cloud required.**

This folder is the judge-friendly entry point for the [AMD Lemonade Developer Challenge](https://www.amd.com/en/developer/resources/technical-articles/2025/amd-lemonade-developer-challenge.html). Everything here is grounded in **verified runtime evidence** already committed in this repository — no fabricated metrics, no cloud inference, no exaggerated claims.

## Start Here

| Document | Purpose |
|----------|---------|
| [demo-script.md](demo-script.md) | 2–3 minute spoken demonstration script |
| [demo-runbook.md](demo-runbook.md) | Step-by-step recording checklist |
| [contest-summary.md](contest-summary.md) | Submission-ready descriptions (short, ~100-word, ~250-word) |
| [verified-results.md](verified-results.md) | Authoritative list of verified results with evidence links |
| [screenshots/README.md](screenshots/README.md) | Screenshot capture checklist (placeholders only) |

**Live showcase:** [Kayock Local AI Trophy Room](../trophy-room/README.md) at **http://127.0.0.1:8771**

---

## Two Verified Innovations

### 1. Dynamic GPU Handoff

On a **4 GB GPU**, a 20B Lemonade model and RVC voice weights cannot coexist. Father Fox Voice Hub coordinates explicit handoff:

```
Father Fox
  → Lemonade / gpt-oss-20b-MXFP4
  → special RVC request
  → Lemonade model unload (POST /v1/unload)
  → VRAM released
  → RVC uses GPU
  → next normal request
  → Lemonade returns successfully
```

**Verified runtime timestamps** (2026-09-01, local journal):

| Time | Event |
|------|-------|
| **00:17:39** | Father Fox → Lemonade (`gpt-oss-20b-MXFP4`) |
| **00:18:08** | Lemonade model unload |
| **00:18:12** | VRAM released for RVC |
| **00:18:28** | RVC `/api/talk` **200 OK** |
| **00:20:15** | Return to Lemonade inference |
| **00:20:46** | Subsequent `/api/talk` **200 OK** |

Evidence: [`evidence/verified-tests/2026-09-01-father-fox-journal.md`](../evidence/verified-tests/2026-09-01-father-fox-journal.md)

Reference integration code: [`integrations/father-fox/`](../integrations/father-fox/), [`integrations/rvc-handoff/`](../integrations/rvc-handoff/)

---

### 2. Kayock AI Resource Governor

The Governor is a **safe, read-only** local prototype that helps squeeze more throughput from Lemonade on constrained hardware. It:

- **Monitors** GPU and system state (nvidia-smi, psutil)
- **Benchmarks** Lemonade with a fixed prompt harness
- **Generates** bounded safe candidates (`max_tokens`, `temperature` only)
- **Scores** each candidate with a deterministic composite metric
- **Rejects** regressions below baseline
- **Tracks** the global best across all candidates
- **Saves** the winning profile to local SQLite
- **Does not** change voltage, clocks, or disable hardware protections

**Corrected verified THROUGHPUT result** (post-optimizer fix, commit `d682462`):

| | Baseline | Winner |
|---|----------|--------|
| `max_tokens` | 512 | **480** |
| `temperature` | 0.7 | **0.7** |
| Score | **14.639872171624882** | **15.25802453529699** |
| Improvement | — | **~+4.22%** |
| TTFT (avg) | — | **6.7409 s** |
| TPS (avg) | — | **7.4384** |

**Candidate decisions** (corrected run):

| Decision | Meaning | Examples |
|----------|---------|----------|
| **REJECT** | Does not beat baseline | `{480, 0.6}`, `{512, 0.6}` |
| **KEEP** | New global best | `{480, 0.7}` |
| **NOT_BEST** | Beats baseline but not current best | `{480, 0.8}`, `{512, 0.8}` |

Live testing discovered an **order-dependent global-best bug** in the optimizer. It was fixed in commit **`d682462`** with regression tests before the corrected contest result was recorded. An earlier pre-fix THROUGHPUT run is **not** contest evidence.

Evidence: [`governor/evidence/throughput-optimization-2026-09-01.md`](../governor/evidence/throughput-optimization-2026-09-01.md)

Governor docs: [`governor/README.md`](../governor/README.md)

---

## What Is Verified vs Planned

| Capability | Status |
|------------|--------|
| Father Fox → Lemonade → RVC GPU handoff | **VERIFIED** |
| Return to Lemonade after RVC | **VERIFIED** |
| Kayock AI Resource Governor (telemetry, benchmark, optimizer) | **VERIFIED** |
| Kayock Local AI Trophy Room (observability dashboard) | **VERIFIED** |
| Whispeer, NOMAD, Comic Reader, Audio Notebook | **PLANNED** — not demonstrated |

## Release Tag

Contest-ready release: **`contest-v0.3-trophy-room`**

Includes verified Lemonade/RVC GPU handoff, Governor v0.1, corrected +4.22% THROUGHPUT optimization, and Trophy Room.
