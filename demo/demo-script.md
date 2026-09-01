# Contest Demo Script (2–3 minutes)

Natural spoken language for recording. Pair with [demo-runbook.md](demo-runbook.md) and the [Trophy Room](../trophy-room/README.md).

---

## 0:00–0:20 — The Problem

> "Local AI is powerful, but GPU memory is finite. On my machine — a Quadro P2000 with four gigabytes of VRAM — I can't run a twenty-billion-parameter Lemonade model and an RVC voice model at the same time. Most people would push one workload to the cloud. I didn't want that. I wanted everything local, on one GPU, with no API bills."

---

## 0:20–0:45 — Trophy Room and Architecture

> "This is Kayock Shared Local AI. The Trophy Room is our contest showcase — a read-only dashboard at port 8771. It doesn't run inference; it shows what's actually happening on the machine."

*Switch to Trophy Room main view.*

> "One Lemonade server on port 13305 serves the LLM. Father Fox Voice Hub on 8765 handles speech. RVC character voices run on 8766. They share the same GPU — but only one heavy workload at a time."

*Briefly show Local AI Clients tab if services are online.*

---

## 0:45–1:30 — GPU Handoff

*Switch to GPU Handoff view.*

> "Here's the innovation: dynamic GPU handoff. When Father Fox needs Lemonade, it calls chat completions with gpt-oss-20b-MXFP4. At seventeen thirty-nine, the journal shows exactly that."

*Point to timeline: 00:17:39.*

> "When the user picks a special RVC character voice, Father Fox doesn't crash or run out of memory. It calls Lemonade's unload endpoint, releases VRAM, and hands the GPU to RVC."

*Walk through 00:18:08, 00:18:12, 00:18:28.*

> "Eighteen oh-eight — unload. Eighteen twelve — VRAM released. Eighteen twenty-eight — RVC talk request returns two hundred OK. That's real runtime evidence from September first, pulled from the systemd journal."

---

## 1:30–1:55 — Return to Lemonade

> "The handoff isn't one-way. When the user asks a normal question again, Father Fox goes back to Lemonade — no restart, no manual intervention."

*Point to 00:20:15 and 00:20:46.*

> "Twenty fifteen — back to Lemonade. Twenty forty-six — another successful talk request. The cycle works."

---

## 1:55–2:30 — Resource Governor

*Switch to Trophy Room Governor panel or Model Arena.*

> "Sharing GPU isn't just about handoff — it's also about getting the most from what you have. The Kayock AI Resource Governor monitors telemetry, benchmarks Lemonade, and tries bounded safe settings."

> "On the THROUGHPUT profile, baseline was five-twelve tokens at temperature zero-point-seven — score fourteen point six four. The winner was four-eighty tokens, same temperature — score fifteen point two six. That's about four point two two percent improvement, verified live. The optimizer correctly rejected worse candidates, kept the global best, and flagged beat-baseline-but-not-best configs as NOT_BEST."

---

## 2:30–2:50 — Evidence Vault

*Switch to Evidence Vault tab.*

> "Every claim in this project links to real evidence — journal excerpts, benchmark results, optimization decisions. We even found and fixed an optimizer bug during live testing, documented the corrected run, and excluded the buggy pre-fix result from contest evidence."

*Expand Father Fox journal or throughput evidence if time allows.*

---

## 2:50–3:00 — Closing

> "Kayock Shared Local AI: one Lemonade server, multiple workloads, shared hardware, no cloud required. Open source, reusable, and built for real consumer GPUs. Thank you."

---

**Total target:** ~2:50. Adjust pacing; silence is fine during UI navigation.
