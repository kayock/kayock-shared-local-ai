"""
Father Fox → Lemonade chat completions (reference extract).

Source: /home/kayock/father-fox-hub/app.py
Marker: FATHER_FOX_LEMONADE_MODEL_ONLY_V1

This is a cleaned reference example. It is not the running Father Fox app.
"""

from __future__ import annotations

import json
import os
import urllib.request

LEMONADE_URL = os.getenv("LEMONADE_URL", "http://127.0.0.1:13305").rstrip("/")
LEMONADE_API_KEY = os.getenv("LEMONADE_API_KEY", "").strip()
LEMONADE_MODEL = os.getenv("LEMONADE_MODEL", "gpt-oss-20b-MXFP4").strip()


def lemonade_chat(messages: list[dict], *, timeout: int = 300) -> str:
    """
    Send a non-streaming chat completion to Lemonade.

  Father Fox uses this path when collection == "Model Only".
    """
    if not LEMONADE_API_KEY:
        raise RuntimeError("LEMONADE_API_KEY is not configured")

    payload = {
        "model": LEMONADE_MODEL,
        "messages": messages,
        "stream": False,
    }

    request = urllib.request.Request(
        f"{LEMONADE_URL}/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LEMONADE_API_KEY}",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.loads(response.read())

    try:
        content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Unexpected Lemonade response format") from exc

    if not content:
        raise RuntimeError("Lemonade returned an empty response")

    return str(content).strip()


if __name__ == "__main__":
    reply = lemonade_chat(
        [
            {
                "role": "user",
                "content": "Say hello in one short sentence.",
            }
        ]
    )
    print(reply)
