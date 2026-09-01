# Verified Tests

## Runtime Evidence — RECOVERED

**VERIFIED FROM RUNTIME LOG**

Journal evidence from `father-fox-voice.service` on **2026-09-01** (00:17:39 – 00:20:46 local time) confirms the full Lemonade ↔ RVC handoff cycle including return to Lemonade.

| Test | Result | Evidence |
|------|--------|----------|
| Lemonade chat (`Model Only`, `gpt-oss-20b-MXFP4`) | Pass | Journal 00:17:39 |
| Lemonade model unload | Pass | Journal 00:18:08 |
| VRAM released for RVC | Pass | Journal 00:18:12 |
| Ollama GPU clear check | Pass | Journal 00:18:12 |
| RVC voice request (`/api/talk`) | Pass | Journal 00:18:28 `200 OK` |
| Return to Lemonade inference | Pass | Journal 00:20:15 |
| Subsequent normal request | Pass | Journal 00:20:46 `200 OK` |

Full excerpt: [`2026-09-01-father-fox-journal.md`](2026-09-01-father-fox-journal.md)

## Source-Only (Not Re-Executed Here)

| Test | Evidence type |
|------|---------------|
| Unload API request shape | **VERIFIED FROM SOURCE CODE** |
| Special RVC voice list | **VERIFIED FROM SOURCE CODE** |
| 1-second VRAM grace period | **VERIFIED FROM SOURCE CODE** |

## Not Demonstrated

| Test | Status |
|------|--------|
| Whispeer → Lemonade | **PLANNED / FUTURE** |
| NOMAD → Lemonade | Not applicable (separate backend) |
| TTFT / TPS benchmarks | Not measured |

## Retrieval

```bash
journalctl -u father-fox-voice.service \
  --since "2026-09-01 00:10:00" \
  --until "2026-09-01 00:30:00" \
  --no-pager
```
