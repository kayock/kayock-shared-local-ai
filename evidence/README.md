# Evidence Directory

Sanitized contest evidence for Kayock Shared Local AI.

## Evidence Tiers

| Label | Meaning |
|-------|---------|
| **VERIFIED FROM RUNTIME LOG** | Captured from system journal |
| **VERIFIED FROM SOURCE CODE** | Confirmed by reading application source |
| **PLANNED / FUTURE** | Design only |

## Contents

| Path | Type | Description |
|------|------|-------------|
| `verified-tests/2026-09-01-father-fox-journal.md` | Runtime log | Full handoff session (sanitized) |
| `verified-tests/README.md` | Index | Test result summary |
| `sanitized-logs/father-fox-log-patterns.md` | Source-derived | Expected log strings from `print()` calls |

## Policy

1. Never copy raw logs without redacting client IPs, tokens, and private paths.
2. Never include model weights, databases, or RAG corpora.
3. Distinguish runtime evidence from source-derived patterns.

## Source Files Referenced

| File | Use |
|------|-----|
| `journalctl -u father-fox-voice.service` | Primary runtime evidence |
| `/home/kayock/father-fox-hub/app.py` | Source code cross-reference |

`AMD_Lemonade_Contest_Evidence_Log.md` was not found on disk; journal excerpts serve as substitute evidence.
