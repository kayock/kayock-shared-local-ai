# Whispeer Integration

## Status: Not Found Locally

Whispeer was expected to integrate with the shared Lemonade server as a second independent application. At repository creation time:

| Check | Result |
|-------|--------|
| `/home/kayock/kayock-social-agent` | **Directory does not exist** |
| `Whispeer` / `whispeer` in `/home/kayock` source | **No matches** |
| Lemonade client code for Whispeer | **Not available** |

## Intended Pattern

When Whispeer source becomes available, the integration should follow the same pattern as Father Fox:

```python
# Expected pattern (not verified — illustrative only)
POST {LEMONADE_URL}/v1/chat/completions
Authorization: Bearer {LEMONADE_API_KEY}

{
  "model": "gpt-oss-20b-MXFP4",
  "messages": [...],
  "stream": false
}
```

## Placeholder

No reference code is included here because no Whispeer source was found to extract from. This avoids inventing integration details that cannot be verified.

## Next Steps

1. Locate or deploy `kayock-social-agent` / Whispeer source
2. Extract a minimal Lemonade client (mirror `integrations/father-fox/lemonade_chat.py`)
3. Update [`docs/integrations.md`](../../docs/integrations.md) and [`docs/contest-evidence.md`](../../docs/contest-evidence.md)
