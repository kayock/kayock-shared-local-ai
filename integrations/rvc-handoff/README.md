# RVC GPU Handoff Integration

Reference extract from Father Fox Voice Hub showing how Lemonade VRAM is released before RVC character voice synthesis.

## Problem

On a Quadro P2000 (4 GB VRAM), `gpt-oss-20b-MXFP4` and RVC voice models cannot coexist on the GPU.

## Solution

Before calling Kayock Voice (`POST https://127.0.0.1:8766/speak`) with a special character voice:

1. `release_lemonade_gpu_for_rvc()` — `POST /v1/unload`
2. `release_ollama_gpu_for_rvc()` — `ollama stop` for legacy models
3. `sleep(1.0)` — VRAM grace period
4. Proceed with RVC synthesis

## Special Voices That Trigger Handoff

- `batman`
- `optimus_prime`
- `darth_vader`
- `iron_man`

## Return to Lemonade

The next `POST /v1/chat/completions` reloads the model automatically. No Lemonade restart is needed.

## Files

| File | Purpose |
|------|---------|
| `lemonade_unload.py` | Unload + Ollama cleanup reference |

## Source Markers

- `FATHER_FOX_LEMONADE_RVC_HANDOFF_V1`
- `FATHER_FOX_RVC_GPU_HANDOFF_V1`

## Related Documentation

- [`docs/gpu-handoff.md`](../../docs/gpu-handoff.md)
