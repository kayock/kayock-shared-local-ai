# Kayock Shared Local AI

**One Lemonade server. Multiple independent local-AI applications. Shared hardware. No cloud required.**

Entry for the [AMD Lemonade Developer Challenge](https://www.amd.com/en/developer/resources/technical-articles/2025/amd-lemonade-developer-challenge.html). This repository documents how multiple household applications share a single AMD Lemonade inference server on constrained local GPU hardware.

## What Is Verified Here

| Capability | Status | Source |
|------------|--------|--------|
| Father Fox → Lemonade (`gpt-oss-20b-MXFP4`) | **Verified in source** | [`integrations/father-fox/`](integrations/father-fox/) |
| Lemonade `/v1/unload` before RVC | **Verified in source** | [`integrations/rvc-handoff/`](integrations/rvc-handoff/) |
| VRAM release + RVC GPU handoff | **Verified in source** | [`docs/gpu-handoff.md`](docs/gpu-handoff.md) |
| Auto-reload on next Lemonade request | **Documented in source comments** | [`integrations/rvc-handoff/lemonade_unload.py`](integrations/rvc-handoff/lemonade_unload.py) |
| Whispeer → Lemonade | **Not found on this machine** | See [`docs/integrations.md`](docs/integrations.md) |
| Contest evidence log | **File not found** | See [`docs/contest-evidence.md`](docs/contest-evidence.md) |

## Architecture

```mermaid
flowchart TB
    subgraph Apps["Independent Applications"]
        FF["Father Fox Voice Hub<br/>:8765"]
        WH["Whispeer<br/>(not present locally)"]
        RVC["Kayock Voice / RVC<br/>:8766"]
    end

    subgraph Shared["Shared Local Stack"]
        LM["AMD Lemonade Server<br/>:13305"]
        GPU["GPU — Quadro P2000 4 GB VRAM"]
    end

    FF -->|"POST /v1/chat/completions<br/>gpt-oss-20b-MXFP4"| LM
    WH -.->|"planned / not verified locally"| LM
    FF -->|"POST /speak (character voices)"| RVC
    FF -->|"POST /v1/unload before RVC"| LM
    LM --> GPU
    RVC --> GPU
```

## GPU Handoff Lifecycle

```mermaid
sequenceDiagram
    participant User
    participant FatherFox as Father Fox
    participant Lemonade
    participant GPU
    participant RVC as Kayock Voice RVC

    User->>FatherFox: Voice request (Model Only)
    FatherFox->>Lemonade: POST /v1/chat/completions
    Lemonade->>GPU: Load gpt-oss-20b-MXFP4
    Lemonade-->>FatherFox: LLM reply

    User->>FatherFox: Reply with special RVC voice
    FatherFox->>Lemonade: POST /v1/unload
    Lemonade->>GPU: Release VRAM
    Note over FatherFox: sleep 1s grace period
    FatherFox->>RVC: POST /speak
    RVC->>GPU: Load voice model

    User->>FatherFox: Next normal request
    FatherFox->>Lemonade: POST /v1/chat/completions
    Note over Lemonade: Model reloads automatically
    Lemonade-->>FatherFox: LLM reply
```

## Repository Layout

```
kayock-shared-local-ai/
├── README.md
├── LICENSE
├── SECURITY.md
├── docs/
│   ├── architecture.md
│   ├── contest-evidence.md
│   ├── gpu-handoff.md
│   ├── integrations.md
│   └── roadmap.md
├── integrations/
│   ├── father-fox/       # Lemonade chat completions
│   ├── whispeer/         # placeholder — source not found
│   └── rvc-handoff/      # unload + VRAM release
├── evidence/
│   ├── README.md
│   ├── verified-tests/
│   └── sanitized-logs/
└── governor/             # future work — AI Resource Governor
    └── README.md
```

## Quick Start (Reference)

These examples mirror patterns from Father Fox. Set credentials locally:

```bash
export LEMONADE_URL="http://127.0.0.1:13305"
export LEMONADE_API_KEY="your-local-key"
export LEMONADE_MODEL="gpt-oss-20b-MXFP4"
```

See [`integrations/father-fox/lemonade_chat.py`](integrations/father-fox/lemonade_chat.py) for a minimal chat-completions client and [`integrations/rvc-handoff/lemonade_unload.py`](integrations/rvc-handoff/lemonade_unload.py) for the GPU handoff unload call.

## Hardware Context

Father Fox documents a **NVIDIA Quadro P2000 with 4 GB VRAM**. The resident Lemonade LLM and RVC character voices cannot coexist on the GPU simultaneously — the handoff pattern exists specifically for this constraint.

## Future Work

The [Kayock AI Resource Governor](governor/README.md) is a planned self-optimizer for TTFT, TPS, VRAM, and multi-app scheduling. It is **not implemented** in this repository.

## License

MIT — see [LICENSE](LICENSE).
