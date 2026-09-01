# THROUGHPUT Optimization — Verified Live Run (Corrected)

**Classification: VERIFIED LIVE OPTIMIZATION**

**Date:** 2026-09-01 (UTC)  
**Profile:** `THROUGHPUT`  
**Model:** `gpt-oss-20b-MXFP4` via Lemonade  
**Hardware:** Quadro P2000 (4 GB VRAM)

> **Note:** An earlier THROUGHPUT run on the same day used buggy optimizer logic (pre-`d682462`) and incorrectly selected `{max_tokens: 512, temperature: 0.8}`. **That run is not contest evidence.** This document records only the corrected run.

## Bug Fix Context

Live testing exposed an **order-dependent global-best bug**: candidates that beat the original baseline overwrote `best_config` even when a higher-scoring candidate had already been found. Fixed in commit **`d682462`** with regression tests in `governor/tests/test_optimizer.py`.

## Baseline

| Field | Value |
|-------|-------|
| Configuration | `max_tokens=512`, `temperature=0.7` |
| Score | **14.639872171624882** |

## Winner

| Field | Value |
|-------|-------|
| Configuration | `max_tokens=480`, `temperature=0.7` |
| Score | **15.25802453529699** |
| Improvement vs baseline | **~4.22%** |
| TTFT (avg) | **6.7409 s** |
| TPS (avg) | **7.4384** |

Saved to `saved_profiles` table as `THROUGHPUT` at `2026-09-01T16:16:43Z`.

## Every Candidate (Corrected Run)

| # | max_tokens | temperature | Score | TTFT (s) | TPS | Decision | Reason |
|---|------------|-------------|-------|----------|-----|----------|--------|
| — | 512 | 0.7 | 14.6399 | — | — | *(baseline)* | Starting configuration |
| 1 | 480 | 0.6 | 14.3498 | 3.86 | 6.94 | **REJECT** | Does not beat baseline 14.6399 |
| 2 | 480 | 0.7 | **15.2580** | 6.74 | 7.44 | **KEEP** | New global best (previous best 14.6399) |
| 3 | 480 | 0.8 | 15.1551 | 6.26 | 7.38 | **NOT_BEST** | Beats baseline but not current best 15.2580 |
| 4 | 512 | 0.6 | 14.1270 | 8.03 | 6.88 | **REJECT** | Does not beat baseline 14.6399 |
| 5 | 512 | 0.8 | 15.0987 | 8.15 | 7.37 | **NOT_BEST** | Beats baseline but not current best 15.2580 |

## Optimizer Behavior Verified

| Behavior | Observed |
|----------|----------|
| Rejected configurations below baseline | **Yes** — `{480, 0.6}` and `{512, 0.6}` → `REJECT` |
| Retained new global best | **Yes** — `{480, 0.7}` → `KEEP`, final active config |
| Recognized beat-baseline-but-not-best | **Yes** — `{480, 0.8}` and `{512, 0.8}` → `NOT_BEST` |
| Automatically saved winning profile | **Yes** — `saved_profiles.THROUGHPUT` = `{480, 0.7}` @ score 15.258 |

## Completion Event

```json
{
  "baseline_score": 14.639872171624882,
  "best_score": 15.25802453529699,
  "active_config": {"max_tokens": 480, "temperature": 0.7}
}
```

## Source

Persisted in `governor/data/governor.sqlite` (gitignored):

- `optimization_decisions` rows 15–19
- `events` rows 9–10
- `saved_profiles` row `THROUGHPUT`

No API keys or protected environment values are included in this document.

## Superseded (Do Not Use)

| Run | Baseline | Reported best | Bug |
|-----|----------|---------------|-----|
| Pre-`d682462` THROUGHPUT | 14.3226 | `{512, 0.8}` @ 14.90 | Order-dependent overwrite |
