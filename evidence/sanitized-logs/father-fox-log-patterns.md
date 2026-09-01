# Sanitized Log Patterns (Source-Derived)

**These are reconstructed log lines from known `print()` statements in Father Fox source code.**
They are **not** copies of actual runtime logs. No timestamps, benchmarks, or test results are included because `AMD_Lemonade_Contest_Evidence_Log.md` was not found.

## Lemonade Chat (Model Only)

```
[Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)
```

## Lemonade Unload — Success

```
[RVC GPU handoff] Unloading Lemonade model: gpt-oss-20b-MXFP4
[RVC GPU handoff] Lemonade VRAM released for RVC.
```

## Lemonade Unload — Already Unloaded

```
[RVC GPU handoff] Unloading Lemonade model: gpt-oss-20b-MXFP4
[RVC GPU handoff] Lemonade model was already unloaded.
```

## Lemonade Unload — Skipped (No API Key)

```
[RVC GPU handoff] No Lemonade API key; skipping Lemonade unload.
```

## Ollama Cleanup (Legacy)

```
[RVC GPU handoff] Unloading Ollama model: <model-name>
[RVC GPU handoff] Ollama VRAM released for RVC.
```

```
[RVC GPU handoff] GPU already clear of Ollama models.
```

## Source

All message strings match `/home/kayock/father-fox-hub/app.py` as of September 2026.
