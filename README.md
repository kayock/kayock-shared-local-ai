# Kayock Shared Local AI

**Lemonade inference and specialized RVC workloads dynamically sharing constrained local GPU resources.**

Entry for the [AMD Lemonade Developer Challenge](https://www.amd.com/en/developer/resources/technical-articles/2025/amd-lemonade-developer-challenge.html). This repository documents and demonstrates — with **runtime journal evidence** — how Father Fox Voice Hub coordinates Lemonade LLM inference (`gpt-oss-20b-MXFP4`) and RVC character voice synthesis on a single 4 GB GPU.

Lemonade is the OpenAI-compatible local runtime/API layer. The project runs on consumer hardware (verified on NVIDIA Quadro P2000); it is not limited to AMD GPUs.

## Contest Demo

**[Kayock Shared Local AI — Contest Demo](demo/README.md)** — judge-friendly package for the AMD Lemonade Developer Challenge.

| Resource | Link |
|----------|------|
| Demo overview | [demo/README.md](demo/README.md) |
| 2–3 min script | [demo/demo-script.md](demo/demo-script.md) |
| Recording runbook | [demo/demo-runbook.md](demo/demo-runbook.md) |
| Submission copy | [demo/contest-summary.md](demo/contest-summary.md) |
| Verified results | [demo/verified-results.md](demo/verified-results.md) |
| Live showcase | [Trophy Room](trophy-room/README.md) — `http://127.0.0.1:8771` |

## What Is Verified Here

| Capability | Status | Evidence type |
|------------|--------|---------------|
| Father Fox → Lemonade (`gpt-oss-20b-MXFP4`) | **Verified** | Runtime log + source |
| Lemonade `/v1/unload` before RVC | **Verified** | Runtime log + source |
| VRAM release + RVC GPU handoff | **Verified** | Runtime log + source |
| Return to Lemonade on next request | **Verified** | Runtime log (2026-09-01 00:20:15) |
| RVC `/api/talk` success after handoff | **Verified** | Runtime log (`200 OK`) |
| Whispeer / additional Lemonade clients | **Not demonstrated** | Planned — source absent locally |
| Kayock AI Resource Governor | **Planned** | Design only |

Evidence file: [`evidence/verified-tests/2026-09-01-father-fox-journal.md`](evidence/verified-tests/2026-09-01-father-fox-journal.md)

## Why This Matters

- **Local-first AI** — Voice conversations stay on your machine. Lemonade serves the LLM; Father Fox handles speech I/O.
- **Resource-constrained hardware** — A 4 GB GPU cannot hold a 20B model and RVC weights simultaneously. This project proves cooperative sharing instead of cloud offload.
- **Cooperative GPU use** — Explicit `POST /v1/unload` before RVC, automatic model reload on the next chat request. No Lemonade restart required.
- **Open-source reusable pattern** — Reference clients in [`integrations/`](integrations/) extract the handoff logic for adoption in other local apps.
- **No cloud inference required** — The verified session used only local Lemonade, Father Fox, and Kayock Voice RVC.

## Architecture

```mermaid
flowchart TB
    subgraph Verified["Verified Workloads"]
        FF["Father Fox Voice Hub<br/>:8765"]
        RVC["Kayock Voice / RVC<br/>:8766"]
    end

    subgraph Shared["Shared Local Stack"]
        LM["Lemonade Server<br/>:13305"]
        GPU["GPU — 4 GB VRAM"]
    end

    subgraph Future["Planned / Future Clients"]
        WH["Whispeer"]
        NOMAD["NOMAD RAG backend"]
    end

    FF -->|"POST /v1/chat/completions<br/>gpt-oss-20b-MXFP4"| LM
    FF -->|"POST /v1/unload before RVC"| LM
    FF -->|"POST /speak (character voices)"| RVC
    LM --> GPU
    RVC --> GPU
    WH -.->|"future"| LM
    FF -.->|"RAG collections"| NOMAD
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

*Sequence verified from runtime journal on 2026-09-01.*

## Repository Layout

```
kayock-shared-local-ai/
├── README.md
├── LICENSE
├── SECURITY.md
├── docs/
│   ├── architecture.md
│   ├── contest-evidence.md
│   ├── demo-script.md
│   ├── gpu-handoff.md
│   ├── integrations.md
│   └── roadmap.md
├── integrations/
│   ├── father-fox/       # Lemonade chat completions
│   ├── rvc-handoff/      # unload + VRAM release
│   └── whispeer/         # future client placeholder
├── evidence/
│   ├── verified-tests/   # runtime journal excerpts
│   └── sanitized-logs/
└── governor/             # AI Resource Governor (experimental on governor-v0.1)
    ├── README.md
    └── ...               # python -m governor CLI
```

## Quick Start (Reference)

```bash
export LEMONADE_URL="http://127.0.0.1:13305"
export LEMONADE_API_KEY="your-local-key"
export LEMONADE_MODEL="gpt-oss-20b-MXFP4"
```

See [`integrations/father-fox/lemonade_chat.py`](integrations/father-fox/lemonade_chat.py) and [`integrations/rvc-handoff/lemonade_unload.py`](integrations/rvc-handoff/lemonade_unload.py).

## Demo Recording

Follow [`docs/demo-script.md`](docs/demo-script.md) for a 2–3 minute contest video walkthrough.

## Hardware Context

Verified on a **NVIDIA Quadro P2000 (4 GB VRAM)**. Lemonade serves `gpt-oss-20b-MXFP4`; RVC character voices require a separate GPU allocation — coordinated via explicit unload.

## Kayock AI Resource Governor (governor-v0.1 branch)

**VERIFIED** telemetry, benchmark harness, and corrected THROUGHPUT optimizer on live Lemonade (`gpt-oss-20b-MXFP4`).

| Evidence | Result |
|----------|--------|
| Benchmark harness | avg TTFT 7.15 s, TPS 7.01 — [`governor/evidence/benchmark-results-2026-09-01.md`](governor/evidence/benchmark-results-2026-09-01.md) |
| THROUGHPUT optimizer | **+4.22%** score → `{480, 0.7}` — [`governor/evidence/throughput-optimization-2026-09-01.md`](governor/evidence/throughput-optimization-2026-09-01.md) |

An order-dependent global-best bug was found during live testing and fixed in commit `d682462`.

```bash
pip install -r governor/requirements.txt
export LEMONADE_API_KEY="your-local-key"
python -m governor status
python -m governor optimize --profile THROUGHPUT
```

See [`governor/README.md`](governor/README.md) for architecture, safety model, and commands.

## Kayock Local AI Trophy Room (trophy-room-v0.1 branch)

**Contest showcase dashboard** at **http://127.0.0.1:8771** — observability only, not an AI runtime.

```bash
pip install -r trophy-room/requirements.txt
cd trophy-room && python app.py
```

Five views: Trophy Room, Model Arena, GPU Handoff, Local AI Clients, Evidence Vault. See [`trophy-room/README.md`](trophy-room/README.md).

Whispeer and NOMAD remain **PLANNED / FUTURE** Lemonade clients — not demonstrated in this repository.

## License

MIT — see [LICENSE](LICENSE).
