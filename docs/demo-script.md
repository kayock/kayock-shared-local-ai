# Contest Demo Script (2–3 minutes)

Use this script when recording the AMD Lemonade Developer Challenge submission video. All steps below are **verified from runtime journal** on 2026-09-01 unless noted.

Evidence: [`evidence/verified-tests/2026-09-01-father-fox-journal.md`](../evidence/verified-tests/2026-09-01-father-fox-journal.md)

---

## 1. Project Problem (15 sec)

> "On a laptop with only 4 GB of GPU memory, you cannot keep a 20-billion-parameter language model and a voice-conversion model loaded at the same time. Most people assume you need cloud inference or a bigger GPU. We show cooperative local sharing instead."

**On screen:** Diagram from README — Quadro P2000 with LLM + RVC marked as incompatible.

---

## 2. Father Fox Using Lemonade (20 sec)

> "Father Fox is a voice assistant. When I select Model Only, it sends my question to a local Lemonade server — no cloud."

**Action:** Open Father Fox on a phone or browser. Confirm Knowledge is set to **Model Only**.

**On screen:** Father Fox UI + terminal or journal tail showing:
```
[Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)
```

---

## 3. Model Loaded: gpt-oss-20b-MXFP4 (10 sec)

> "The model is OpenAI's gpt-oss-20b in MXFP4 quantization, served by Lemonade on port 13305."

**On screen:** Lemonade status or the log line above. Optional: `lemonade ps` if available.

---

## 4. Ask a Normal Question (15 sec)

> "I'll ask a conversational question and get a spoken reply with a standard voice."

**Action:** Tap to talk, ask something simple ("What is photosynthesis in one sentence?"), wait for reply.

**On screen:** Transcript + audio playing with a standard Kokoro voice.

---

## 5. Special RVC Voice Request (15 sec)

> "Now I switch to a character voice — Batman, Iron Man, or another special RVC voice. These require a separate GPU-heavy voice model."

**Action:** Change Voice to a special character (e.g., Iron Man). Ask another question.

---

## 6. Lemonade Unload (15 sec)

> "Before RVC can load, Father Fox calls Lemonade's unload API to free GPU memory."

**On screen:** Journal or log:
```
[RVC GPU handoff] Unloading Lemonade model: gpt-oss-20b-MXFP4
```

---

## 7. VRAM Release (10 sec)

> "Four seconds later, the log confirms VRAM is released."

**On screen:**
```
[RVC GPU handoff] Lemonade VRAM released for RVC.
[RVC GPU handoff] GPU already clear of Ollama models.
```

---

## 8. RVC Workload Completes (15 sec)

> "The character voice synthesizes and plays back. The HTTP request succeeds."

**On screen:**
```
POST /api/talk HTTP/1.1" 200 OK
```
Plus audio of the character voice reply.

---

## 9. Return to Lemonade (20 sec)

> "On my next normal question, Father Fox calls Lemonade again — the model reloads automatically. No restart, no manual intervention."

**Action:** Switch back to Model Only (if needed) and standard voice, ask another question.

**On screen:**
```
[Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)
```
followed by another `200 OK` on `/api/talk`.

---

## 10. Why This Matters (20 sec)

> "This is local-first AI on hardware people actually own — a 4 GB GPU, not a datacenter. Lemonade provides the OpenAI-compatible runtime layer; the handoff pattern is open source and reusable. No cloud inference required. The same approach extends to any second local client that needs the GPU."

**On screen:** README "Why This Matters" bullets.

---

## 11. Future: Kayock AI Resource Governor (15 sec) — PLANNED / FUTURE

> "Today the handoff is explicit — unload, wait, proceed. The planned Kayock AI Resource Governor will centralize VRAM monitoring, app priority, and safe benchmarking with automatic rollback."

**On screen:** [`governor/README.md`](../governor/README.md) diagram. Label clearly as **future work**.

---

## Recording Checklist

- [ ] Journal or log visible for unload and return-to-Lemonade lines
- [ ] Character voice audible (proves RVC path)
- [ ] No API keys, `.env`, or private IPs visible on screen
- [ ] Distinguish verified demo from future Governor slide

**Total target:** ~2:30 – 3:00
