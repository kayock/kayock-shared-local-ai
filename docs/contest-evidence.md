# Contest Evidence

This document records what evidence was searched for, what was found, and what could not be verified on the local machine at repository creation time.

## Search Performed

The following paths and patterns were searched under `/home/kayock`:

| Item | Result |
|------|--------|
| `AMD_Lemonade_Contest_Evidence_Log.md` | **Not found** |
| `/home/kayock/kayock-social-agent` | **Directory does not exist** |
| `Whispeer` / `whispeer` in source files | **No matches** |
| `Lemonade` in source files | Found in `father-fox-hub/app.py` and backups |
| `gpt-oss-20b-MXFP4` | Found in `father-fox-hub/app.py` |
| `RVC GPU handoff` | Found in `father-fox-hub/app.py` |
| `Lemonade VRAM released` | Found in `father-fox-hub/app.py` |

## Verified from Source Code

The following capabilities are **confirmed by reading** `/home/kayock/father-fox-hub/app.py`:

### 1. Father Fox → Lemonade (Model Only)

When `collection == "Model Only"`, Father Fox sends a non-streaming chat completion request to Lemonade with the configured model (`gpt-oss-20b-MXFP4` by default).

Source markers: `FATHER_FOX_LEMONADE_MODEL_ONLY_V1`

### 2. Lemonade Model Unload

`release_lemonade_gpu_for_rvc()` POSTs to `{LEMONADE_URL}/v1/unload` with `{"model_name": LEMONADE_MODEL}` and expects `{"status": "success"}`.

Source markers: `FATHER_FOX_LEMONADE_RVC_HANDOFF_V1`

### 3. VRAM Release

After a successful unload, the code sleeps 1 second and logs:

```
[RVC GPU handoff] Lemonade VRAM released for RVC.
```

### 4. RVC GPU Handoff

Special character voices (`batman`, `optimus_prime`, `darth_vader`, `iron_man`) trigger `release_ai_gpu_for_rvc()` before calling Kayock Voice at `https://127.0.0.1:8766/speak`.

Source markers: `FATHER_FOX_RVC_GPU_HANDOFF_V1`

### 5. Return to Lemonade

Source comment in `release_lemonade_gpu_for_rvc()`:

> The next Lemonade chat request automatically reloads the model, so Father Fox does not need to restart Lemonade afterward.

This is a **design assertion in code comments**, not a captured benchmark or test result.

## Not Verified

| Claim | Reason |
|-------|--------|
| Whispeer using Lemonade | No Whispeer source code found on this machine |
| Runtime benchmarks (TTFT, TPS) | No evidence log file found; not invented here |
| Timestamps of successful handoff tests | No evidence log file found |
| `kayock-social-agent` integration | Directory absent at expected path |

## Missing Evidence File

`AMD_Lemonade_Contest_Evidence_Log.md` was requested as the primary evidence source but **does not exist** anywhere under `/home/kayock` (searched with `find` and filename/content grep, September 2026).

If this file is created later, place a sanitized copy under `evidence/verified-tests/` and update this document with cross-references to specific test entries.

## Bash History Note

A single Lemonade CLI invocation appears in shell history (model load command for `gpt-oss-20b-MXFP4` with Vulkan backend). This is noted for completeness but is **not** included as contest evidence because it was not part of a formal test log.

## Evidence Repository Policy

See [`evidence/README.md`](../evidence/README.md) for rules on what may be added to the evidence directory.
