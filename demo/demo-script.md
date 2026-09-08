# Contest Demo Script (2–3 minutes)

Natural spoken language for recording. Pair with [demo-runbook.md](demo-runbook.md) and the [Trophy Room](../trophy-room/README.md).

---

## 0:00–0:20 — The Problem

> "Local AI is powerful, but GPU memory is finite. On my machine — a Quadro P2000 with four gigabytes of VRAM — the resident twenty-billion-parameter Lemonade model allocation and the RVC voice workload can't stay on the GPU together. I wanted both workloads local, on one GPU, without cloud inference."

---

## 0:20–0:45 — Trophy Room and Architecture

> "This is Kayock Shared Local AI. The Trophy Room is our local contest showcase — a read-only dashboard at port 8771. It doesn't run inference; it shows what's actually happening on the machine."

*Switch to Trophy Room main view.*

> "One Lemonade server on port 13305 serves the LLM. Father Fox Voice Hub on 8765 handles speech. RVC character voices run on 8766. They share the same GPU — but only one heavy workload at a time on this four-gigabyte setup."

*Briefly show Local AI Clients tab if services are online.*

---

## 0:45–1:30 — GPU Handoff

*Switch to GPU Handoff view.*

> "Here's the innovation: dynamic GPU handoff. When Father Fox needs Lemonade, it calls chat completions with gpt-oss-20b-MXFP4. At seventeen thirty-nine, the journal shows exactly that."

*Point to timeline: 00:17:39.*

> "When the user picks a special RVC character voice, Father Fox calls Lemonade's unload endpoint, releases VRAM, and hands the GPU to RVC."

*Walk through 00:18:08, 00:18:12, 00:18:28.*

> "Eighteen oh-eight — unload. Eighteen twelve — VRAM released. Eighteen twenty-eight — RVC talk request returns two hundred OK. That's runtime evidence from September first, pulled from the systemd journal."

---

## 1:30–1:55 — Return to Lemonade

> "The handoff isn't one-way. When the user asks a normal question again, Father Fox goes back to Lemonade — no Lemonade restart and no manual model reload step."

*Point to 00:20:15 and 00:20:46.*

> "Twenty fifteen — back to Lemonade. Twenty forty-six — another successful talk request. The cycle works."

---

## 1:55–2:30 — Resource Governor

*Switch to Trophy Room Governor panel or Model Arena.*

> "Sharing GPU isn't just about handoff — it's also about measuring what works best on limited hardware. The Kayock AI Resource Governor monitors telemetry, benchmarks Lemonade, and tries bounded software settings."

> "On the THROUGHPUT profile, the baseline was five-twelve tokens at temperature zero-point-seven, with a composite score of fourteen point six four. The winner was four-eighty tokens at the same temperature, with a composite score of fifteen point two six. That's about a four point two two percent improvement in the composite THROUGHPUT score. The winning run measured roughly six point seven four seconds time-to-first-token and seven point four four generated tokens per second."

---

## 2:30–2:50 — Evidence Vault

*Switch to Evidence Vault tab.*

> "Every contest claim links to evidence — journal excerpts, benchmark results, optimization decisions. We even found and fixed an optimizer bug during live testing, documented the corrected run, and excluded the buggy pre-fix result from contest evidence."

*Expand Father Fox journal or throughput evidence if time allows.*

---

## 2:50–3:00 — Closing

> "Kayock Shared Local AI: one Lemonade server, multiple workloads, shared hardware, no cloud inference in the verified path. Open source, reusable, and built for real consumer hardware. Thank you."

---

**Total target:** ~2:50. Adjust pacing; silence is fine during UI navigation.
