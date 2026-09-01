# Sanitized Log Patterns (Source-Derived)

**Classification: VERIFIED FROM SOURCE CODE** (expected `print()` output)

These patterns match Father Fox `app.py` and were **confirmed in actual runtime logs** on 2026-09-01. See [`verified-tests/2026-09-01-father-fox-journal.md`](../verified-tests/2026-09-01-father-fox-journal.md) for the captured journal excerpt.

## Lemonade Chat (Model Only)

```
[Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)
```

## Lemonade Unload — Success

```
[RVC GPU handoff] Unloading Lemonade model: gpt-oss-20b-MXFP4
[RVC GPU handoff] Lemonade VRAM released for RVC.
```

## Ollama Cleanup

```
[RVC GPU handoff] GPU already clear of Ollama models.
```

## HTTP Success

```
POST /api/talk HTTP/1.1" 200 OK
```

## Patterns Not Seen in Recovered Journal

The following are implemented in source but did not appear in the 2026-09-01 session:

```
[RVC GPU handoff] Lemonade model was already unloaded.
[RVC GPU handoff] No Lemonade API key; skipping Lemonade unload.
[RVC GPU handoff] Unloading Ollama model: <model-name>
[RVC GPU handoff] Ollama VRAM released for RVC.
```

## Source

`/home/kayock/father-fox-hub/app.py` — September 2026.
