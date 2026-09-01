"""
Lemonade model unload for RVC GPU handoff (reference extract).

Source: /home/kayock/father-fox-hub/app.py
Markers: FATHER_FOX_LEMONADE_RVC_HANDOFF_V1, FATHER_FOX_RVC_GPU_HANDOFF_V1

This is a cleaned reference example. It is not the running Father Fox app.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.error
import urllib.request

LEMONADE_URL = os.getenv("LEMONADE_URL", "http://127.0.0.1:13305").rstrip("/")
LEMONADE_API_KEY = os.getenv("LEMONADE_API_KEY", "").strip()
LEMONADE_MODEL = os.getenv("LEMONADE_MODEL", "gpt-oss-20b-MXFP4").strip()

OLLAMA_BIN = os.getenv("OLLAMA_BIN", "/usr/local/bin/ollama")

SPECIAL_RVC_VOICES = frozenset({
    "batman",
    "optimus_prime",
    "darth_vader",
    "iron_man",
})

VRAM_GRACE_SECONDS = 1.0


def release_lemonade_gpu_for_rvc() -> None:
    """
    Release Lemonade's resident LLM before loading an RVC voice.

    The next Lemonade chat request automatically reloads the model,
    so callers do not need to restart Lemonade afterward.
    """
    if not LEMONADE_API_KEY:
        print(
            "[RVC GPU handoff] No Lemonade API key; skipping Lemonade unload.",
            flush=True,
        )
        return

    payload = {"model_name": LEMONADE_MODEL}

    request = urllib.request.Request(
        f"{LEMONADE_URL}/v1/unload",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LEMONADE_API_KEY}",
        },
        method="POST",
    )

    print(
        f"[RVC GPU handoff] Unloading Lemonade model: {LEMONADE_MODEL}",
        flush=True,
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")

        if exc.code == 404:
            print(
                "[RVC GPU handoff] Lemonade model was already unloaded.",
                flush=True,
            )
            return

        raise RuntimeError(
            f"Lemonade unload failed HTTP {exc.code}: {body}"
        ) from exc

    if result.get("status") != "success":
        raise RuntimeError(
            f"Lemonade unload returned unexpected result: {result}"
        )

    time.sleep(VRAM_GRACE_SECONDS)

    print(
        "[RVC GPU handoff] Lemonade VRAM released for RVC.",
        flush=True,
    )


def release_ollama_gpu_for_rvc() -> None:
    """
    Unload resident Ollama models (legacy path).

    The Quadro P2000 has 4 GB VRAM. Ollama and RVC cannot fit simultaneously.
    """
    try:
        result = subprocess.run(
            [OLLAMA_BIN, "ps"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            print(
                "[RVC GPU handoff] ollama ps failed:",
                result.stderr.strip(),
                flush=True,
            )
            return

        models = []
        for line in result.stdout.splitlines()[1:]:
            parts = line.split()
            if parts:
                models.append(parts[0])

        if not models:
            print(
                "[RVC GPU handoff] GPU already clear of Ollama models.",
                flush=True,
            )
            return

        for model in models:
            print(
                f"[RVC GPU handoff] Unloading Ollama model: {model}",
                flush=True,
            )
            stopped = subprocess.run(
                [OLLAMA_BIN, "stop", model],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30,
            )
            if stopped.returncode != 0:
                raise RuntimeError(
                    f"Could not unload {model}: {stopped.stderr.strip()}"
                )

        time.sleep(VRAM_GRACE_SECONDS)

        print(
            "[RVC GPU handoff] Ollama VRAM released for RVC.",
            flush=True,
        )

    except Exception as exc:
        raise RuntimeError(
            f"Could not release Ollama GPU memory for RVC: {exc}"
        ) from exc


def release_ai_gpu_for_rvc() -> None:
    """Clear both Lemonade and legacy Ollama allocations before RVC."""
    release_lemonade_gpu_for_rvc()
    release_ollama_gpu_for_rvc()


def needs_gpu_handoff(voice: str) -> bool:
    """Return True if the voice requires unloading LLM models first."""
    return voice in SPECIAL_RVC_VOICES
