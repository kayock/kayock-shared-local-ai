# Governor Benchmark Results — 2026-09-01

**Classification: VERIFIED FROM RUNTIME MEASUREMENT**

Source artifact: `governor/data/benchmark_20260901T155952Z.json` (local, gitignored)  
Model: `gpt-oss-20b-MXFP4` via Lemonade  
Hardware: Quadro P2000 (4 GB VRAM)  
Profile label in run: `default` (config: `max_tokens=128`, `temperature=0.7`)

## Aggregate Baseline (3-prompt harness)

| Metric | Value |
|--------|-------|
| Avg TTFT | **7.15 s** |
| Avg tokens/sec | **7.01** |
| Avg total time | **8.97 s** |
| Peak VRAM (all prompts) | **3191 MiB** |
| Peak temperature (all prompts) | **57 °C** |
| Errors | **0** |

First prompt TTFT (11.46 s) includes **cold-start / model-load penalty**; subsequent prompts were faster.

## Per-Prompt Results

| Prompt ID | TTFT (s) | Total (s) | Tokens | TPS | Peak VRAM (MiB) | Peak temp (°C) |
|-----------|----------|-----------|--------|-----|-----------------|----------------|
| `short_greeting` | 11.46 | 11.71 | 1 | 4.00 | 3191 | 53 |
| `factual_brief` | 3.62 | 8.24 | 47 | 10.19 | 3191 | 56 |
| `reasoning_light` | 6.36 | 6.95 | 4 | 6.83 | 3191 | 57 |

## Optimization Run Status

**VERIFIED LIVE OPTIMIZATION** — corrected `THROUGHPUT` run documented in [`throughput-optimization-2026-09-01.md`](throughput-optimization-2026-09-01.md).

| Result | Value |
|--------|-------|
| Baseline score | 14.64 |
| Winning config | `max_tokens=480`, `temperature=0.7` |
| Winning score | 15.26 (~4.22% improvement) |
| Winner TTFT / TPS | 6.74 s / 7.44 |

An earlier pre-`d682462` THROUGHPUT run produced incorrect results and is **not** contest evidence.

`LOW_LATENCY` multi-candidate optimization was not separately documented at time of initial benchmark capture.

## Scoring

Composite optimizer scores were **not recorded** for this live benchmark run (benchmark-only command does not compute scores). Scores exist only in mocked unit tests.

## Service Health After Benchmark

| Service | Status (post-run) |
|---------|-------------------|
| `father-fox-voice.service` | **active** |
| Lemonade `/health` | **HTTP 200** |

No modifications were made to Father Fox, Lemonade, or RVC.

## Sanitization

No API keys, client IPs, or protected environment values are included in this document.
