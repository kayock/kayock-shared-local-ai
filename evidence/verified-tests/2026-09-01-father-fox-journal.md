# Father Fox Runtime Journal Evidence

**Classification: VERIFIED FROM RUNTIME LOG**

## Retrieval Command

```bash
journalctl -u father-fox-voice.service \
  --since "2026-09-01 00:10:00" \
  --until "2026-09-01 00:30:00" \
  --no-pager
```

User journal (`journalctl --user -u father-fox-voice.service`) returned no entries for this window.

## Sanitization Notes

- Client IP addresses replaced with `<client-host>:<port>`
- Hostname replaced with `<host>`
- Process IDs retained (non-sensitive)
- Log message text is verbatim from journal output

## Full Session Excerpt

Service restart at 00:16:44, then the verified handoff sequence:

```
Sep 01 00:16:44 <host> systemd[1]: Stopped father-fox-voice.service - Father Fox Voice Hub.
Sep 01 00:16:44 <host> systemd[1]: Started father-fox-voice.service - Father Fox Voice Hub.
Sep 01 00:16:46 <host> python[24464]: INFO:     Uvicorn running on https://0.0.0.0:8765 (Press CTRL+C to quit)
Sep 01 00:17:39 <host> python[24464]: Loading Whisper...
Sep 01 00:17:39 <host> python[24464]: [Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)
Sep 01 00:18:08 <host> python[24464]: [RVC GPU handoff] Unloading Lemonade model: gpt-oss-20b-MXFP4
Sep 01 00:18:12 <host> python[24464]: [RVC GPU handoff] Lemonade VRAM released for RVC.
Sep 01 00:18:12 <host> python[24464]: [RVC GPU handoff] GPU already clear of Ollama models.
Sep 01 00:18:28 <host> python[24464]: INFO:     <client-host>:63577 - "POST /api/talk HTTP/1.1" 200 OK
Sep 01 00:20:15 <host> python[24464]: [Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)
Sep 01 00:20:46 <host> python[24464]: INFO:     <client-host>:64104 - "POST /api/talk HTTP/1.1" 200 OK
```

## What This Proves

| Step | Timestamp (local) | Log evidence |
|------|-------------------|--------------|
| Lemonade inference (`Model Only`) | 00:17:39 | `[Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)` |
| Lemonade model unload | 00:18:08 | `[RVC GPU handoff] Unloading Lemonade model: gpt-oss-20b-MXFP4` |
| VRAM released for RVC | 00:18:12 | `[RVC GPU handoff] Lemonade VRAM released for RVC.` |
| Ollama GPU already clear | 00:18:12 | `[RVC GPU handoff] GPU already clear of Ollama models.` |
| RVC voice request completed | 00:18:28 | `POST /api/talk HTTP/1.1" 200 OK` |
| Return to Lemonade inference | 00:20:15 | `[Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)` |
| Subsequent normal request OK | 00:20:46 | `POST /api/talk HTTP/1.1" 200 OK` |

## Timing Observations (from journal timestamps only)

- Lemonade chat → unload start: ~29 seconds (includes LLM inference + voice pipeline)
- Unload call → VRAM released log: ~4 seconds
- VRAM released → `/api/talk` 200 OK: ~16 seconds (includes RVC synthesis)
- RVC completion → next Lemonade request: ~1 minute 47 seconds (user think time)
- Second Lemonade request → `/api/talk` 200 OK: ~31 seconds

These intervals are observed wall-clock gaps between log lines, not formal benchmarks.
