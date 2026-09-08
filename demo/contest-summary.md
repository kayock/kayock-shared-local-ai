# Contest Submission Summary

Copy-ready text for the 2026 AMD Lemonade Developer Challenge form. All claims are **verified** in this repository unless marked PLANNED.

---

## One-Liner (1–2 sentences)

Kayock Shared Local AI demonstrates dynamic GPU handoff between Lemonade LLM inference and RVC voice synthesis on a single 4 GB GPU, plus a safe local Resource Governor that achieved a verified **+4.22% composite THROUGHPUT score improvement** — all local, no cloud inference required.

---

## ~100 Words

Kayock Shared Local AI solves a constraint measured on a 4 GB Quadro P2000: the resident 20B Lemonade model allocation and RVC voice workload cannot remain on the GPU together. Father Fox Voice Hub coordinates explicit `POST /v1/unload`, VRAM release, RVC synthesis, and automatic return to Lemonade — proven with runtime journal timestamps on 2026-09-01. The Kayock AI Resource Governor adds read-only telemetry, bounded benchmarking, and deterministic optimization that improved its composite THROUGHPUT score by approximately 4.22% without touching voltage or hardware protections. A Trophy Room dashboard presents verified evidence for judges. Open source, reusable, and built for resource-constrained local AI.

---

## ~250 Words

Kayock Shared Local AI focuses on a practical local-AI constraint: sharing one limited GPU between multiple heavy workloads without falling back to cloud inference.

**Dynamic GPU handoff (verified):** On an NVIDIA Quadro P2000 (4 GB), Father Fox drives Lemonade `gpt-oss-20b-MXFP4` for conversation, then unloads the model before RVC character-voice synthesis. Runtime journal evidence from 2026-09-01 records the full cycle: Lemonade inference at 00:17:39, unload at 00:18:08, VRAM release at 00:18:12, successful RVC at 00:18:28, return to Lemonade at 00:20:15, and a subsequent successful request at 00:20:46. Reference integration code is included for adoption in other local apps.

**Kayock AI Resource Governor (verified experimental prototype):** The Governor monitors GPU state, benchmarks Lemonade, generates bounded `max_tokens`/`temperature` candidates, scores them with a deterministic composite metric, rejects regressions, tracks the global best, and saves the winning profile. A corrected live THROUGHPUT run improved the composite score from 14.64 to 15.26 (~+4.22%). An optimizer bug found during live testing was fixed and regression-tested; pre-fix results are excluded from contest evidence.

**Trophy Room:** A read-only local contest dashboard at port 8771 surfaces milestones, live telemetry, and a sanitized evidence vault.

**Planned / not demonstrated in this contest repository:** Whispeer, NOMAD RAG backend, Comic Reader, Audio Notebook.

Lemonade is the OpenAI-compatible runtime that makes this architecture practical — one local API for chat completions, model unload, health checks, and future clients.

---

## Technical Highlights

- OpenAI-compatible Lemonade API (`/v1/chat/completions`, `/v1/unload`, `/health`)
- Explicit VRAM coordination before RVC on the verified 4 GB Quadro P2000 setup
- Runtime-verified handoff with journal timestamps (not simulated)
- Deterministic optimizer with REJECT / KEEP / NOT_BEST decisions
- Read-only hardware telemetry (nvidia-smi, psutil) — no overclocking or voltage changes
- SQLite persistence for benchmark and optimization history
- 26 automated tests (Governor + Trophy Room)
- Sanitized evidence — no API keys or private IPs in committed docs

---

## Creativity and Innovation

- **Cooperative sharing** instead of cloud fallback on constrained hardware
- **Lifecycle-aware handoff** integrated into a real voice assistant (Father Fox), not a toy script
- **Evidence-first optimizer engineering** — bug found in live testing, fixed, corrected result documented, buggy run explicitly excluded
- **Trophy Room** — contest-grade observability layer that makes verified claims inspectable in seconds

---

## Community and Open-Source Impact

- MIT-licensed reference clients in `integrations/` for Lemonade chat and RVC handoff
- Reusable Governor pattern for Lemonade deployments on limited VRAM
- Evidence-first documentation — judges and contributors can trace every metric to a file
- Designed for adoption on consumer hardware, not datacenter assumptions

---

## Why Lemonade Matters to This Project

Lemonade is the shared inference layer. Father Fox, the Resource Governor, and future clients can speak the same OpenAI-compatible API. The `/v1/unload` endpoint is the critical hook that makes GPU handoff possible without restarting services. The verified contest path uses Lemonade for local inference and explicit model lifecycle control.

---

## Verified vs Future (Do Not Conflate)

| Verified in this submission | PLANNED / not demonstrated |
|-----------------------------|----------------------------|
| Father Fox → Lemonade → RVC handoff | Whispeer client |
| Return to Lemonade after RVC | NOMAD RAG backend |
| Governor telemetry, benchmark, THROUGHPUT optimize | Comic Reader, Audio Notebook |
| Trophy Room dashboard | Automatic Governor → Father Fox config push |
| +4.22% corrected composite THROUGHPUT score | LOW_LATENCY optimization evidence |
