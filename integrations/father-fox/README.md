# Father Fox → Lemonade Integration

Reference extract from Father Fox Voice Hub (`/home/kayock/father-fox-hub/app.py`).

## What This Shows

When the user selects **Model Only** knowledge, Father Fox bypasses the NOMAD/Ollama RAG backend and calls Lemonade directly:

```
POST {LEMONADE_URL}/v1/chat/completions
Authorization: Bearer {LEMONADE_API_KEY}

{
  "model": "gpt-oss-20b-MXFP4",
  "messages": [...],
  "stream": false
}
```

## Configuration

| Variable | Default |
|----------|---------|
| `LEMONADE_URL` | `http://127.0.0.1:13305` |
| `LEMONADE_API_KEY` | *(required)* |
| `LEMONADE_MODEL` | `gpt-oss-20b-MXFP4` |

## Files

| File | Purpose |
|------|---------|
| `lemonade_chat.py` | Minimal chat-completions client |

## Routing Logic

Father Fox routes by collection name:

- `Model Only` → Lemonade (this integration)
- Any named collection → `http://<nomad-host>:8080/api/ollama/chat` (legacy RAG; not demonstrated)

## Source Marker

`FATHER_FOX_LEMONADE_MODEL_ONLY_V1` in the original `app.py`.
