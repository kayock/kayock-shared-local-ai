# Evidence Directory

This directory holds sanitized contest evidence. **No unsanitized logs, credentials, or private data belong here.**

## What Was Searched

At repository creation (September 2026), the following were searched under `/home/kayock`:

- `AMD_Lemonade_Contest_Evidence_Log.md` — **not found**
- Application logs mentioning Lemonade handoff — **not copied** (would require sanitization review)
- Runtime test results — **not available**

## Directory Structure

| Path | Purpose |
|------|---------|
| `verified-tests/` | Formal test outputs (empty — awaiting evidence log) |
| `sanitized-logs/` | Redacted log excerpts matching known source patterns |

## Policy

1. **Never** copy raw application logs without redacting IPs, tokens, paths with usernames, or private content.
2. **Never** include model weights, databases, or RAG corpora.
3. Only add entries that can be traced to a verifiable source file or test run.
4. Label synthetic/reconstructed examples clearly.

## Source Files Used for This Repository

| File | What Was Extracted |
|------|-------------------|
| `/home/kayock/father-fox-hub/app.py` | Lemonade config, chat client, unload/handoff logic |
| `/home/kayock/father-fox-hub/backups/app.before-lemonade-20260901-000703.py` | Pre-Lemonade RVC handoff (Ollama only) |
| `/home/kayock/father-fox-hub/backups/app.before-lemonade-rvc-handoff-20260901-001644.py` | Lemonade without unload integration |

## Adding Evidence Later

When `AMD_Lemonade_Contest_Evidence_Log.md` is located:

1. Review for secrets and private data
2. Place a sanitized copy in `verified-tests/`
3. Update `docs/contest-evidence.md` with entry cross-references
