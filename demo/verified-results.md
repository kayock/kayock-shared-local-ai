# Verified Results — Authoritative Contest Evidence

Single reference page for judges. Every row links to committed evidence. **Pre-fix optimizer results are not contest performance evidence.**

Release: tag **`contest-v0.3-trophy-room`**

---

## VERIFIED RUNTIME — Dynamic GPU Handoff

| Claim | Evidence |
|-------|----------|
| Father Fox → Lemonade inference | [Father Fox journal](../evidence/verified-tests/2026-09-01-father-fox-journal.md) — `00:17:39` |
| Model: `gpt-oss-20b-MXFP4` | Same journal — `[Father Fox] Model Only -> Lemonade (gpt-oss-20b-MXFP4)` |
| Lemonade unload before RVC | Same journal — `00:18:08` |
| VRAM release | Same journal — `00:18:12` |
| RVC GPU handoff / talk success | Same journal — `00:18:28` POST `/api/talk` 200 OK |
| Successful return to Lemonade | Same journal — `00:20:15` |
| Subsequent normal request OK | Same journal — `00:20:46` POST `/api/talk` 200 OK |
| Handoff sequence diagram | [docs/gpu-handoff.md](../docs/gpu-handoff.md) |
| Reference unload client | [integrations/rvc-handoff/lemonade_unload.py](../integrations/rvc-handoff/lemonade_unload.py) |
| Reference chat client | [integrations/father-fox/lemonade_chat.py](../integrations/father-fox/lemonade_chat.py) |

### Handoff Timeline (journal timestamps)

```
00:17:39  Father Fox → Lemonade (gpt-oss-20b-MXFP4)
00:18:08  Lemonade model unload
00:18:12  VRAM released for RVC
00:18:28  RVC /api/talk 200 OK
00:20:15  Return to Lemonade
00:20:46  /api/talk 200 OK
```

---

## VERIFIED GOVERNOR — Kayock AI Resource Governor v0.1

| Claim | Evidence |
|-------|----------|
| Quadro P2000 telemetry | [Governor benchmark results](../governor/evidence/benchmark-results-2026-09-01.md) — 3191 MiB peak VRAM |
| Lemonade benchmark harness | Same file — avg TTFT **7.15 s**, TPS **7.01** |
| Bounded optimizer (max_tokens, temperature) | [Governor README](../governor/README.md) — safety model |
| REJECT / KEEP / NOT_BEST decisions | [Throughput optimization](../governor/evidence/throughput-optimization-2026-09-01.md) — candidate table |
| Saved winning profile | Same file — `saved_profiles.THROUGHPUT` = `{480, 0.7}` |
| Corrected +4.22% THROUGHPUT improvement | Same file — see metrics below |
| Optimizer bug fix + regression tests | Commit `d682462`, [governor/tests/test_optimizer.py](../governor/tests/test_optimizer.py) |
| Governor architecture | [governor/README.md](../governor/README.md) |

### THROUGHPUT Optimization (corrected run only)

| | Baseline | Winner |
|---|----------|--------|
| `max_tokens` | 512 | **480** |
| `temperature` | 0.7 | **0.7** |
| Score | **14.639872171624882** | **15.25802453529699** |
| Improvement | — | **~+4.22%** |
| TTFT (avg) | — | **6.7409 s** |
| TPS (avg) | — | **7.4384** |

### Candidate Decisions (corrected run)

| # | Config | Score | Decision |
|---|--------|-------|----------|
| — | `{512, 0.7}` | 14.6399 | baseline |
| 1 | `{480, 0.6}` | 14.3498 | **REJECT** |
| 2 | `{480, 0.7}` | 15.2580 | **KEEP** |
| 3 | `{480, 0.8}` | 15.1551 | **NOT_BEST** |
| 4 | `{512, 0.6}` | 14.1270 | **REJECT** |
| 5 | `{512, 0.8}` | 15.0987 | **NOT_BEST** |

### Automated Tests

| Suite | Tests | Location |
|-------|-------|----------|
| Governor | 16 | `governor/tests/` |
| Trophy Room | 10 | `trophy-room/tests/` |
| **Total** | **26** | Run: `pytest trophy-room/tests/ governor/tests/` |

---

## VERIFIED SHOWCASE — Trophy Room

| Claim | Evidence |
|-------|----------|
| Read-only contest dashboard (:8771) | [trophy-room/README.md](../trophy-room/README.md) |
| Five views (Trophy Room, Model Arena, GPU Handoff, Clients, Evidence Vault) | Same |
| Sanitized evidence display | [trophy-room/adapters/evidence.py](../trophy-room/adapters/evidence.py) |
| Verified constants (+4.22%, handoff timeline) | [trophy-room/config.py](../trophy-room/config.py) |

---

## NOT CONTEST EVIDENCE

| Item | Why excluded | Reference |
|------|--------------|-----------|
| Pre-`d682462` THROUGHPUT run | Order-dependent global-best bug | [Throughput optimization — Superseded section](../governor/evidence/throughput-optimization-2026-09-01.md) |
| Buggy winner `{512, 0.8}` @ ~14.90 | Incorrect overwrite of global best | Same |
| Whispeer / NOMAD demos | Source not demonstrated | [docs/roadmap.md](../docs/roadmap.md) |
| Cloud inference | Not used in verified session | Father Fox journal |

---

## Evidence File Index

```
evidence/verified-tests/2026-09-01-father-fox-journal.md   ← GPU handoff
governor/evidence/benchmark-results-2026-09-01.md            ← benchmark harness
governor/evidence/throughput-optimization-2026-09-01.md      ← +4.22% optimizer
docs/gpu-handoff.md                                        ← architecture
trophy-room/README.md                                      ← live demo
demo/README.md                                               ← you are here
```
