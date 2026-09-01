# Contest Evidence

Evidence is classified into three tiers throughout this repository:

| Tier | Label | Meaning |
|------|-------|---------|
| 1 | **VERIFIED FROM RUNTIME LOG** | Captured from `journalctl` or equivalent system logs |
| 2 | **VERIFIED FROM SOURCE CODE** | Confirmed by reading application source (not executed here) |
| 3 | **PLANNED / FUTURE** | Design intent only; not implemented or demonstrated |

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

### Key runtime log lines (verbatim message text)

```
[Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)
[RVC GPU handoff] Unloading Lemonade model: gpt-oss-20b-MXFP4
[RVC GPU handoff] Lemonade VRAM released for RVC.
[RVC GPU handoff] GPU already clear of Ollama models.
POST /api/talk HTTP/1.1" 200 OK
[Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)    ← second request (return to Lemonade)
POST /api/talk HTTP/1.1" 200 OK
```

The second `Model Only -> Lemonade` line at **00:20:15** confirms the full handoff cycle: unload → RVC → return to Lemonade inference.

## Verified from Source Code

The following are **VERIFIED FROM SOURCE CODE** in `/home/kayock/father-fox-hub/app.py`:

| Capability | Source marker |
|------------|---------------|
| Lemonade chat for `Model Only` collection | `FATHER_FOX_LEMONADE_MODEL_ONLY_V1` |
| `POST /v1/unload` with `model_name` | `FATHER_FOX_LEMONADE_RVC_HANDOFF_V1` |
| RVC handoff for special voices | `FATHER_FOX_RVC_GPU_HANDOFF_V1` |
| 1-second VRAM grace period | `time.sleep(1.0)` in unload functions |
| Auto-reload comment on next request | Comment in `release_lemonade_gpu_for_rvc()` |

Runtime journal evidence now corroborates the auto-reload behavior that was previously source-comment-only.

## Search Performed (Initial Repository Creation)

| Item | Result |
|------|--------|
| `AMD_Lemonade_Contest_Evidence_Log.md` | **Not found** on disk |
| `/home/kayock/kayock-social-agent` | **Directory does not exist** |
| `journalctl -u father-fox-voice.service` | **Runtime evidence recovered** (see above) |
| `journalctl --user -u father-fox-voice.service` | No entries for test window |

## Not Verified / Not Demonstrated

| Claim | Status |
|-------|--------|
| Whispeer using Lemonade | **PLANNED / FUTURE** — no source on this machine |
| NOMAD as Lemonade client | Uses separate RAG backend; not part of Lemonade demo |
| Runtime benchmarks (TTFT, TPS) | Not measured; only wall-clock gaps between journal lines |
| Multiple independent apps sharing Lemonade | Only Father Fox + RVC workload demonstrated |
| Kayock AI Resource Governor | **PLANNED / FUTURE** |

## Missing Evidence File

`AMD_Lemonade_Contest_Evidence_Log.md` was not found under `/home/kayock`. Runtime journal excerpts substitute for formal test documentation.

## Evidence Repository Policy

See [`evidence/README.md`](../evidence/README.md).
