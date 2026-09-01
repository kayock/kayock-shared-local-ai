# Kayock Local AI Trophy Room

**Contest showcase and observability dashboard** — not an AI runtime.

## Purpose

Visually demonstrate Kayock Shared Local AI within seconds:

- Verified milestones (Father Fox, Lemonade, RVC handoff, Governor)
- Live read-only GPU telemetry
- GPU handoff lifecycle with runtime evidence timestamps
- Governor THROUGHPUT optimization (+4.22% verified)
- Sanitized evidence vault

## Architecture

```
Browser → Trophy Room (FastAPI :8771)
              ├── adapters/telemetry.py  → Governor nvidia-smi collector
              ├── adapters/services.py   → HTTP health probes (read-only)
              ├── adapters/evidence.py   → Repository markdown evidence
              └── adapters/governor_data.py → Verified constants + SQLite (ro)
```

Trophy Room does **not** call `/v1/unload`, modify Lemonade, or control Father Fox.

## Run

```bash
cd /home/kayock/kayock-shared-local-ai
pip install -r trophy-room/requirements.txt
# Optional for Lemonade model list:
export LEMONADE_API_KEY="your-local-key"

cd trophy-room
python app.py
```

Open **http://127.0.0.1:8771**

Port **8771** — does not conflict with Father Fox (8765), RVC (8766), Governor (8770), or Lemonade (13305).

## Views

| Tab | Content |
|-----|---------|
| 🏆 Trophy Room | Milestones + Governor panel |
| 🧠 Model Arena | Model info + verified benchmarks |
| ⚡ GPU Handoff | Lifecycle diagram + live GPU |
| 🌐 Local AI Clients | Detected/planned services |
| 📜 Evidence Vault | Expandable sanitized evidence |

## Data Sources

| Source | Type |
|--------|------|
| Repository markdown evidence | Static (committed) |
| `governor/data/governor.sqlite` | Live read-only (optional) |
| nvidia-smi / psutil | Live polling (4s) |
| Service health URLs | Live polling |

## Detected Local Systems (2026-09-01)

| System | Status |
|--------|--------|
| Father Fox | **ONLINE** — verified |
| Lemonade | **ONLINE** — verified |
| Governor dashboard | **ONLINE** on :8770 |
| Kayock Voice RVC | **ONLINE** on :8766 |
| Whispeer | **PLANNED** — no source |
| NOMAD | **PLANNED** |
| Comic Reader | **PLANNED** — source at ~/ocr-lab, not running |
| Audio Notebook | **PLANNED** — source at ~/erics-notebook-portable-deploy |

## Security

- API keys read from environment server-side only
- Never embedded in HTML or JavaScript
- Evidence sanitized (no private IPs, no keys)
- Does not read `/etc/father-fox-lemonade.env`
- Binds to `127.0.0.1` by default

## Tests

```bash
cd /home/kayock/kayock-shared-local-ai
pip install pytest httpx
PYTHONPATH=trophy-room:. pytest trophy-room/tests/ -v
```

## Verified vs Planned

- **VERIFIED** — backed by committed runtime evidence
- **VERIFIED EXPERIMENTAL** — Governor v0.1 with live optimization evidence
- **PLANNED** — not demonstrated or not running locally
